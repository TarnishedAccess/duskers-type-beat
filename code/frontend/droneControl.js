const abbreviationDict = {
    radar: 'RDR',
    computer: 'CMP',
    camera: 'CAM',
    generator: 'GEN',
    navigation: 'NAV',
    inventory_controller: 'INV',
    geolyzer: 'GEO'
};

var droneComponents = [];

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
    droneComponents = [];
    fetch('http://127.0.0.1:5001/connected_drones', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })


    .then(response => response.json())
    .then(data => {

        data.connected_drones.forEach((drone, i) => {
            const index = i + 1;
            updateDrone(index, drone.name);
            droneComponents.push(drone.components.sort());
        });
        console.log(droneComponents);
    })
    .catch(error => {
        console.error('Error fetching connected drones:', error);
    });
}

async function fetchDroneInfo(drone, context) {
    try {
        const response = await fetch(`http://127.0.0.1:5001/drone_info?param1=${drone}&param2=${context}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error fetching connected drones:', error);
        throw error;
    }
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
        inputLog.value = droneLogs[selectedDrone];

        selectedDroneComponents = droneComponents[selectedDrone];
        
        console.log('Selected Drone:', selectedDrone);
        console.log('Selected Components:', selectedDroneComponents);

        const droneModules = document.getElementById(`droneModuleSelect`);
        droneModules.innerHTML = ``;
        selectedDroneComponents.forEach(component => {
            droneModules.innerHTML += `
            <div id="droneModule${component}" class="droneModule button">${abbreviationDict[component]}</div>
            `;
        });

        selectedDroneComponents.forEach(component => {
            const button = document.getElementById(`droneModule${component}`);
            if (button) {
                button.onclick = () => handleComponentClick(component);
            }
        });

    }

    // YOUR WORK IS DOWN HERE

    function handleComponentClick(component) {
        switch (component) {
            case 'radar':
                console.log('Radar clicked');
                break;
            case 'computer':
                console.log('Computer clicked');
                break;
            case 'camera':
                console.log('Camera clicked');
                break;
            case 'generator':
                
                fetchDroneInfo(1, 'computer.energy()')
                .then(data => {
                    console.log('Fetched drone data:', data);
                })
                .catch(error => {
                    console.error('Failed to fetch drone info:', error);
                });
                break;

            case 'navigation':
                console.log('Navigation clicked');
                break;
            case 'inventory_controller':
                console.log('Inventory Controller clicked');
                break;
            case 'geolyzer':
                console.log('Geolyzer clicked');
                break;
            default:
                console.log('Unknown component:', component);
        }
    }

    // YOUR WORK IS UP HERE

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
