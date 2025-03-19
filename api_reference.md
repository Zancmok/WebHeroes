# API Reference

## Index
- [WebSocket Events](#websocket-events)  
  - [`connect`](#1-websocket-event-connect)  
  - [`disconnect`](#2-websocket-event-disconnect)  
  - [`get_lobby_data`](#3-websocket-event-get_lobby_data)  
  - [`create_lobby`](#4-websocket-event-create_lobby)  
  - [`lobby_update`](#5-websocket-event-lobby_update)  
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
  - [`Create Lobby Response`](#5-create-lobby-response)  
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

### 1. [`WebSocket Event: connect`](#index)
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

### 2. [`WebSocket Event: disconnect`](#index)
Handles the WebSocket disconnection event.

#### **Behavior**
- Updates the user's presence status to `offline` if they exist in `UserManager`.
- Removes the user from the default lobby room.

---

### 3. [`WebSocket Event: get_lobby_data`](#index)
Fetches and emits the current lobby data, providing information about the requesting user, the users in the same lobby, and other available lobbies.

#### **Behavior**
- If the session lacks a valid access token, an [`EmptyResponse`](#1-empty-response) is emitted.
- Retrieves the requesting user's details based on their session user ID.
- Gathers information about the current lobby's users.
- Collects details of other available lobbies and their members.

#### **Response**
- [**`EmptyResponse`**](#1-empty-response): If the user is not authenticated.
- [**`GetLobbyDataResponse`**](#3-get-lobby-data-response): If the user is authenticated, containing:
  - `self`: The requesting user.
  - `users`: A list of users in the same lobby.
  - `lobbies`: A list of available lobbies and their members.

---

### 4. [`WebSocket Event: create_lobby`](#index)
Allows a user to create a new lobby and automatically join it.

#### **Request**
- **Payload**:
  - `lobby_name` (`string`, required): The name of the new lobby.

#### **Behavior**
- The server validates the `lobby_name`.
- If the user is already in another lobby, the request is rejected.
- The user is removed from the default lobby and added to the new one.
- The new lobby is added to the list of available lobbies.
- The server sends two updates to all users in the default lobby:
  - A [`LOBBY_UPDATE`](#4-lobby-update-response) event indicating a new lobby was created.
  - A [`LOBBY_UPDATE`](#4-lobby-update-response) event indicating the user left the default lobby.

#### **Response**
- [**`EmptyResponse`**](#1-empty-response): If `lobby_name` is invalid or the user is already in another lobby.
- [**`CreateLobbyResponse`**](#5-create-lobby-response): If the lobby is successfully created, containing:
  - `lobby`: The newly created lobby details.

---

### 5. [`WebSocket Event: lobby_update`](#index)
Notifies all users when a change occurs in the lobby system.

#### **Sent by**: Server  
#### **Payload**:
  - `change_type` (`LobbyUpdate`): The type of change that occurred.
  - `change`:
    - If `change_type = NEW_LOBBY`: `NewLobbyUpdateModel`
    - If `change_type = USER_LEFT`: `UserLeftUpdateModel`

#### **Behavior**
- Sent when:
  - A new lobby is created (`NEW_LOBBY`).
  - A user leaves the default lobby to create their own (`USER_LEFT`).

#### **Response**
- No direct response; clients update their UI accordingly.


---

## GET Methods

### 1. [`GET /`](#index)
Serves the home page.

#### **Request**
- **Method**: `GET`
- **Endpoint**: `/`

#### **Response**
- **200 OK**: Returns the rendered HTML page for the home screen.

---

### 2. [`GET /modding-documentation/`](#index)
Serves the modding documentation page.

#### **Request**
- **Method**: `GET`
- **Endpoint**: `/modding-documentation/`

#### **Response**
- **200 OK**: Returns the rendered HTML page for the modding documentation.

---

### 3. [`GET /oauth/`](#index)
Handles Discord OAuth2 authentication.

#### **Request**
- **Method**: `GET`
- **Endpoint**: `/oauth/`
- **Query Parameters**:
  - `code` (string, required): Authorization code from Discord.

#### **Response**
- **302 Found**: Redirects to:
  - [`/online-lobbies/`](#4-get-online-lobbies) if authentication is successful.
  - [`/`](#1-get-) if authentication fails.

#### **Behavior**
- Exchanges the authorization code for an access token.
- Retrieves user details from Discord.
- Stores user details (`access_token`, `username`, `avatar_url`, `user_id`) in the session.

---

### 4. [`GET /online-lobbies/`](#index)
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

### 1. [`Empty Response`](#index)
Represents an empty response with no additional data.

#### Object Type: `empty`

#### **Fields**
_None_

#### **Field Explanation**
- This response type indicates that no additional data is included.
- It is used when an API response is required but no further information is necessary.

---

### 2. [`Success Response`](#index)
Indicates a successful operation.

#### Object Type: `success`

#### **Fields**
_None_

#### **Field Explanation**
- This response type is used to indicate that an operation was successfully executed without additional data.

---

### 3. [`Get Lobby Data Response`](#index)
Provides data about available lobbies and active users.

#### Object Type: `get-lobby-data-response`

#### **Fields**
- `self`: [`UserModel`](#2-user-model)  
- `users`: [`list[UserModel]`](#2-user-model)  
- `lobbies`: [`list[LobbyModel]`](#1-lobby-model)  

#### **Field Explanation**
- `self`: The requesting user.  
- `users`: A list of active users in the system.  
- `lobbies`: A list of available lobbies.

---

### 4. [`Lobby Update Response`](#index)
Represents an update to a lobby, detailing the type of change and its specifics.

#### Object Type: `lobby-update`

#### **Fields**
- `change_type`: [`LobbyUpdate`](#1-lobbyupdate)  
- `change`: `NewUserUpdateModel | NewLobbyUpdateModel | UserUpdatedUpdateModel | UserLeftUpdateModel`  

#### **Field Explanation**
- `change_type`: The type of change that occurred, represented as an enumeration from `LobbyUpdate`.  
- `change`: The specific details of the change, which can be one of the following:  
  - `NewUserUpdateModel`  
  - `NewLobbyUpdateModel`  
  - `UserUpdatedUpdateModel`  
  - `UserLeftUpdateModel`  

---

### 5. [`Create Lobby Response`](#index)

Gives you the data about the newly created lobby. Sent only to the user creating the said lobby.

#### Object Type: `create-lobby-response`

#### **Fields**
- `lobby`: [`LobbyModel`](#1-lobby-model)

#### **Field Explanation**
- `lobby`: The newly created lobby.

---

## Response Data Models

### 1. [`Lobby Model`](#index)

Represents a game lobby.

#### **Object Type**: `lobby`

#### **Fields**  
- `room_id`: `int`  
- `name`: `str`  
- `owner`: [`UserModel`](#2-user-model)  
- `members`: [`list[UserModel]`](#2-user-model)  

#### **Field Explanation**  
- `room_id`: The unique identifier for the lobby.  
- `name`: The name of the lobby.  
- `owner`: The user who owns the lobby, represented by a `UserModel`.  
- `members`: A list of users in the lobby, each represented by a `UserModel`.  

---

### 2. [`User Model`](#index)

Represents a user in the system.

#### **Object Type**: `user`

#### **Fields**  
- `user_id`: `int`  
- `username`: `str`  
- `avatar_url`: `str`  
- `presence_status`: [`PresenceStatus`](#2-presencestatus) 

#### **Field Explanation**  
- `user_id`: The unique identifier for the user.  
- `username`: The username of the user.  
- `avatar_url`: The URL to the user's avatar image.  
- `presence_status`: The current online status of the user, represented by a `PresenceStatus` enumeration.  

---

### 3. [`New Lobby Update Model`](#index)

Notification about a new lobby being created.

#### **Object Type**: `new-lobby-update`

#### **Fields**  
- `lobby_name`: `str`  
- `owner`: [`UserModel`](#2-user-model)  

#### **Field Explanation**  
- `lobby_name`: The name of the newly created lobby.  
- `owner`: The user who owns the newly created lobby, represented by a `UserModel`.

---

### 4. [`New User Update Model`](#index)

Notification about a new user being added.

#### **Object Type**: `new-user-update`

#### **Fields**  
- `user`: [`UserModel`](#2-user-model)  

#### **Field Explanation**  
- `user`: The details of the newly added user, represented by a `UserModel`.  

---

### 5. [`User Left Update Model`](#index)

Notification about a user leaving the system or a lobby.

#### **Object Type**: `user-left-update`

#### **Fields**  
- `user`: [`UserModel`](#2-user-model)  

#### **Field Explanation**  
- `user`: The details of the user who has left, represented by a `UserModel`.  

---

### 6. [`User Updated Update Model`](#index)

Notification about a user's information being updated.

#### **Object Type**: `user-updated-update`

#### **Fields**  
_None_

#### **Field Explanation**  
- This response type indicates that a user's information has been updated in the system.  

---

## Enums

### 1. [`LobbyUpdate`](#index)

#### **Values**
- `NEW_LOBBY`: `new-lobby`
- `NEW_USER`: `new-user`
- `USER_UPDATED`: `user-updated`
- `USER_LEFT`: `user-left`

---

### 2. [`PresenceStatus`](#index)

#### **Values**
- `OFFLINE`: `offline`
- `ONLINE`: `online`
