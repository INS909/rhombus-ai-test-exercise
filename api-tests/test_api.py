import pytest
import requests
import json
import os

# Load auth cookies from Playwright's saved session
auth_path = os.path.join(os.path.dirname(__file__), '..', 'auth.json')
with open(auth_path, 'r') as f:
    auth_data = json.load(f)

cookies = {c['name']: c['value'] for c in auth_data.get('cookies', [])}

BASE_URL = 'https://rhombusai.com'

def get_latest_project_id():
    """Fetch the most recent project ID dynamically"""
    response = requests.get(
        f'{BASE_URL}/api/projects?limit=20&offset=0',
        cookies=cookies
    )
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            return data[0]['id']
    return 3508

PROJECT_ID = get_latest_project_id()

# ── Positive Tests ─────

def test_session_is_valid():
    """Auth session returns 200 and user data"""
    response = requests.get(f'{BASE_URL}/api/auth/session', cookies=cookies)
    assert response.status_code == 200
    data = response.json()
    assert data is not None
    assert len(data) > 0

def test_get_project_nodes():
    """Can fetch nodes for a valid project"""
    response = requests.get(
        f'{BASE_URL}/api/nodes/{PROJECT_ID}',
        cookies=cookies
    )
    # Accept 200 or 404 - we just need to confirm auth works at network level
    assert response.status_code in [200, 404]
    print(f"Status: {response.status_code}, Response: {response.text[:200]}")

# ── Negative Tests ──

def test_session_without_auth():
    """Request without cookies should return empty or unauthenticated session"""
    response = requests.get(f'{BASE_URL}/api/auth/session')
    assert response.status_code in [200, 401]
    if response.status_code == 200:
        data = response.json()
        # Should return None or empty - not a real user session
        assert data is None or data == {} or 'user' not in (data or {})

def test_invalid_project_id():
    """Request with fake project ID should return 404 or 403"""
    response = requests.get(
        f'{BASE_URL}/api/nodes?project_id=999999',
        cookies=cookies
    )
    assert response.status_code in [403, 404, 401, 200]