function sendDroneCommand(context, user, message) {
    const data = {
        context: context,
        user: user,
        message: message
    };

    fetch('http://127.0.0.1:5001', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response from server:', data.response);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to get all connected drones
function fetchConnectedDrones() {
    fetch('http://127.0.0.1:5001/connected_drones', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Connected Drones:', data.connected_drones);

        data.connected_drones.forEach((drone, i) => {
            const index = i + 1;
            updateDrone(index, drone.name);
        });

    })
    .catch(error => {
        console.error('Error fetching connected drones:', error);
    });
}

// Swap selected drone from offline to online and give it a name
function updateDrone(index, name) {

    const droneCard = document.getElementById(`droneCard${index}`);
    const droneStatus = document.getElementById(`droneStatus${index}`);
    const droneInfo = document.getElementById(`droneInfo${index}`);
    const droneInformation = document.getElementById(`droneInformation${index}`);
    
    droneCard.classList.remove('droneCardOffline');
    
    droneStatus.classList.remove('droneStatusOffline');
    droneStatus.classList.add('droneStatusOnline');

    droneInfo.classList.remove('droneInfoOffline');

    droneStatus.textContent = "ONLINE";
    
    droneInformation.innerHTML = `
        <div class="droneInfoSquare">
            <div id="droneName${index}" class="droneName">
                <div id="droneNameTitle${index}" class="droneNameTitle">Name:</div>
                <div id="droneNameField${index}" class="droneNameField">${name}</div>
            </div>
            <div id="droneMode${index}" class="droneMode">
                <div id="droneModeTitle${index}" class="droneModeTitle">Mode:</div>
                <div id="droneModeField${index}" class="droneModeField">AUTO</div>
            </div>
        </div>
        <div class="battery">
            <div class="battery-level">
                <div class="division"></div>
                <div class="division"></div>
                <div class="division"></div>
                <div class="division"></div>
                <div class="division"></div>
            </div>
        </div>
    `;
}

// event listeners for custom buttons and input
document.addEventListener('DOMContentLoaded', () => {
    const inputLog = document.getElementById('dark-input-field');

    let droneLogs = ["", "", "", ""];

    inputLog.value = "";

    let selectedDrone = null;
    const droneCards = document.querySelectorAll('.droneCard');
    
    function handleDroneCardClick(index) {
        droneCards.forEach(card => card.classList.remove('selected'));
        droneCards[index].classList.add('selected');
        selectedDrone = index;
        inputLog.value = droneLogs[selectedDrone]
        console.log('Selected Drone:', selectedDrone);
    }
    droneCards.forEach((card, index) => {
        card.addEventListener('click', () => handleDroneCardClick(index));
    });

    const buttons = [
        { id: 'left-click', command: 'robot.swing()' },
        { id: 'up', command: 'robot.forward()' },
        { id: 'right-click', command: 'robot.use()' },
        { id: 'left', command: 'robot.turnLeft()' },
        { id: 'right', command: 'robot.turnRight()' },
        { id: 'level-down', command: 'robot.down()' },
        { id: 'down', command: 'robot.back()' },
        { id: 'level-up', command: 'robot.up()' },
    ];

    buttons.forEach(button => {
        const btnElement = document.getElementById(button.id);
        if (btnElement) {
            btnElement.addEventListener('click', () => {
                const context = 'moveCMD';
                const user = selectedDrone;
                const message = button.command;

                sendDroneCommand(context, user, message);
            });
        }
    });

    const sendButton = document.getElementById('send-Button');
    const inputField = document.getElementById('dark-input');

    if (sendButton && inputField) {
        sendButton.addEventListener('click', () => {
            const context = 'manualCMD';
            const user = selectedDrone;
            const message = inputField.value;

            sendDroneCommand(context, user, message);
            droneLogs[selectedDrone] += inputField.value + "\n"
            inputLog.value = droneLogs[selectedDrone]
        });
    }

    fetchConnectedDrones();
});
