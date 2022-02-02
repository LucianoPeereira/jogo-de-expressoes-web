var ws = new WebSocket("ws://localhost:8000/emo");

ws.onmessage = function(event) {
    const emocao_mestre = document.getElementById('emo')
    const video_mestre = document.getElementById('video_mestre')
    const video_aluno = document.getElementById('video_aluno')
    const emocao_aluno = document.getElementById('emo_aluno')
    const resultado = document.getElementById('result')

    const msg = JSON.parse(event.data)
    console.log(msg)

    if(msg.message === "mestre"){
        emocao_mestre.innerText = msg.emocao
        video_mestre.src = msg.imagem

    } else if(msg.message === "aluno"){
        emocao_aluno.innerText = msg.emocao
        video_aluno.src = msg.imagem
    } else if (msg.message == "resposta"){
        if(msg.result === true){
            resultado.innerText = "Você acertou!"
        } else {
            resultado.innerText = "Tempo esgotado!"
        }
    }
    
};
function stop(event) {
    ws.send("stop")
    event.preventDefault()
}
function go(event) {
    ws.send("go")
    event.preventDefault()
}