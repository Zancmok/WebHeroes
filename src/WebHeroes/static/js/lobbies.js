(function init() {
    var socket = io()

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    socket.on("connect", async () => {
        console.log("Connected to server!");

        // Initial refresh
        socket.emit('lobby-management:refresh');

        // Refresh every 10 seconds
        while (true) {
            await sleep(10000);
            socket.emit('lobby-management:refresh');
        }
    });

    socket.on('lobby-management:refresh', (data) => {
        console.log('Received refresh response:', data);

        // Update online players
        const onlinePlayers = document.querySelector("#bot3 tbody");
        onlinePlayers.innerHTML = "";

        if (data.members && data.members.length > 0) {
            for (let i = 0; i < data.members.length; i++) {
                let member = data.members[i];
                let row = document.createElement("tr");
                row.innerHTML = "<td>" + member.member_name + "</td>";
                onlinePlayers.append(row);
            }
        } else {
            let row = document.createElement("tr");
            row.innerHTML = "<td>No players online</td>";
            onlinePlayers.append(row);
        }

        // Update lobbies
        const lobbiesTable = document.querySelector("#bot tbody");
        lobbiesTable.innerHTML = "";

        if (data.lobbies && data.lobbies.length > 0) {
            for (let i = 0; i < data.lobbies.length; i++) {
                let lobby = data.lobbies[i];
                let row = document.createElement("tr");

                // Host Name - use the lobby name
                let lobbyName = lobby.lobby_name || "Unknown";

                // Game Description - list all players
                let playersList = "";

                for (let i = 0; i < lobby.members.length; i++) {
                    playersList += lobby.members[i].member_name;

                    if (i < lobby.members.length - 1) {
                        playersList += ", ";
                    }
                }

                // Player Count
                let playerCount = lobby.members ? lobby.members.length : 0;

                row.innerHTML = `
                    <td>${lobbyName}</td>
                    <td><button class="join-btn" data-lobby="${lobby.lobby_name}">Join</button></td>
                    <td>${playersList}</td>
                    <td>${playerCount}</td>
                `;

                lobbiesTable.append(row);
            }

            // Add event listeners to join buttons
            document.querySelectorAll('.join-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    const lobbyName = this.getAttribute('data-lobby');
                    console.log('Joining lobby:', lobbyName);
                    // TODO: Implement join lobby functionality
                });
            });
        } else {
            let row = document.createElement("tr");
            row.innerHTML = "<td colspan='4'>No active lobbies</td>";
            lobbiesTable.append(row);
        }
    });

    // Create new game button handler
    document.getElementById('newGame').addEventListener('click', function() {
        let lobbyName = prompt("Enter lobby name:");
        if (lobbyName && lobbyName.trim() !== "") {
            socket.emit('lobby-management:create-lobby', {"lobby-name": lobbyName.trim()});
            // Refresh immediately after creating
            setTimeout(() => socket.emit('lobby-management:refresh'), 500);
        }
    });
})();