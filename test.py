import pytest
import uvicorn
import requests

def test_server():
    requests.get("http://127.0.0.1:8000/sayhello")
    print("server started")

@pytest.mark.parametrize(
    "input",
    [{"outlook":"sunny", "temperature":"mild","humidity":"normal","wind":"weak"},
    {"outlook":"sunny","temperature":"hot","humidity":"normal","wind":"weak"}]
)
def test_true(input):
    res = requests.post("http://127.0.0.1:8000/playability",json=input)
    assert(res.json()['playability'])