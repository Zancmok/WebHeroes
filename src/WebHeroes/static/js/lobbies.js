(function init() {
    var socket = io()

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    socket.on("connect", async () => {
        console.log("Connected to server!");

        socket.emit('create-lobby', {"lobby-name": "Im a bloody nigger, ho, ho, ho"});

        while (true)
        {
            socket.emit('refresh');
            await sleep(10000);
        }
    });

    socket.on('refresh', (data) => {
        console.log('Received refresh response:', data);

        const onlinePlayers = document.querySelector("#bot3 tbody");
        onlinePlayers.innerHTML = "";

        if(data.members && data.members.length > 0){

            for(let i = 0; i < data.members.length; i++){

                let member = data.members[i];
                let row = document.createElement("tr");

                row.innerHTML = "<td>" + member.member_name + "</td>";
                onlinePlayers.append(row);
            }
        } else{
            let row = row = document.createElement("tr");

            row.innerHTML = "<td>No players online</td>"
            onlinePlayers.append(row);
        }

    });
})()