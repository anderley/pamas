document.addEventListener('DOMContentLoaded', function() {

    const inputCartao = document.getElementById('id_cartao');
    const inputValidade = document.getElementById('id_vencimento');
    const inputNome = document.getElementById('id_nome');
    const inputCVC = document.getElementById('id_codigo');
    
    const cardNumberDisplay = document.getElementById('card-number');
    const cardValidadeDisplay = document.getElementById('card-validade');
    const cardNomeDisplay = document.getElementById('card-nome');
    const cardCVCDisplay = document.getElementById('card-cvc');
    
    const cartaoOption = document.getElementById('cartao-option');
    const pixOption = document.getElementById('pix-option');
    const cardDetails = document.getElementById('card-details'); // A caixa de informações do cartão
    const pixDetails = document.getElementById('pix-details'); // A caixa de informações do Pix

    // Inicialmente, esconda as caixas de detalhes
    cardDetails.classList.add('hidden');
    pixDetails.classList.add('hidden');

    // Máscara para o número do cartão
    inputCartao.addEventListener('input', function (e) {
        let valor = this.value.replace(/\D/g, '');
        if (valor.length > 16) {
            valor = valor.substring(0, 16);
        }
        let partes = [];
        for (let i = 0; i < valor.length; i += 4) {
            partes.push(valor.substring(i, i + 4));
        }
        this.value = partes.join(' ').trim();
        cardNumberDisplay.textContent = valor.length > 0 ? this.value : '**** **** **** ****';
    });

    // Máscara para a validade do cartão
    inputValidade.addEventListener('input', function (e) {
        let valor = this.value.replace(/\D/g, ''); // Remove caracteres não numéricos
        if (valor.length > 6) {
            valor = valor.substring(0, 6); // Limita a 4 dígitos
        }
        // Adiciona a barra (/) no terceiro caractere
        if (valor.length >= 3) {
            valor = valor.substring(0, 2) + '/' + valor.substring(2);
        }
        this.value = valor;
        cardValidadeDisplay.textContent = valor.length > 0 ? 'Validade: ' + valor : 'Validade: **/**';
    });

    // Atualiza o nome no cartão
    inputNome.addEventListener('input', function (e) {
        cardNomeDisplay.textContent = this.value.length > 0 ? this.value : 'Nome Sobrenome';
    });

    // Atualiza o CVC
    inputCVC.addEventListener('input', function (e) {
        let valor = this.value.replace(/\D/g, ''); // Remove caracteres não numéricos
        if (valor.length > 4) {
            valor = valor.substring(0, 4); 
        }
        this.value = valor;
        cardCVCDisplay.textContent = valor.length > 0 ? valor : '***';
    });

    cartaoOption.addEventListener('click', function() {
        cardDetails.classList.remove('hidden');
        pixDetails.classList.add('hidden');
        document.getElementById('cartao').checked = true; // Marca o botão de rádio
    });

    pixOption.addEventListener('click', function() {
        pixDetails.classList.remove('hidden');
        cardDetails.classList.add('hidden');
        document.getElementById('pix').checked = true; // Marca o botão de rádio
    });

});