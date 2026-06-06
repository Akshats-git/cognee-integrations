# Cognee Memory Plugin for Hermes Agent

Standalone Hermes memory provider backed by Cognee.

This replaces the closed in-tree Hermes PR path. Hermes no longer accepts new
providers under `plugins/memory/`; this integration is shaped as a standalone
plugin that can be installed into `~/.hermes/plugins/cognee` or distributed as a
Python package with the `hermes_agent.plugins` entry point.

## Features

- Stores each completed Hermes turn in Cognee session memory.
- Uses `cognee_recall` for session-first recall with graph fallback.
- Exposes `cognee_remember` for durable graph memory.
- Exposes `cognee_forget` for deletion requests.
- Runs `cognee.improve()` at Hermes session end to bridge session memory into the graph.
- Mirrors explicit Hermes memory writes through `on_memory_write`.
- Supports local embedded Cognee and remote Cognee service mode.

## Install For Local Hermes Development

From this repository:

```bash
mkdir -p ~/.hermes/plugins/cognee
cp -R integrations/hermes-agent/. ~/.hermes/plugins/cognee/
hermes memory setup
```

Select `cognee` in the memory provider picker.

## Install From Pip

```bash
pip install cognee-integration-hermes-agent
hermes memory setup
```

The package exposes:

```toml
[project.entry-points."hermes_agent.plugins"]
cognee = "cognee_integration_hermes"
```

## Configuration

The setup wizard writes non-secret settings to `$HERMES_HOME/cognee.json` and
secrets to `$HERMES_HOME/.env`.

Local embedded mode:

```bash
LLM_API_KEY=sk-...
LLM_MODEL=gpt-4o-mini
COGNEE_DATASET=hermes
```

Remote service mode:

```bash
COGNEE_SERVICE_URL=https://your-cognee-service.example
COGNEE_API_KEY=...
COGNEE_DATASET=hermes
```

Optional settings:

| Setting | Env var | Default |
| --- | --- | --- |
| `dataset` | `COGNEE_DATASET` | `hermes` |
| `top_k` | `COGNEE_TOP_K` | `5` |
| `auto_route` | `COGNEE_AUTO_ROUTE` | `true` |
| `improve_on_end` | `COGNEE_IMPROVE_ON_END` | `true` |
| `session_prefix` | `COGNEE_SESSION_PREFIX` | `hermes` |
| `service_url` | `COGNEE_SERVICE_URL` | empty |
| `data_root` | `COGNEE_DATA_ROOT` | `$HERMES_HOME/cognee/data` |
| `system_root` | `COGNEE_SYSTEM_ROOT` | `$HERMES_HOME/cognee/system` |

## Hermes Commands

When Cognee is the active memory provider:

```bash
hermes cognee status
hermes cognee setup
hermes cognee config
hermes cognee install
```

## Development

```bash
cd integrations/hermes-agent
uv sync --dev
uv run pytest -q
uv run ruff check .
```

