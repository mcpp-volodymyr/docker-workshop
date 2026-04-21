import importlib.util
import os
import sys
from pathlib import Path


def load_app_with_test_db(tmp_path: Path):
    db_path = tmp_path / "test_poll.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"

    app_file = Path(__file__).resolve().parents[1] / "app.py"

    module_name = "workshop_app_under_test"
    if module_name in sys.modules:
        del sys.modules[module_name]

    spec = importlib.util.spec_from_file_location(module_name, app_file)
    app_module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = app_module
    spec.loader.exec_module(app_module)

    return app_module


def test_index_page_loads(tmp_path):
    app_module = load_app_with_test_db(tmp_path)
    client = app_module.app.test_client()

    response = client.get("/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Never used it" in html
    assert "Fairly comfortable with it" in html


def test_valid_vote_redirects_to_results(tmp_path):
    app_module = load_app_with_test_db(tmp_path)
    client = app_module.app.test_client()

    response = client.post("/vote", data={"option": "Used it a little"})

    assert response.status_code == 302
    assert "/results" in response.headers["Location"]


def test_invalid_vote_returns_400(tmp_path):
    app_module = load_app_with_test_db(tmp_path)
    client = app_module.app.test_client()

    response = client.post("/vote", data={"option": "Totally invalid option"})

    assert response.status_code == 400
    assert "Invalid option" in response.get_data(as_text=True)


def test_results_page_shows_recorded_vote(tmp_path):
    app_module = load_app_with_test_db(tmp_path)
    client = app_module.app.test_client()

    client.post("/vote", data={"option": "Heard of it, but never used it"})
    response = client.get("/results")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "How much experience do you have with Docker?" in html
    assert "Total votes: 1" in html
    assert "Heard of it, but never used it — 1 vote(s) — 100.0%" in html
