"""
Atto 3 — Testiamo il contratto dei tool
========================================
Structural contract tests for map_api_rest and generate_ts_api,
following the same pattern as S04_03_Lab_04_demo.ipynb Atto 3.

Each test:
  1. Calls the tool function directly (integration test, real LLM call)
  2. Parses the JSON output
  3. Asserts the structural contract

Run from the src/ directory:
    pytest test/ -v
"""

import json
import shutil

import pytest

from tool.tool import create_file_ts_api, generate_ts_api, map_api_rest

# ---------------------------------------------------------------------------
# Sample input
# ---------------------------------------------------------------------------

SAMPLE_API_DOC = """
POST /api/v1/users/{userId}/orders

Crea un nuovo ordine per un utente specifico.

Path Parameters:
  - userId (string, required): ID univoco dell'utente.

Request Body:
  - productId (string, required): ID del prodotto.
  - quantity (integer, required): Quantità ordinata.
  - note (string, optional): Note aggiuntive.

Responses:
  201 Created
    - orderId (string): ID dell'ordine creato.
    - status (string): Stato dell'ordine.
    - createdAt (string, timestamp): Data di creazione.

  400 Bad Request
    - message (string): Descrizione dell'errore.

  404 Not Found
    - message (string): Utente non trovato.
"""


# ---------------------------------------------------------------------------
# Fixtures  (scope=module → 1 LLM call per classe, non 1 per test)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def map_output() -> dict:
    """Calls map_api_rest once and returns the parsed JSON."""
    raw = map_api_rest.func(text=SAMPLE_API_DOC)
    return json.loads(raw)


@pytest.fixture(scope="module")
def ts_output(map_output: dict) -> dict:
    """Chains generate_ts_api on the output of map_api_rest."""
    raw = generate_ts_api.func(contract_json=json.dumps(map_output, ensure_ascii=False))
    return json.loads(raw)


# ---------------------------------------------------------------------------
# map_api_rest — structural contract
# ---------------------------------------------------------------------------


class TestMapApiRestContract:

    def test_output_is_valid_json(self):
        raw = map_api_rest.func(text=SAMPLE_API_DOC)
        parsed = json.loads(raw)
        assert isinstance(parsed, dict), "output deve essere un oggetto JSON"

    def test_required_fields_present(self, map_output):
        required = {"method", "uri", "request_params", "path_params", "request_body", "responses"}
        missing = required - map_output.keys()
        assert not missing, f"campi mancanti: {missing}"

    def test_method_is_valid_http_verb(self, map_output):
        valid = {"GET", "POST", "PUT", "DELETE", "PATCH"}
        assert map_output["method"].upper() in valid, f"method non valido: {map_output['method']}"

    def test_uri_is_non_empty_string(self, map_output):
        assert isinstance(map_output["uri"], str) and map_output["uri"].strip(), \
            "uri non deve essere vuoto"

    def test_param_groups_are_lists(self, map_output):
        for field in ("request_params", "path_params", "request_body"):
            assert isinstance(map_output[field], list), f"{field} deve essere una lista"

    def test_responses_is_list(self, map_output):
        assert isinstance(map_output["responses"], list), "responses deve essere una lista"

    def test_responses_have_int_status_code(self, map_output):
        for r in map_output["responses"]:
            assert "status_code" in r, f"response senza status_code: {r}"
            assert isinstance(r["status_code"], int), \
                f"status_code deve essere int, trovato {type(r['status_code'])}"

    def test_responses_have_body_list(self, map_output):
        for r in map_output["responses"]:
            assert "body" in r, f"response senza body: {r}"
            assert isinstance(r["body"], list), f"body deve essere una lista: {r}"

    def test_path_params_extracted(self, map_output):
        """Sample doc has {userId} — at least one path param expected."""
        assert len(map_output["path_params"]) > 0, \
            "path_params vuoto: deve contenere almeno userId"

    def test_201_response_present(self, map_output):
        codes = [r["status_code"] for r in map_output["responses"]]
        assert 201 in codes, f"response 201 attesa, trovati: {codes}"


# ---------------------------------------------------------------------------
# generate_ts_api — structural contract
# ---------------------------------------------------------------------------


class TestGenerateTsApiContract:

    def test_output_is_valid_json(self, map_output):
        raw = generate_ts_api.func(contract_json=json.dumps(map_output, ensure_ascii=False))
        parsed = json.loads(raw)
        assert isinstance(parsed, dict), "output deve essere un oggetto JSON"

    def test_required_fields_present(self, ts_output):
        required = {"entity_name", "types_file", "api_file"}
        missing = required - ts_output.keys()
        assert not missing, f"campi mancanti: {missing}"

    def test_entity_name_is_pascal_case(self, ts_output):
        name = ts_output["entity_name"]
        assert isinstance(name, str) and name.strip(), "entity_name non deve essere vuoto"
        assert name[0].isupper(), f"entity_name deve iniziare con maiuscola: {name}"

    def test_types_file_is_non_empty(self, ts_output):
        assert isinstance(ts_output["types_file"], str)
        assert ts_output["types_file"].strip(), "types_file non deve essere vuoto"

    def test_api_file_is_non_empty(self, ts_output):
        assert isinstance(ts_output["api_file"], str)
        assert ts_output["api_file"].strip(), "api_file non deve essere vuoto"

    def test_types_file_contains_interface(self, ts_output):
        assert "interface" in ts_output["types_file"], \
            "types_file deve contenere almeno un'interface TypeScript"

    def test_api_file_uses_axios_client(self, ts_output):
        assert "apiClient" in ts_output["api_file"], \
            "api_file deve usare apiClient (axios), non fetch"

    def test_api_file_no_fetch(self, ts_output):
        assert "fetch" not in ts_output["api_file"], \
            "api_file NON deve usare fetch"

    def test_api_file_has_error_handling(self, ts_output):
        assert "handleAxiosError" in ts_output["api_file"], \
            "api_file deve chiamare handleAxiosError"


# ---------------------------------------------------------------------------
# create_file_ts_api — structural + filesystem contract  (deterministico)
# ---------------------------------------------------------------------------

# Sample contract that matches GenerateTsApiResponse shape (no LLM needed)
_SAMPLE_TS_CONTRACT = {
    "entity_name": "_TestOrder",
    "types_file": "export interface _TestOrderRequestDTO {}\nexport interface _TestOrderResponseDTO {}",
    "api_file": (
        "import { apiClient } from '@/api/client/axios';\n"
        "import { handleAxiosError } from '@/api/client/errors';\n"
        "export const use_TestOrderAPI = () => {};"
    ),
}

# Path where the tool writes: src/assets/Api/{entity_name}/
_API_OUTPUT_DIR = (
    __import__("pathlib").Path(__file__).parent.parent
    / "src" / "assets" / "Api" / _SAMPLE_TS_CONTRACT["entity_name"]
)


@pytest.fixture(scope="module")
def create_ts_output():
    """Calls create_file_ts_api once and yields the parsed output. Cleans up after the module."""
    raw = create_file_ts_api.func(contract_json=json.dumps(_SAMPLE_TS_CONTRACT))
    yield json.loads(raw)
    if _API_OUTPUT_DIR.exists():
        shutil.rmtree(_API_OUTPUT_DIR)


class TestCreateFileTsApiContract:

    def test_output_is_valid_json(self):
        raw = create_file_ts_api.func(contract_json=json.dumps(_SAMPLE_TS_CONTRACT))
        assert isinstance(json.loads(raw), dict), "output deve essere un oggetto JSON"

    def test_output_has_required_fields(self, create_ts_output):
        assert "types_file" in create_ts_output
        assert "api_file" in create_ts_output

    def test_types_file_created_on_disk(self, create_ts_output):
        from pathlib import Path
        assert Path(create_ts_output["types_file"]).exists(), \
            f"types_file non trovato su disco: {create_ts_output['types_file']}"

    def test_api_file_created_on_disk(self, create_ts_output):
        from pathlib import Path
        assert Path(create_ts_output["api_file"]).exists(), \
            f"api_file non trovato su disco: {create_ts_output['api_file']}"

    def test_types_file_content_matches(self, create_ts_output):
        from pathlib import Path
        content = Path(create_ts_output["types_file"]).read_text(encoding="utf-8")
        assert content == _SAMPLE_TS_CONTRACT["types_file"], \
            "contenuto di types_file non corrisponde all'input"

    def test_api_file_content_matches(self, create_ts_output):
        from pathlib import Path
        content = Path(create_ts_output["api_file"]).read_text(encoding="utf-8")
        assert content == _SAMPLE_TS_CONTRACT["api_file"], \
            "contenuto di api_file non corrisponde all'input"

    def test_files_under_entity_subdirectory(self, create_ts_output):
        entity = _SAMPLE_TS_CONTRACT["entity_name"]
        assert entity in create_ts_output["types_file"], \
            "types_file deve trovarsi in una sottocartella col nome dell'entità"
        assert entity in create_ts_output["api_file"], \
            "api_file deve trovarsi in una sottocartella col nome dell'entità"

    def test_types_file_extension(self, create_ts_output):
        assert create_ts_output["types_file"].endswith(".types.ts"), \
            "types_file deve avere estensione .types.ts"

    def test_api_file_extension(self, create_ts_output):
        assert create_ts_output["api_file"].endswith(".ts"), \
            "api_file deve avere estensione .ts"
