import multiprocessing
from time import sleep

import pytest
import requests
import uvicorn


@pytest.fixture(scope="module")
def callback_server():
    process = multiprocessing.Process(
        target=uvicorn.run,
        args=("examples.callback_app:app",),
        kwargs={"host": "localhost", "port": 5001},
        daemon=True,
    )
    process.start()
    for i in range(50):  # 5-second timeout
        sleep(0.1)
        try:
            requests.get("http://localhost:5001")
        except requests.ConnectionError:
            continue
        else:
            break
    else:
        raise TimeoutError("Server did not start in time")

    yield process

    process.terminate()
