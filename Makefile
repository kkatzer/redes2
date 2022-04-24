pip := pip3
python := python3

install:
	${pip} install fastapi urwid requests uvicorn

api:
	${python} -m uvicorn api:app

server:
	${python} server.py

client:
	${python} client.py

make clear:
	lsof -ti:65432 | xargs kill -9
	lsof -ti:8000 | xargs kill -9