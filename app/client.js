function verificarChute() {
    let chute = document.querySelector('input').value;
    
    if (chute == numeroSecreto) {
        alert('Acertou!');
    } else {
        if (chute > numeroSecreto) {
            alert('O número secreto é menor');
        } else {
            alert('O número secreto é maior');
        }
        limparCampo();
    }
}

function limparCampo() {
    let chute = document.querySelector('input');
    chute.value = '';
}
