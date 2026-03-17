(function init() {
  var socket = io();

  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  socket.on('connect', async () => {
    console.log('Connected to server!');
    socket.emit('lobby-management:refresh');

    while (true) {
      await sleep(10000);
      socket.emit('lobby-management:refresh');
    }
  });

  socket.on('lobby-management:refresh', (data) => {
    console.log('Received refresh response:', data);

    //Update online players list
    const playersList = document.getElementById('playersList');
    playersList.innerHTML = '';

    if (data.members && data.members.length > 0) {
      data.members.forEach(member => {
        const row = document.createElement('div');
        row.className = 'player-row';
        row.textContent = member.member_name;
        playersList.appendChild(row);
      });
    } else {
      const empty = document.createElement('div');
      empty.className = 'no-players';
      empty.textContent = 'No settlers online';
      playersList.appendChild(empty);
    }

    //Update lobbies table
    const tbody = document.querySelector('#lobbiesTable tbody');
    tbody.innerHTML = '';

    if (data.lobbies && data.lobbies.length > 0) {
      data.lobbies.forEach(lobby => {
        const row = document.createElement('tr');

        const lobbyName   = lobby.lobby_name || 'Unknown';
        const playersList = lobby.members.map(m => m.member_name).join(', ');
        const playerCount = lobby.members ? lobby.members.length : 0;

        row.innerHTML = `
          <td>${lobbyName}</td>
          <td><button class="join-btn" data-lobby="${lobby.lobby_name}">⚔ Join</button></td>
          <td>${playersList}</td>
          <td>${playerCount}</td>
        `;

        tbody.appendChild(row);
      });

      // Attach join button listeners
      document.querySelectorAll('.join-btn').forEach(btn => {
        btn.addEventListener('click', function () {
          const lobbyName = this.getAttribute('data-lobby').trim();
          console.log('Joining lobby:', lobbyName);
          sessionStorage.setItem('currentLobbyName', lobbyName);
          socket.emit('lobby-management:join-lobby', { lobby_name: lobbyName });
          window.location.href = '/lobby/';
        });
      });

    } else {
      const row = document.createElement('tr');
      row.className = 'no-data';
      row.innerHTML = "<td colspan='4'>No active campaigns — be the first to raise your banner!</td>";
      tbody.appendChild(row);
    }
  });

  //Create new game
  document.getElementById('newGame').addEventListener('click', function () {
    let lobbyName = prompt('Name your campaign:');
    if (lobbyName && lobbyName.trim() !== '') {
      lobbyName = lobbyName.trim();
      sessionStorage.setItem('currentLobbyName', lobbyName);
      socket.emit('lobby-management:create-lobby', { lobby_name: lobbyName });
      window.location.href = '/lobby/';
      setTimeout(() => socket.emit('lobby-management:refresh'), 500);
    }
  });

  //Back button
  document.getElementById('back').addEventListener('click', function () {
    window.history.back();
  });

})();