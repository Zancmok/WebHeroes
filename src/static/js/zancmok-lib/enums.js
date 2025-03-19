export const SocketEvent = {
    GET_LOBBY_DATA: "get-lobby-data",
    LOBBY_UPDATE: "lobby-update",
    CREATE_LOBBY: "create-lobby"
};

export const ObjectType = {
    LobbyModel: "lobby",
    NewLobbyUpdateModel: "new-lobby-update",
    NewUserUpdateModel: "new-user-update",
    UserLeftUpdateModel: "user-left-update",
    UserModel: "user",
    UserUpdatedUpdateModel: "user-updated-update",
    CreateLobbyResponse: "create-lobby-response",
    EmptyResponse: "empty",
    GetLobbyDataResponse: "get-lobby-data-response",
    LobbyUpdateResponse: "lobby-update",
    SuccessResponse: "success"
}

export const PresenceStatus = {
    OFFLINE: "offline",
    ONLINE: "online"
};

export const LobbyUpdate = {
    NEW_LOBBY: "new-lobby",
    NEW_USER: "new-user",
    USER_UPDATED: "user-updated",
    USER_LEFT: "user-left"
};
