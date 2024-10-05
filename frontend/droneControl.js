// Send command to the server
function sendDroneCommand(context, user, message) {
    const data = {
        context: context,
        user: user,
        message: message
    };

    fetch('http://127.0.0.1:5000', {
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

// event listeners for custom buttons
document.addEventListener('DOMContentLoaded', () => {
    const buttons = [
        { id: 'left-click', command: 'test1' },
        { id: 'up', command: 'test2' },
        { id: 'right-click', command: 'test3' },
        { id: 'left', command: 'test4' },
        { id: 'right', command: 'test5' },
        { id: 'level-down', command: 'test6' },
        { id: 'down', command: 'test7' },
        { id: 'level-up', command: 'test8' }
    ];

    buttons.forEach(button => {
        const btnElement = document.getElementById(button.id);
        if (btnElement) {
            btnElement.addEventListener('click', () => {
                const context = 'moveCMD';
                const user = 'MentalBoom';
                const message = button.command;

                sendDroneCommand(context, user, message);
            });
        }
    });
});
