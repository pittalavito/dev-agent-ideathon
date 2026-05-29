# API Generator

# Dev Agent Ideathon

> Setup ambiente: vedi `readme.ipynb`. Lavorare su branch separato da `develop`.

## Avvio

```bash
python -m streamlit run src/main.py
```

## Stack

- **UI**: Streamlit (`src/ui/app.py` + `src/ui/logs_page.py`)
- **Agent**: `DevAgent` — OpenAI `gpt-4o`, `max_steps=2`, tool: `map_api_rest`
- **Client**: `_FAST_CLIENT` (OpenAI) / `_LOCAL_CLIENT` (Ollama `gemma4` locale, non ancora usato)
- **Observability**: log di agent run e tool call persistiti in JSON, visibili nella UI

## Struttura `src/`

```
main.py
agent/devagent.py        # singleton DevAgent
client/client.py         # init client LLM
tool/tool.py             # map_api_rest tool
tool/model.py            # MapApiRestToolResponse (Pydantic)
ui/app.py                # pagina principale
ui/logs_page.py          # tab Agent Runs / Tool Calls
observability/           # decoratori observe_*, pricing, modelli
```
