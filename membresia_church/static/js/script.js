//Confirmacao visual para Buttons de exclusao
domcument.querySelectorAll('.btn-excluir').forEach(botao => {
    botao.addEventListener('click', (evento) => {
        const confirmou = window.confirm('Tem certeza que deseja excluir?')
        if (!confirmou) {
            evento.preventDefault();
        }
    });
});

const campoSenha = document.getElementById('senha');
const forcasenha = document.getElementById('forca-senha');

//indica o nivel de seguranca da senha
if (campoSenha && forcasenha) {
    campoSenha.addEventListener('input', () => {
        const valor = campoSenha.value;
        let nivel = 'Senha fraca';

        if (valor.length >= 8 && /[A-Z]/.test(valor) && /\d/.test(valor)) {
            nivel = 'Senha forte';
        } else if (valor.length >= 6) {
            nivel = 'Senha média';
        }

        forcasenha.textContent = `Força da senha: ${nivel}`;
    });
}