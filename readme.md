# ohtuvarasto26

[![main](https://github.com/oskari6/ohtuvarasto/actions/workflows/main.yml/badge.svg)

[![codecov](https://codecov.io/github/oskari6/ohtuvarasto/graph/badge.svg?token=E1EXWB8MKO)](https://codecov.io/github/oskari6/ohtuvarasto)

https://github.com/oskari6/ohtuvarasto/actions

coverage run --branch -m pytest; coverage html

## Warehouse web interface

Run the web app with `uv run python src/web.py` and open http://127.0.0.1:5001.
Storages are kept in memory while the app is running.

Run the route tests with `uv run pytest` and the end-to-end Robot Framework
checks with `uv run robot src/tests/warehouse.robot`.
