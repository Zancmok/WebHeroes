# API Reference

## Index
- [WebSocket Events](#websocket-events)  
  - [`connect`](#1-websocket-event-connect)  
  - [`disconnect`](#2-websocket-event-disconnect)
- [GET Methods](#get-methods)  
  - [`GET /`](#1-get-)  
  - [`GET /modding-documentation/`](#2-get-modding-documentation)  
  - [`GET /oauth/`](#3-get-oauth)  
  - [`GET /online-lobbies/`](#4-get-online-lobbies)  
- [POST Methods](#post-methods)
- [Response Objects](#response-objects)  
  - [`Empty Response`](#1-empty-response)  
  - [`Success Response`](#2-success-response)  
  - [`Get Lobby Data Response`](#3-get-lobby-data-response)  
  - [`Lobby Update Response`](#4-lobby-update-response)  
- [Response Data Models](#response-data-models)  
  - [`Lobby Model`](#1-lobby-model)  
  - [`User Model`](#2-user-model)  
  - [`New Lobby Update Model`](#3-new-lobby-update-model)  
  - [`New User Update Model`](#4-new-user-update-model)  
  - [`User Left Update Model`](#5-user-left-update-model)  
  - [`User Updated Update Model`](#6-user-updated-update-model)  
- [Enums](#enums)  
  - [`LobbyUpdate`](#1-lobbyupdate)  
  - [`PresenceStatus`](#2-presencestatus)

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

## Response Objects

---

### 1. `Empty Response`
Represents an empty response with no additional data.

#### Object Type: `empty`

#### **Fields**
_None_

#### **Field Explanation**
- This response type indicates that no additional data is included.
- It is used when an API response is required but no further information is necessary.

---

### 2. `Success Response`
Indicates a successful operation.

#### Object Type: `success`

#### **Fields**
_None_

#### **Field Explanation**
- This response type is used to indicate that an operation was successfully executed without additional data.

---

### 3. `Get Lobby Data Response`
Provides data about available lobbies and active users.

#### Object Type: `get-lobby-data-response`

#### **Fields**
- `self`: `UserModel`  
- `users`: `list[UserModel]`  
- `lobbies`: `list[LobbyModel]`  

#### **Field Explanation**
- `self`: The requesting user.  
- `users`: A list of active users in the system.  
- `lobbies`: A list of available lobbies.

---

### 4. `Lobby Update Response`
Represents an update to a lobby, detailing the type of change and its specifics.

#### Object Type: `lobby-update`

#### **Fields**
- `change_type`: `LobbyUpdate`  
- `change`: `NewUserUpdateModel | NewLobbyUpdateModel | UserUpdatedUpdateModel | UserLeftUpdateModel`  

#### **Field Explanation**
- `change_type`: The type of change that occurred, represented as an enumeration from `LobbyUpdate`.  
- `change`: The specific details of the change, which can be one of the following:  
  - `NewUserUpdateModel`  
  - `NewLobbyUpdateModel`  
  - `UserUpdatedUpdateModel`  
  - `UserLeftUpdateModel`  

---

## Response Data Models

### 1. `Lobby Model`

Represents a game lobby.

#### **Object Type**: `lobby`

#### **Fields**  
- `room_id`: `int`  
- `name`: `str`  
- `owner`: `UserModel`  
- `members`: `list[UserModel]`  

#### **Field Explanation**  
- `room_id`: The unique identifier for the lobby.  
- `name`: The name of the lobby.  
- `owner`: The user who owns the lobby, represented by a `UserModel`.  
- `members`: A list of users in the lobby, each represented by a `UserModel`.  

---

### 2. `User Model`

Represents a user in the system.

#### **Object Type**: `user`

#### **Fields**  
- `user_id`: `int`  
- `username`: `str`  
- `avatar_url`: `str`  
- `presence_status`: `PresenceStatus`  

#### **Field Explanation**  
- `user_id`: The unique identifier for the user.  
- `username`: The username of the user.  
- `avatar_url`: The URL to the user's avatar image.  
- `presence_status`: The current online status of the user, represented by a `PresenceStatus` enumeration.  

---

### 3. `New Lobby Update Model`

Notification about a new lobby being created.

#### **Object Type**: `new-lobby-update`

#### **Fields**  
- `lobby_name`: `str`  
- `owner`: `UserModel`  

#### **Field Explanation**  
- `lobby_name`: The name of the newly created lobby.  
- `owner`: The user who owns the newly created lobby, represented by a `UserModel`.

---

### 4. `New User Update Model`

Notification about a new user being added.

#### **Object Type**: `new-user-update`

#### **Fields**  
- `user`: `UserModel`  

#### **Field Explanation**  
- `user`: The details of the newly added user, represented by a `UserModel`.  

---

### 5. `User Left Update Model`

Notification about a user leaving the system or a lobby.

#### **Object Type**: `user-left-update`

#### **Fields**  
- `user`: `UserModel`  

#### **Field Explanation**  
- `user`: The details of the user who has left, represented by a `UserModel`.  

---

### 6. `User Updated Update Model`

Notification about a user's information being updated.

#### **Object Type**: `user-updated-update`

#### **Fields**  
_None_  

#### **Field Explanation**  
- This response type indicates that a user's information has been updated in the system.  

---

## Enums

### 1. `LobbyUpdate`

#### **Values**
- `NEW_LOBBY`: `new-lobby`
- `NEW_USER`: `new-user`
- `USER_UPDATED`: `user-updated`
- `USER_LEFT`: `user-left`

---

### 2. `PresenceStatus`

#### **Values**
- `OFFLINE`: `offline`
- `ONLINE`: `online`
