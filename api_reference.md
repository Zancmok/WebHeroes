# API Reference

## Index
- [WebSocket Events](#websocket-events)  
  - [`connect`](#1-websocket-event-connect)  
  - [`disconnect`](#2-websocket-event-disconnect)
  - [get-lobby-data](#3-websocket-event-get-lobby-data)
- [GET Methods](#get-methods)  
  - [`GET /`](#1-get-)  
  - [`GET /modding-documentation/`](#2-get-modding-documentation)  
  - [`GET /oauth/`](#3-get-oauth)  
  - [`GET /online-lobbies/`](#4-get-online-lobbies)  
- [POST Methods](#post-methods)  

---

## WebSocket Events

### 1. `WebSocket Event: connect`
Handles the WebSocket connection event.

#### **Behavior**
- If the user is not authenticated (`access_token` missing from session), the connection is rejected.
- If the user is authenticated but not found in `UserManager`, a new `User` instance is created.
- Updates the user's presence status to `online`.
- Automatically joins the user to the default lobby room.

#### **Response**
- **Connection accepted**: If authentication is valid.
- **Connection rejected (False)**: If the user is not authenticated.

---

### 2. `WebSocket Event: disconnect`
Handles the WebSocket disconnection event.

#### **Behavior**
- Updates the user's presence status to `offline` if they exist in `UserManager`.
- Removes the user from the default lobby room.

---

### 3. WebSocket Event: get-lobby-data
Fetches and emits the current lobby data, including the details of the user requesting it,
the list of users in the current lobby, and other available lobbies with their members.

#### **Behavior**
- If the session does not contain a valid `access_token`, an empty lobby data object is emitted.
- Otherwise, the function retrieves the user details for the current user (`name`, `avatar_url`, `user_id`, and `presence_status`), and collects the necessary data for users in the current lobby and other lobbies.
- Emits the collected data, which includes:
  - The current user's details.
  - The details of other users in the same lobby.
  - A list of other available lobbies and their members.

#### **Response**
- **Emits** the "get-lobby-data" event with a JSON object containing:
  - `self`: The current user's details.
  - `users`: A list of users in the current lobby.
  - `lobbies`: A list of other lobbies with their members' details.

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
