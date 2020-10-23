from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from .main import app


# test settings
client = TestClient(app)
assets = Path(__file__).parent / "test_assets"


def test_home():
    assert client.get("/").json() == {"hello": "world"}


@pytest.mark.parametrize("asset_path,expected_response", [
    # valid files
    ("test.gif",  {"safe": True}),
    ("test.jpg", {"safe": True}),
    ("test.jpeg", {"safe": True}),
    ("test.pdf", {"safe": True}),
    ("test.png", {"safe": True}),
    # invalid files
    ("unknown.foo", {"safe": False, "reason": "unrecognized file type"}),
    ("test.tif", {"safe": False, "reason": "invalid file type"}),
    ("eicar-standard-antivirus-test-file-adobe-acrobat-attachment.pdf", {"safe": False, "reason": "clamav"}),
    ("misnamed.jpg", {"safe": False, "reason": "invalid file extension"}),
])
def test_response(asset_path, expected_response):
    response = client.post("/scan/", files={"file": (asset_path, assets.joinpath(asset_path).read_bytes())})
    assert response.status_code == 200
    print(asset_path, response.json())
    assert response.json() == expected_response
