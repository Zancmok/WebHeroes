(function () {
  const socket = io();

  const lobbyNameEl = document.getElementById("lobbyName");
  const lobbyOwnerEl = document.getElementById("lobbyOwner");
  const playersListEl = document.getElementById("playersList");
  const statusEl = document.getElementById("status");
  const startBtn = document.getElementById("startBtn");

  const lobbyName = (sessionStorage.getItem("currentLobbyName") || "").trim();

  function setStatus(msg) {
    statusEl.textContent = msg || "";
  }

  function renderPlayers(members) {
    playersListEl.innerHTML = "";
    if (!members || members.length === 0) {
      const li = document.createElement("li");
      li.textContent = "No players joined yet";
      playersListEl.appendChild(li);
      return;
    }

    for (const m of members) {
      const li = document.createElement("li");
      li.textContent = m.member_name;
      playersListEl.appendChild(li);
    }
  }

  if (!lobbyName) {
    lobbyNameEl.textContent = "Unknown";
    lobbyOwnerEl.textContent = "Unknown";
    renderPlayers([]);
    setStatus("No lobby selected. Go back and create/join a lobby first.");
    return;
  }

  lobbyNameEl.textContent = lobbyName;

  function requestRefresh() {
    socket.emit("lobby-management:refresh");
  }

  socket.on("connect", () => {
    // Make sure the server session joins the lobby
    socket.emit("lobby-management:join-lobby", { lobby_name: lobbyName });

    requestRefresh();
    setInterval(requestRefresh, 2000);
  });

  socket.on("lobby-management:refresh", (data) => {
    if (!data || !data.lobbies) return;

    const lobby = data.lobbies.find(l => (l.lobby_name || "").trim() === lobbyName);

    if (!lobby) {
      lobbyOwnerEl.textContent = "Unknown";
      renderPlayers([]);
      setStatus("Lobby not found (maybe it was deleted or not created yet).");
      return;
    }

    // We don't have owner name directly in refresh, only owner_id.
    // But we do have members list with names; owner is usually included in members.
    // So we guess owner name by matching owner_id to members.
    const ownerMember = (lobby.members || []).find(m => m.member_id === lobby.owner_id);

    lobbyOwnerEl.textContent = ownerMember ? ownerMember.member_name : "Owner (ID: " + lobby.owner_id + ")";
    renderPlayers(lobby.members || []);
    setStatus("");
  });

  startBtn.addEventListener("click", () => {
    socket.emit("lobby-management:start-game");
  });
})();
