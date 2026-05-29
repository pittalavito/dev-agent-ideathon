# API Generator

# Dev Agent Ideathon

> Setup ambiente: vedi `readme.ipynb`. Lavorare su branch separato da `develop`.

## Avvio

```bash
python -m streamlit run src/main.py
```

## Stack

- **UI**: Streamlit (`src/ui/app.py` + `src/ui/logs_page.py`)
- **Agent**: `DevAgent` — OpenAI `gpt-4o`, `max_steps=4`, tool: `map_api_rest`, `generate_ts_api`
- **Client**: `_FAST_CLIENT` (OpenAI) / `_LOCAL_CLIENT` (Ollama `gemma3:4b` locale, non ancora usato)
- **Observability**: log di agent run e tool call persistiti in JSON, visibili nella UI

## Struttura `src/`

```
main.py
agent/devagent.py        # singleton DevAgent
client/client.py         # init client LLM
tool/tool.py             # map_api_rest, generate_ts_api
tool/model.py            # MapApiRestToolResponse, GenerateTsApiResponse (Pydantic)
assets/apiTemplate.ts    # template TypeScript per generate_ts_api
ui/app.py                # pagina principale
ui/logs_page.py          # tab Agent Runs / Tool Calls
observability/           # decoratori observe_*, pricing, modelli
test/                    # contract test dei tool (pytest)
```

## Tool

| Tool | Tipo | Descrizione |
|---|---|---|
| `map_api_rest` | LLM (remote) | Converte documentazione testuale di un'API REST in `MapApiRestToolResponse` (Pydantic JSON) |
| `generate_ts_api` | LLM (remote) | Riceve il contratto JSON e genera `entity.types.ts` + `entity.api.ts` seguendo `apiTemplate.ts` |

## Test

Contract test di integrazione per i tool (chiamate LLM reali, assert sul contratto strutturale):

```bash
pytest test/ -v
```
