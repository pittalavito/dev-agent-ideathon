# Guardare il file readme.ipynb per settare l'ambiente e avviare l'app

# Staccare da develop per fare le prove

## Documentazione tecnica breve

### Scopo attuale

L'app espone una UI minima in Streamlit per testare un solo caso d'uso: prendere in input una documentazione testuale di API REST e passarla a un agente che la converte in un contratto strutturato.

### Flusso applicativo

1. L'entrypoint e' `src/main.py`.
2. All'avvio vengono inizializzati logging, client LLM e istanza dell'agente `DevAgent`.
3. La UI definita in `src/ui/app.py` mostra:
	- titolo e testo descrittivo
	- una `text_area` per incollare documentazione API REST
	- un pulsante `Run`
4. Al click del pulsante, se il campo non e' vuoto, la UI invoca `run_dev_agent(api_doc)`.
5. `run_dev_agent()` esegue l'agente e restituisce al massimo i primi 2500 caratteri della risposta.

### Componenti attivi

- `src/ui/app.py`: pagina Streamlit singola.
- `src/agent/devagent.py`: crea e mantiene un agente singleton `DevAgent`.
- `src/tool/tool.py`: registra i tool disponibili all'agente.
- `src/tool/impl/map_api_rest.py`: implementazione concreta del mapping della documentazione API.

### Configurazione corrente dell'agente

- Nome agente: `DevAgent`
- Tool effettivamente abilitato: `map_api_rest`
- `max_steps=2`
- `terminate_on_text=True`
- Prompt di sistema orientato a mapping di documentazione REST verso `ApiRestContract`

### Note sullo stato attuale

- Le funzioni `heuristic_hello_world` e `llm_hello_world` sono presenti nel codice ma non sono esposte nella UI corrente.
- La UI non gestisce cronologia, stato conversazionale, validazione avanzata dell'input o gestione esplicita degli errori..
- L'app e' oggi un prototipo focalizzato sul test rapido del tool di mapping API.