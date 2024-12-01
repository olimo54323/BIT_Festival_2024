document.addEventListener('DOMContentLoaded', () => {
    // Connect to the SocketIO server
    const socket = io();

    // Get room ID and current user from the page
    const roomId = window.location.pathname.split('/').pop();
    const currentUsername = document.getElementById('current-username').textContent.trim();

    // Message form and input elements
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    const messagesContainer = document.getElementById('messages');

    // Join the room
    socket.emit('join', {room: roomId});

    // Send message
    messageForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const message = messageInput.value.trim();
        
        if (message) {
            // Emit message to server
            socket.emit('message', {
                room: roomId,
                message: message
            });
            
            // Clear input
            messageInput.value = '';
        }
    });

    // Handle incoming messages
    socket.on('message', (data) => {
        // Create new message element
        const messageDiv = document.createElement('div');
        
        // Determine if the message is from the current user
        const isCurrentUser = data.user === currentUsername;
        
        messageDiv.classList.add('message');
        if (isCurrentUser) {
            messageDiv.classList.add('text-right');
        }
        
        messageDiv.innerHTML = `
            <div class="inline-block max-w-xl text-left ${isCurrentUser ? 'bg-blue-500 text-white' : 'bg-gray-200'} rounded-lg px-4 py-2">
                <div class="font-semibold">${data.user}</div>
                <div>${data.message}</div>
                <div class="text-xs ${isCurrentUser ? 'text-blue-100' : 'text-gray-500'} mt-1">${data.timestamp}</div>
            </div>
        `;
        
        // Append to messages container
        messagesContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    });

    // Handle room status messages
    socket.on('status', (data) => {
        const statusDiv = document.createElement('div');
        statusDiv.classList.add('text-center', 'text-gray-500', 'my-2');
        statusDiv.textContent = data.msg;
        messagesContainer.appendChild(statusDiv);
    });
});