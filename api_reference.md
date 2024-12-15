# API Reference

## Endpoints

### 1. `GET /get-basic-user-data/`
Fetches basic user data (username, avatar URL, and user ID) of the currently authenticated user.

**Request**:
- Method: `GET`

**Response**:
- **200 OK**: If the user is authenticated and has an active session, the response includes their username, avatar URL, and user ID.
- **Empty JSON Object**: If the user is not authenticated or their session has expired.

**Response Example**:
```json
{
  "username": "john_doe",
  "avatar_url": "https://example.com/avatar.jpg",
  "user_id": "123456789"
}
```

**Behavior**:
- If the session does not contain an `access_token`, an empty JSON object (`{}`) is returned.
- If authenticated, the endpoint retrieves the `username`, `avatar_url`, and `user_id` from the session and returns them in the response.

