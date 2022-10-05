const chatLog = document.querySelector('#chat-log')
const roomName = JSON.parse(document.getElementById('room-name').textContent);
const logginUser = JSON.parse(document.getElementById('user-id').textContent);
const userName = JSON.parse(document.getElementById('username').textContent);

if (chatLog.childNodes.length <= 1){
    const emptyText = document.createElement('h3')
    emptyText.id = 'emptyText'
    emptyText.innerText = 'opps! no message yet'
    emptyText.className = 'emptyText'
    chatLog.appendChild(emptyText)
}
const chatSocket = new WebSocket(
    'ws://' 
    + window.location.host 
    + '/ws/' 
    + roomName 
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const messageElement = document.createElement('div')
    const userId = data.user_id
    messageElement.innerText = data.message

    if (userId === logginUser){
        messageElement.classList.add('message', 'sender')
    }else{
        messageElement.classList.add('message', 'receiver')
    }

    chatLog.appendChild(messageElement)

    if (document.querySelector('#emptyText')){
        document.querySelector('#emptyText').remove()
    }

};

chatSocket.onclose = function(e){
    console.error('Chat Socket Closed Unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e){
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    const obj = JSON.stringify({'message': userName + ' says: ' + message});
    chatSocket.send(obj)
    messageInputDom.value = '';
};
