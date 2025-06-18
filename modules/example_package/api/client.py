"""
API client for making HTTP requests.
"""

from typing import Optional, List, Any, Dict
import requests
from .models import User, Post, Comment, UserCreate, PostCreate

class APIError(Exception):
    """Custom exception for API errors."""
    pass

class APIClient:
    """Client for interacting with the API."""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Initialize the API client.
        
        Args:
            base_url: The base URL of the API
            api_key: Optional API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({'Authorization': f'Bearer {api_key}'})
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            params: Query parameters
            json: JSON body data
            
        Returns:
            Response data as dictionary
            
        Raises:
            APIError: If the request fails
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"API request failed: {str(e)}") from e
    
    # User endpoints
    def get_user(self, user_id: int) -> User:
        """Get a user by ID."""
        data = self._make_request('GET', f'/users/{user_id}')
        return User(**data)
    
    def create_user(self, user: UserCreate) -> User:
        """Create a new user."""
        data = self._make_request('POST', '/users', json=user.model_dump())
        return User(**data)
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> User:
        """Update a user."""
        data = self._make_request('PUT', f'/users/{user_id}', json=user_data)
        return User(**data)
    
    def delete_user(self, user_id: int) -> None:
        """Delete a user."""
        self._make_request('DELETE', f'/users/{user_id}')
    
    # Post endpoints
    def get_post(self, post_id: int) -> Post:
        """Get a post by ID."""
        data = self._make_request('GET', f'/posts/{post_id}')
        return Post(**data)
    
    def create_post(self, post: PostCreate, author_id: int) -> Post:
        """Create a new post."""
        data = post.model_dump()
        data['author_id'] = author_id
        response = self._make_request('POST', '/posts', json=data)
        return Post(**response)
    
    def get_user_posts(self, user_id: int) -> List[Post]:
        """Get all posts by a user."""
        data = self._make_request('GET', f'/users/{user_id}/posts')
        return [Post(**post_data) for post_data in data]
    
    def search_posts(
        self,
        query: str,
        tag: Optional[str] = None,
        limit: int = 10
    ) -> List[Post]:
        """Search for posts."""
        params = {'q': query, 'limit': limit}
        if tag:
            params['tag'] = tag
        
        data = self._make_request('GET', '/posts/search', params=params)
        return [Post(**post_data) for post_data in data]
    
    # Comment endpoints
    def get_post_comments(self, post_id: int) -> List[Comment]:
        """Get all comments for a post."""
        data = self._make_request('GET', f'/posts/{post_id}/comments')
        return [Comment(**comment_data) for comment_data in data]
    
    def add_comment(
        self,
        post_id: int,
        author_id: int,
        content: str
    ) -> Comment:
        """Add a comment to a post."""
        data = {
            'post_id': post_id,
            'author_id': author_id,
            'content': content
        }
        response = self._make_request('POST', f'/posts/{post_id}/comments', json=data)
        return Comment(**response) 