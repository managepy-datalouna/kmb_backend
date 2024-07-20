## Get started
1. Copy backend and frontend dirs.
2. Run the following:
```shell
git clone git@github.com:managepy-datalouna/kmb_backend.git
git clone git@github.com:managepy-datalouna/kmb_frontend.git

sqlite3 base.db < kmb_backend/schema.sql

cd kmb_backend
poetry env use python3.10
poetry install
poetry run uvicorn main:app --reload
```
3. Project will be available on `http://localhost:8000/static/index.html`
