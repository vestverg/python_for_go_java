"""
Tests for the API client module.
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from example_package.api import (
    APIClient,
    APIError,
    User,
    Post,
    Comment,
    UserCreate,
    PostCreate
)

# Test data
TEST_USER_DATA = {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "full_name": "Test User",
    "created_at": datetime.now().isoformat(),
    "is_active": True
}

TEST_POST_DATA = {
    "id": 1,
    "title": "Test Post",
    "content": "Test content",
    "author_id": 1,
    "tags": ["test", "python"],
    "created_at": datetime.now().isoformat(),
    "updated_at": None
}

@pytest.fixture
def api_client():
    """Create an API client for testing."""
    return APIClient("https://api.example.com", "test-api-key")

@pytest.fixture
def mock_response():
    """Create a mock response."""
    mock = Mock()
    mock.json = Mock(return_value={})
    mock.raise_for_status = Mock()
    return mock

def test_api_client_initialization():
    """Test API client initialization."""
    client = APIClient("https://api.example.com", "test-api-key")
    assert client.base_url == "https://api.example.com"
    assert client.api_key == "test-api-key"
    assert "Authorization" in client.session.headers
    assert client.session.headers["Authorization"] == "Bearer test-api-key"

@patch("requests.Session.request")
def test_get_user(mock_request, api_client, mock_response):
    """Test getting a user."""
    mock_response.json.return_value = TEST_USER_DATA
    mock_request.return_value = mock_response
    
    user = api_client.get_user(1)
    
    assert isinstance(user, User)
    assert user.id == TEST_USER_DATA["id"]
    assert user.username == TEST_USER_DATA["username"]
    assert user.email == TEST_USER_DATA["email"]
    
    mock_request.assert_called_once_with(
        method="GET",
        url="https://api.example.com/users/1",
        params=None,
        json=None
    )

@patch("requests.Session.request")
def test_create_user(mock_request, api_client, mock_response):
    """Test creating a user."""
    mock_response.json.return_value = TEST_USER_DATA
    mock_request.return_value = mock_response
    
    user_create = UserCreate(
        username="testuser",
        email="test@example.com",
        password="password123"
    )
    
    user = api_client.create_user(user_create)
    
    assert isinstance(user, User)
    assert user.username == TEST_USER_DATA["username"]
    
    mock_request.assert_called_once()
    assert mock_request.call_args[1]["method"] == "POST"
    assert mock_request.call_args[1]["url"] == "https://api.example.com/users"

@patch("requests.Session.request")
def test_get_post(mock_request, api_client, mock_response):
    """Test getting a post."""
    mock_response.json.return_value = TEST_POST_DATA
    mock_request.return_value = mock_response
    
    post = api_client.get_post(1)
    
    assert isinstance(post, Post)
    assert post.id == TEST_POST_DATA["id"]
    assert post.title == TEST_POST_DATA["title"]
    assert post.content == TEST_POST_DATA["content"]
    
    mock_request.assert_called_once_with(
        method="GET",
        url="https://api.example.com/posts/1",
        params=None,
        json=None
    )

@patch("requests.Session.request")
def test_create_post(mock_request, api_client, mock_response):
    """Test creating a post."""
    mock_response.json.return_value = TEST_POST_DATA
    mock_request.return_value = mock_response
    
    post_create = PostCreate(
        title="Test Post",
        content="Test content",
        tags=["test", "python"]
    )
    
    post = api_client.create_post(post_create, author_id=1)
    
    assert isinstance(post, Post)
    assert post.title == TEST_POST_DATA["title"]
    assert post.author_id == TEST_POST_DATA["author_id"]
    
    mock_request.assert_called_once()
    assert mock_request.call_args[1]["method"] == "POST"
    assert mock_request.call_args[1]["url"] == "https://api.example.com/posts"

@patch("requests.Session.request")
def test_api_error(mock_request, api_client):
    """Test API error handling."""
    mock_request.side_effect = Exception("API Error")
    
    with pytest.raises(APIError) as exc_info:
        api_client.get_user(1)
    
    assert "API request failed" in str(exc_info.value)

@patch("requests.Session.request")
def test_search_posts(mock_request, api_client, mock_response):
    """Test searching posts."""
    mock_response.json.return_value = [TEST_POST_DATA]
    mock_request.return_value = mock_response
    
    posts = api_client.search_posts("test", tag="python", limit=10)
    
    assert len(posts) == 1
    assert isinstance(posts[0], Post)
    assert posts[0].title == TEST_POST_DATA["title"]
    
    mock_request.assert_called_once()
    assert mock_request.call_args[1]["params"] == {
        "q": "test",
        "tag": "python",
        "limit": 10
    } 