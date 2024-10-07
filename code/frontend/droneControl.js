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

// event listeners for custom buttons and input
document.addEventListener('DOMContentLoaded', () => {
    const inputLog = document.getElementById('dark-input-field');

    inputLog.value = "";

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

    // Loop through your predefined buttons
    buttons.forEach(button => {
        const btnElement = document.getElementById(button.id);
        if (btnElement) {
            btnElement.addEventListener('click', () => {
                const context = 'moveCMD';
                const user = 'Controller';
                const message = button.command;

                sendDroneCommand(context, user, message);
            });
        }
    });

    // Event listener for the "RUN" button and input field
    const sendButton = document.getElementById('send-Button');
    const inputField = document.getElementById('dark-input');

    if (sendButton && inputField) {
        sendButton.addEventListener('click', () => {
            const context = 'manualCMD';
            const user = 'Controller';
            const message = inputField.value; // Get the value from the input field

            // Send the input value as the message
            sendDroneCommand(context, user, message);
            inputLog.value += inputField.value + "\n"
        });
    }
});
