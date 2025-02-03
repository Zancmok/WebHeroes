# API Reference

## Index
- [WebSocket Events](#websocket-events)  
  - [`get-basic-user-data`](#1-websocket-event-get-basic-user-data)  
  - [`connect`](#2-websocket-event-connect)  
  - [`disconnect`](#3-websocket-event-disconnect)  
- [GET Methods](#get-methods)  
  - [`GET /`](#1-get-)  
  - [`GET /modding-documentation/`](#2-get-modding-documentation)  
  - [`GET /oauth/`](#3-get-oauth)  
  - [`GET /online-lobbies/`](#4-get-online-lobbies)  
- [POST Methods](#post-methods)  

---

## WebSocket Events

### 1. `WebSocket Event: get-basic-user-data`
Emits basic user information stored in the session.

#### **Request**
- **Event**: `get-basic-user-data`

#### **Response**
- **200 OK**: If the user is authenticated and has an active session, the response contains:
  - `username`: The user's display name.
  - `avatar_url`: The URL of the user's avatar.
  - `user_id`: The unique identifier of the user.
- **Empty JSON Object (`{}`)**: Returned if the user is not authenticated or their session has expired.

#### **Behavior**
- If the session does not contain an `access_token`, an empty JSON object (`{}`) is emitted.
- If authenticated, the event retrieves the `username`, `avatar_url`, and `user_id` from the session and emits them.

#### **Response Example**
```json
{
  "username": "john_doe",
  "avatar_url": "https://example.com/avatar.jpg",
  "user_id": 123456789
}
```

---

### 2. `WebSocket Event: connect`
Handles the WebSocket connection event.

#### **Request**
- **Event**: `get-basic-user-data`

#### **Behavior**
- If the user is not authenticated (`access_token` missing from session), the connection is rejected.
- If the user is authenticated but not found in `UserManager`, a new `User` instance is created.
- Updates the user's presence status to `online`.
- Automatically joins the user to the default lobby room.

#### **Response**
- **Connection accepted**: If authentication is valid.
- **Connection rejected (False)**: If the user is not authenticated.

---

### 3. `WebSocket Event: disconnect`
Handles the WebSocket disconnection event.

#### **Behavior**
- Updates the user's presence status to `offline` if they exist in `UserManager`.
- Removes the user from the default lobby room.

---

## GET Methods

### 1. `GET /`
Serves the home page.

#### **Request**
- **Method**: `GET`
- **Endpoint**: `/`

#### **Response**
- **200 OK**: Returns the rendered HTML page for the home screen.

---

### 2. `GET /modding-documentation/`
Serves the modding documentation page.

#### **Request**
- **Method**: `GET`
- **Endpoint**: `/modding-documentation/`

#### **Response**
- **200 OK**: Returns the rendered HTML page for the modding documentation.

---

### 3. `GET /oauth/`
Handles Discord OAuth2 authentication.

#### **Request**
- **Method**: `GET`
- **Endpoint**: `/oauth/`
- **Query Parameters**:
  - `code` (string, required): Authorization code from Discord.

#### **Response**
- **302 Found**: Redirects to:
  - `/online-lobbies/` if authentication is successful.
  - `/` if authentication fails.

#### **Behavior**
- Exchanges the authorization code for an access token.
- Retrieves user details from Discord.
- Stores user details (`access_token`, `username`, `avatar_url`, `user_id`) in the session.

---

### 4. `GET /online-lobbies/`
Serves the online lobbies page.

#### **Request**
- **Method**: `GET`
- **Endpoint**: `/online-lobbies/`

#### **Response**
- **200 OK**: If authenticated, returns the rendered HTML page for online lobbies.
- **302 Found**: Redirects to the Discord OAuth2 login page if the user is not authenticated.

---

## POST Methods

_None yet_

---
