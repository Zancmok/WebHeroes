(function () {
  const socket = io();

  const lobbyNameEl = document.getElementById("lobbyName");
  const lobbyOwnerEl = document.getElementById("lobbyOwner");
  const playersListEl = document.getElementById("playersList");
  const statusEl = document.getElementById("status");
  const startBtn = document.getElementById("startBtn");

  const lobbyName = (sessionStorage.getItem("currentLobbyName") || "").trim();

  let refreshInterval = null;

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
    startBtn.style.display = "none";
    return;
  }

  // Hide until confirmed as owner
  startBtn.style.display = "none";

  lobbyNameEl.textContent = lobbyName;

  function requestLobby() {
    socket.emit("lobby-management:get-lobby");
  }

  socket.on("connect", () => {
    socket.emit("lobby-management:join-lobby", { lobby_name: lobbyName });
    requestLobby();
    if (refreshInterval) clearInterval(refreshInterval);
    refreshInterval = setInterval(requestLobby, 2000);
  });

  // Only the owner receives this event — if we get it, we are the owner
  socket.on("lobby-management:get-lobby", (data) => {
    if (!data) return;

    if (data.owner) {
      lobbyOwnerEl.textContent = data.owner.member_name || ("Owner (ID: " + data.owner.member_id + ")");
    } else {
      lobbyOwnerEl.textContent = "Unknown";
    }

    renderPlayers(data.members || []);
    setStatus("");

    // Receiving this response means we are the owner
    startBtn.style.display = "";
  });

  // All clients listen for game start and relocate simultaneously
  socket.once("lobby-management:game-started", () => {
    window.location.assign("/game/");
  });

  startBtn.addEventListener("click", () => {
    startBtn.disabled = true;
    setStatus("Starting game...");
    socket.emit("lobby-management:start-game");
  });
}());