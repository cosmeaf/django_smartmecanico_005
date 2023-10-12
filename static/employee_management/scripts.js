document.addEventListener('DOMContentLoaded', function () {
  const cepInput = document.querySelector('#id_cep');

  if (cepInput) {
      cepInput.addEventListener('blur', function () {
          const cep = cepInput.value;
          if (cep) {
              fetch(`https://viacep.com.br/ws/${cep}/json/`)
                  .then(response => response.json())
                  .then(data => {
                      document.querySelector('#id_logradouro').value = data.logradouro;
                      document.querySelector('#id_complemento').value = data.complemento;
                      document.querySelector('#id_bairro').value = data.bairro;
                      document.querySelector('#id_localidade').value = data.localidade;
                      document.querySelector('#id_uf').value = data.uf;
                  })
                  .catch(error => {
                      console.error('Erro ao buscar o CEP:', error);
                  });
          }
      });
  }
});