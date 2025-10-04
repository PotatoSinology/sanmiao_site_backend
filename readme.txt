python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
gunicorn -b 0.0.0.0:$PORT main:app -k uvicorn.workers.UvicornWorker -w 2
