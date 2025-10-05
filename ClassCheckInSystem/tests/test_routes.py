from fastapi.testclient import TestClient
from backend.app.main import app

def test_health_endpoint():
    c = TestClient(app)
    r = c.get('/health')
    assert r.status_code == 200


def test_login_requires_form():
    c = TestClient(app)
    r = c.post('/login', data={'username':'x','password':'y'})
    # 可能返回 400 或 200（若库中有用户），这里只做可达性
    assert r.status_code in (200, 400)
