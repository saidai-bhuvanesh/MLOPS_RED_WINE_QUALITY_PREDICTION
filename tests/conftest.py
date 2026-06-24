import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Mock USER_DB to have "password" key for tests
@pytest.fixture(autouse=True)
def mock_user_db(monkeypatch):
    """Patch USER_DB to use 'password' instead of 'password_hash' for test compatibility."""
    from mlProject.components import security
    
    # Create test-friendly USER_DB with 'password' key
    test_user_db = {
        "admin": {"password": "admin_password", "role": "Admin"},
        "engineer": {"password": "engineer_password", "role": "Engineer"},
        "viewer": {"password": "viewer_password", "role": "Viewer"}
    }
    
    monkeypatch.setattr(security, "USER_DB", test_user_db)
