# Copilot instructions for `pyetrade`

## Build, test, and lint commands

Use the existing Makefile and tox/pre-commit setup instead of inventing new workflows.

- Install runtime deps: `make init`
- Install dev tooling and git hooks: `make devel`
- Run the full test suite: `make test` or `tox`
- Run one test: `pytest tests/test_accounts.py::TestETradeAccounts::test_list_accounts -q`
- Run lint/format/import checks: `make analysis`
- Build docs: `make -C docs/ html`
- Build a source distribution: `make dist`

## High-level architecture

The package is a thin wrapper around E*TRADE REST APIs, organized by API domain:

- `pyetrade.authorization` handles OAuth setup and token renewal/revocation.
- `pyetrade.accounts`, `alerts`, `market`, and `order` each expose one main client class for a specific E*TRADE API area.
- `pyetrade.__init__` re-exports those client classes as the public import surface (`pyetrade.ETradeAccounts`, `pyetrade.ETradeOrder`, etc.), so public API changes should stay aligned there.

Each client builds an `OAuth1Session` in `__init__`, chooses sandbox vs production by toggling `dev`, and constructs E*TRADE endpoint URLs from a module-specific `base_url`. Most methods are direct request wrappers: build URL and params/payload, call the session, `raise_for_status()`, then return parsed XML or JSON.

`pyetrade.order` is the only module with substantial internal orchestration. It centralizes request parsing (`get_request_result`), payload construction (`build_order_payload`), preview/place flows, and custom exceptions. `place_equity_order()` and changed-order flows automatically preview first when a `previewId` is not supplied, because the downstream E*TRADE flow expects it.

Documentation is Sphinx-based under `docs/`, and `docs/conf.py` imports the package directly for autodoc. Changes to exported classes, module names, or docstrings can affect the docs build even when runtime code is untouched.

## Key conventions

- Sandbox is the default almost everywhere: constructors use `dev=True` unless a caller explicitly opts into production.
- Response format is usually XML by default. Methods switch to JSON by appending `.json` to the endpoint and otherwise parse XML with `xmltodict`. Keep that dual-format pattern consistent when adding endpoints.
- Order code treats API errors differently from the other modules: `get_request_result()` inspects parsed responses for an `"Error"` payload and raises `RequestException` instead of returning the error body.
- Order payload generation is centralized in `build_order_payload()`. Reuse it instead of open-coding request bodies, especially for preview/place parity and option order fields.
- Dev dependencies and exported requirement files are coupled through pre-commit: `.pre-commit-config.yaml` runs Poetry export hooks that regenerate `requirements.txt` and `requirements_dev.txt` from `pyproject.toml`. If dependency definitions change, update `pyproject.toml` and let the existing export workflow refresh the requirements files.
- Tests use `unittest` with `@patch("pyetrade.<module>.OAuth1Session")` to mock HTTP calls at the module import boundary. They commonly assert exact URLs, params, and payload shapes, so seemingly small request-construction changes often require test updates.
- `tests/` includes XML fixture files for market responses; prefer those existing examples when extending market parsing tests instead of adding ad hoc inline payloads.
