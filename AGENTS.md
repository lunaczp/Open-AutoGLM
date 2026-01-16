# Repository Guidelines

## Project Structure & Module Organization
- Core CLI entrypoint: `main.py` for Android (`adb`), HarmonyOS (`hdc`), or iOS (`wda`).
- `phone_agent/`: transport layers (`adb/`, `hdc/`, `xctest/`), action planners (`actions/`), model wrapper (`model/`), and prompts/app catalogs (`config/`).
- `scripts/`: deployment checks with sample messages. `examples/`: quick usage demos.
- Docs/assets: `resources/`, `docs/ios_setup/`; packaging in `setup.py`, `phone_agent.egg-info`.

## Build, Test, and Development Commands
- Install: `pip install -r requirements.txt && pip install -e .` (Python 3.10+).
- Lint/format: `pre-commit run --all-files` (`ruff`, `ruff-format`, `typos`, `pymarkdown`).
- Health check: `python scripts/check_deployment_en.py --base-url http://localhost:8000/v1 --apikey KEY --model autoglm-phone-9b`.
- Run agent: `python main.py --device-type adb --base-url https://open.bigmodel.cn/api/paas/v4 --model autoglm-phone --apikey KEY "打开微信发送消息"` (swap `--device-type hdc`/`ios`).
- Smoke: set `PHONE_AGENT_BASE_URL`, `PHONE_AGENT_MODEL`, `PHONE_AGENT_API_KEY`, `PHONE_AGENT_DEVICE_ID`, then `python examples/basic_usage.py`.

## Coding Style & Naming Conventions
- PEP 8, 4-space indents; snake_case for functions/vars, PascalCase for classes. Add type hints and brief docstrings when logic is non-trivial.
- Reuse existing device abstractions; prefer extension via `config/` and `actions/` over ad-hoc subprocess calls.
- Run `ruff`/`ruff-format` before sending changes; keep prompts/config localized and avoid hardcoded device IDs.
- Markdown should satisfy `pymarkdown`; keep headings ordered and lines concise.

## Testing Guidelines
- No unit-test suite yet; rely on command-level checks. Use deployment scripts for model responses and run `main.py --check` or a short task on a real/emulated device.
- For new features, add a minimal demo under `examples/` or a CLI flag that can be exercised without hardware when possible.
- Capture `main.py` logs and device-tool output (`adb devices`, `hdc list targets`, `idevice_id -l`) when validating connectivity or reporting bugs.

## Commit & Pull Request Guidelines
- Commit messages are short and imperative (e.g., `add context log`, `fix format`); keep scope tight.
- PRs should list purpose, device type + model provider tested, manual checks/commands, and screenshots or log snippets for device-facing changes. Link issues where relevant.
- Ensure `pre-commit` passes and user-facing config changes are reflected in `README.md`/`README_en.md`.

## Security & Configuration Tips
- Do not hardcode API keys or device IDs; use env vars (`PHONE_AGENT_BASE_URL`, `PHONE_AGENT_MODEL`, `PHONE_AGENT_API_KEY`, `PHONE_AGENT_DEVICE_ID`) or CLI flags. Avoid committing credentials in examples.
- Keep sensitive-operation confirmations intact; avoid new defaults that bypass user consent or broaden device access without checks.
