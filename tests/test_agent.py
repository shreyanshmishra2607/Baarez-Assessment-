from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_calculator_basic():
    response = client.post(
        "/agent/query",
        json={"prompt": "What is 10 plus 5"}
    )

    data = response.json()

    assert response.status_code == 200
    assert data["chosen_tool"] == "calculator"
    assert data["response"]["result"] == 15


def test_calculator_complex():
    response = client.post(
        "/agent/query",
        json={"prompt": "What is 5 times (10 plus 2)"}
    )

    data = response.json()

    assert data["chosen_tool"] == "calculator"
    assert data["response"]["result"] == 60


def test_memory_save():
    response = client.post(
        "/agent/query",
        json={"prompt": "Remember my hometown is Lucknow"}
    )

    data = response.json()

    assert data["chosen_tool"] == "memory_save"
    assert data["response"]["value"] == "lucknow"


def test_memory_read_exact():
    client.post(
        "/agent/query",
        json={"prompt": "Remember my hometown is Lucknow"}
    )

    response = client.post(
        "/agent/query",
        json={"prompt": "Recall my hometown"}
    )

    data = response.json()

    assert data["chosen_tool"] == "memory_read"
    assert data["response"]["value"] == "lucknow"



def test_memory_read_synonym():
    response = client.post(
        "/agent/query",
        json={"prompt": "What is my city?"}
    )

    data = response.json()

    assert data["chosen_tool"] == "memory_read"
    assert data["response"]["value"] == "lucknow"


def test_memory_read_exact():
    client.post(
        "/agent/query",
        json={"prompt": "Remember my hometown is Lucknow"}
    )

    response = client.post(
        "/agent/query",
        json={"prompt": "Recall my hometown"}
    )

    data = response.json()

    assert data["chosen_tool"] == "memory_read"
    assert data["response"]["value"] == "lucknow"



def test_unknown_prompt():
    response = client.post(
        "/agent/query",
        json={"prompt": "Tell me a joke"}
    )

    data = response.json()

    assert "error" in data
