# python -m pytest -v

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# CALCULATOR STRESS TESTS

def test_calculator_basic():
    r = client.post("/agent/query", json={"prompt": "What is 10 plus 5"})
    assert r.json()["response"]["result"] == 15


def test_calculator_nested():
    r = client.post("/agent/query", json={"prompt": "What is (2 plus 3) times (4 plus 6)"})
    assert r.json()["response"]["result"] == 50


def test_calculator_deep_nested():
    r = client.post("/agent/query", json={"prompt": "What is ((2 plus 3) times (4 plus 6)) minus 10"})
    assert r.json()["response"]["result"] == 40


def test_calculator_large_numbers():
    r = client.post("/agent/query", json={"prompt": "What is 100000 times 3000"})
    assert r.json()["response"]["result"] == 300000000


def test_calculator_spacing():
    r = client.post("/agent/query", json={"prompt": "What is    5    plus    5"})
    assert r.json()["response"]["result"] == 10


def test_calculator_invalid_expression():
    r = client.post("/agent/query", json={"prompt": "What is five plus six"})
    assert "error" in r.json()["response"]


# MEMORY STRESS TESTS

def test_memory_multiple_saves():
    client.post("/agent/query", json={"prompt": "Remember my hometown is Lucknow"})
    client.post("/agent/query", json={"prompt": "Remember my favorite color is blue"})
    client.post("/agent/query", json={"prompt": "Remember my cat's name is Fluffy"})

    r1 = client.post("/agent/query", json={"prompt": "Recall my hometown"})
    r2 = client.post("/agent/query", json={"prompt": "What is my favorite color?"})
    r3 = client.post("/agent/query", json={"prompt": "Recall my cat's name"})

    assert r1.json()["response"]["value"] == "lucknow"
    assert r2.json()["response"]["value"] == "blue"
    assert r3.json()["response"]["value"] == "fluffy"


def test_memory_overwrite():
    client.post("/agent/query", json={"prompt": "Remember my hometown is Delhi"})
    r = client.post("/agent/query", json={"prompt": "Recall my hometown"})

    assert r.json()["response"]["value"] == "delhi"


def test_memory_synonym_variations():
    client.post("/agent/query", json={"prompt": "Remember my hometown is Mumbai"})

    r1 = client.post("/agent/query", json={"prompt": "Recall my place"})
    r2 = client.post("/agent/query", json={"prompt": "What is my city?"})

    assert r1.json()["response"]["value"] == "mumbai"
    assert r2.json()["response"]["value"] == "mumbai"


def test_memory_fuzzy_typo_heavy():
    client.post("/agent/query", json={"prompt": "Remember my hometown is Pune"})

    r = client.post("/agent/query", json={"prompt": "Recall my hometowwn"})
    assert r.json()["response"]["value"] == "pune"


def test_memory_unknown_key():
    r = client.post("/agent/query", json={"prompt": "Recall my salary"})
    assert "error" in r.json()["response"]


# ROUTER EDGE CASES TESTS 

def test_case_insensitivity():
    client.post("/agent/query", json={"prompt": "Remember My Hometown Is Jaipur"})

    r = client.post("/agent/query", json={"prompt": "RECALL MY HOMETOWN"})
    assert r.json()["response"]["value"] == "jaipur"


def test_weird_spacing_memory():
    client.post("/agent/query", json={"prompt": "Remember    my    hometown   is   Agra"})

    r = client.post("/agent/query", json={"prompt": "Recall my hometown"})
    assert r.json()["response"]["value"] == "agra"


def test_unknown_prompt():
    r = client.post("/agent/query", json={"prompt": "Tell me a joke"})
    assert "error" in r.json()


# LOAD STYLE TEST 

def test_many_requests_loop():
    for i in range(20):
        r = client.post("/agent/query", json={"prompt": f"What is {i} plus {i}"})
        assert r.json()["response"]["result"] == i + i

