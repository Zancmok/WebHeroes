(function () {
  const socket = io();

  const lobbyNameEl  = document.getElementById("lobbyName");
  const lobbyOwnerEl = document.getElementById("lobbyOwner");
  const playersListEl = document.getElementById("playersList");
  const statusEl     = document.getElementById("status");
  const startBtn     = document.getElementById("startBtn");

  const lobbyName = (sessionStorage.getItem("currentLobbyName") || "").trim();

  let refreshInterval = null;

  function setStatus(msg, isError) {
    statusEl.textContent = msg || "";
    statusEl.className   = isError ? "msg-err" : "";
  }

  function renderPlayers(members) {
    playersListEl.innerHTML = "";
    if (!members || members.length === 0) {
      const li = document.createElement("li");
      li.textContent = "No settlers joined yet";
      playersListEl.appendChild(li);
      return;
    }
    for (const m of members) {
      const li = document.createElement("li");
      li.textContent = m.member_name;
      playersListEl.appendChild(li);
    }
  }

  // No lobby selected
  if (!lobbyName) {
    lobbyNameEl.textContent  = "Unknown Campaign";
    lobbyOwnerEl.textContent = "Unknown";
    renderPlayers([]);
    setStatus("No lobby selected. Go back and create or join a lobby first.", true);
    startBtn.style.display = "none";
    return;
  }

  // Hide start button until confirmed as owner
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

    lobbyOwnerEl.textContent = data.owner
      ? (data.owner.member_name || "Owner (ID: " + data.owner.member_id + ")")
      : "Unknown";

    renderPlayers(data.members || []);
    setStatus("");

    // Receiving this response means we are the owner
    startBtn.style.display = "";
  });

  // All clients redirect when the game starts
  socket.once("lobby-management:game-started", () => {
    window.location.assign("/game/");
  });

  startBtn.addEventListener("click", () => {
    startBtn.disabled = true;
    setStatus("Rallying the troops…");
    socket.emit("lobby-management:start-game");
  });
}());