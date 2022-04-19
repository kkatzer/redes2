import socket
from enum import Enum
import time
import requests
import asyncio


class Place(Enum):
    ANTARCTICA = "antarctica"
    DEATHVALLEY = "deathvalley"
    SAARADESERT = "saaradesert"


CACHE_TABLE = {
    Place.ANTARCTICA: {"temperature": 0.0, "updated_at": 0.0},
    Place.DEATHVALLEY: {"temperature": 0.0, "updated_at": 0.0},
    Place.SAARADESERT: {"temperature": 0.0, "updated_at": 0.0}
}


async def request_temperature(place):
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, requests.get, "http://127.0.0.1:8000/{}".format(place.value))
    response = await future
    return response.json()


async def update_cache(place):
    if CACHE_TABLE[place]["updated_at"] < time.time() - 30:
        CACHE_TABLE[place]["temperature"] = (await request_temperature(place))["temperature"]
        CACHE_TABLE[place]["updated_at"] = time.time()


async def request_cache(place):
    await update_cache(place)
    return CACHE_TABLE[place]["temperature"]


HOST = "127.0.0.1"
PORT = 65432


async def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        while True:
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024).decode("utf-8")
                temperature = await request_cache(Place[data])
                conn.sendall(str(temperature).encode())

if __name__ == "__main__":
    asyncio.run(main())