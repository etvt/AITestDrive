let chatHistory = [];

document.getElementById('sendButton').addEventListener('click', sendMessage);

document.getElementById('chatInput').addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent the default action to avoid form submission
        sendMessage();
    }
});

function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value;
    chatHistory.push({content: message, role: 'user'});

    fetch(chat_api_url, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({history: chatHistory})
    })
        .then(response => response.json())
        .then(data => {
            chatHistory.push({content: data.content, role: data.role});
            updateChatHistoryDisplay();
        })
        .catch(error => console.error('Error:', error));

    input.value = '';
}

function updateChatHistoryDisplay() {
    const historyDiv = document.getElementById('chatHistory');
    historyDiv.innerHTML = chatHistory.map(entry => {
        return `<div class="${entry.role}">${entry.content}</div>`;
    }).join('');
}
