let chatHistory = [];

document.getElementById('sendButton').addEventListener('click', () => {
    const input = document.getElementById('chatInput');
    const message = input.value;
    chatHistory.push({ content: message, role: 'user' });

    fetch(chat_api_url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ history: chatHistory })
    })
    .then(response => response.json())
    .then(data => {
        chatHistory.push({ content: data.content, role: data.role });
        updateChatHistoryDisplay();
    })
    .catch(error => console.error('Error:', error));

    input.value = '';
});

function updateChatHistoryDisplay() {
    const historyDiv = document.getElementById('chatHistory');
    historyDiv.innerHTML = chatHistory.map(entry => {
        return `<div class="${entry.role}">${entry.content}</div>`;
    }).join('');
}
