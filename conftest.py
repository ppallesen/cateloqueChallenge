from fastapi.testclient import TestClient
from main import app
from random import random

client = TestClient(app)


def rng_string():
    return str(random())
