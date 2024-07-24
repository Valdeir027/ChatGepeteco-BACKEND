const $chatMessages = Qs(".messages");

const baseUrl = window.location.origin.replace(/^http/, 'ws');

const socket = new WebSocket(baseUrl +"/ws/chat/");

var user_autenticated= '';

if(sessionStorage.user){
    var user_autenticated  = JSON.parse(sessionStorage.user)
}else{
    window.location.href = "/logout"
}
function scrollToBottom() {
    Qs(".messages").scrollTop = Qs(".messages").scrollHeight;
}
    
socket.onopen = () => {
    getAllRoom()
    console.log("Conectado")

}



const setRoomActive = (room_id) =>{
    var chatContainer = Qs('.chat-messages');
    QsAll(".list-rooms li").forEach(el => {
        el.classList.remove("active");
        
    })
    // var activeRoom = document.querySelector('.list-rooms li active');
        
        // Verifica se existe uma sala ativa
    chatContainer.style.display = 'block';


    Qs(`#room-${room_id}`).classList.add("active");
    Qs("#selected-room").value = room_id


    socket.send(JSON.stringify({
        'command': 'getMessages',
        'room_name': room_id
    }));

    socket.send(JSON.stringify({
        'command': 'join',
        'room_name': room_id
    }));

    
};

const getMessages = async (room_id) => {
    // Exemplo de como sair de uma sala
    socket.send(JSON.stringify({
        'command': 'leave',
        'room_name': document.querySelector("#selected-room").value
    }));
    const response = await fetch(`/${room_id}`);
    const html = await response.text();
    $chatMessages.innerHTML = html

    setRoomActive(room_id);
    
};


socket.onmessage = (e) => {
    var activeRoom  = Qs("#selected-room").value
    const data = JSON.parse(e.data);
    const message_info = Qs(".message_list_room")

    if (data.notification) {
            if(parseInt(data.notification.room.id) !== parseInt(activeRoom)){
                notify(`${data.notification.message.user.username}: ${data.notification.message.text}`)
            }
    } else if (data.message){
        if(message_info){
            message_info.style.display = "none"
        }
        addMessage(data.message)
        
    } else if(data.room){
        html =`<li role='button'class = "list-group-item"  id="room-${data.room.id}" onclick="getMessages('${data.room.id}')">${data.room.title}</li> `
        const $uniqueRoomContainer = Qs(".list-rooms");
        $uniqueRoomContainer.insertAdjacentHTML("afterbegin", html);
        const userString = sessionStorage.getItem('user');
        const user = JSON.parse(userString);
        console.log("user local:", user_autenticated.id, "user que criou a sala", data.room.user.id);
        if(user_autenticated.id === data.room.user.id){
            getLastRoom()
        }
        Qs(".create-room").reset();
    }
    if(data.rooms){
        for (const room of data.rooms) {
            addRoom(room)
            
        }
        
    }
    
    if(data.messages){
        for (const message of data.messages){
            addMessage(message)
            Qs(".messages").scrollTop = Qs(".messages").scrollHeight;
        }
    }


};


socket.onclose = () => {
    
}


const addMessage = (message) =>{
    if(message.user.id === user_autenticated.id){
        var html = `
        <div class="chat-message message-sent clearfix"">
            <div class="message-text">
            ${message.text}
            </div>
        </div>
        `

    }else {
        var html = `
        <div class="chat-message  message-received clearfix">
            <div class="message-text">
            <div class="message-username">${message.user.username}</div>
            ${message.text}
            </div>
        </div>
        `  
    }
    const $uniqueMessageContainer = Qs("#messages");
    $uniqueMessageContainer.insertAdjacentHTML("beforeend", html);
}



const getAllRoom = async (data) =>{
    
    socket.send(JSON.stringify({
        'command': 'getRooms',

    }));

}
const sendMessage = async (data) =>{
    
    socket.send(JSON.stringify({
        'command': 'message',
        'message': data.message,
        'room_name': data.room_id
    }));

    Qs(".send-message").reset();
};

const createRoom = async (data) =>{

    socket.send(JSON.stringify({
        'command': 'createRoom',
        'room_name': data.title
    }));
    const modal = bootstrap.Modal.getInstance(Qs(".modal"));
    modal.hide()
    
    
}


const getLastRoom  =  () => {
    Qs(".list-rooms li").click();
}


Qs(".send-message").addEventListener('submit', (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target).entries());
    sendMessage(data);
});

const textarea = document.getElementById('chat_textarea');
const form = Qs(".send-message");


textarea.addEventListener('input', ()=>{
    form.style.height = 'auto'; // Reseta a altura para calcular a nova altura corretamente
    textarea.style.height = 'auto'; // Reseta a altura para calcular a nova altura corretamente
    textarea.style.height = (textarea.scrollHeight) + 'px'; 
}
);
function autoResize() {
this.style.height = 'auto'; // Reseta a altura para calcular a nova altura corretamente
this.style.height = (this.scrollHeight) + 'px'; // Ajusta a altura com base no scrollHeight
}


Qs(".create-room").addEventListener('submit', (e) =>{
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target).entries());
    createRoom(data)
})


const notify = (body) =>{
    // Verifica se a API de Notificação está disponível
    if (!('Notification' in window)) {
        alert('Seu navegador não suporta notificações.');
        return;
    }

    // Verifica se o usuário já concedeu permissão
    if (Notification.permission === 'granted') {
        // Cria e exibe a notificação
        new Notification("Chatgepeteco", {
        body: body,
        icon: 'https://via.placeholder.com/150' // Opcional: ícone da notificação
        });
    } else if (Notification.permission === 'default') {
        // Solicita permissão ao usuário
        Notification.requestPermission().then(permission => {
        if (permission === 'granted') {
            new Notification('Título da Notificação', {
            body: 'Este é o corpo da notificação.',
            icon: 'https://via.placeholder.com/150'
            });
        }
        });
    }
}


function scrollToBottom() {
    var messages = document.getElementById('messages');
    messages.scrollTop = messages.scrollHeight;
}


const addRoom= (room) =>{
    html = `<li role='button'class = "list-group-item"  id="room-${room.id}" onclick="getMessages('${room.id}')">${room.title}</li> `
    const $uniqueRoomContainer = Qs(".list-rooms");
    $uniqueRoomContainer.insertAdjacentHTML("afterbegin", html);
}


console.log(user_autenticated)
