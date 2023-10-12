#!/bin/bash

# Verifica se o diretório certs existe, se não, cria-o
if [ ! -d "certs" ]; then
  mkdir certs
fi

# Navegue até o diretório certs
cd certs

# Gere o certificado autoassinado e a chave privada
openssl req -x509 -newkey rsa:4096 -nodes -out server.crt -keyout server.key -days 365 \
-subj "/C=BR/ST=Minas Gerais/L=Belo Horizonte/O=Smart Mecanico/OU=Tecnologia da Informacao/CN=smartmecanico.com.br/emailAddress=smartmecanico@gmail.com"

# Combine server.crt e server.key para criar um arquivo .pem
cat server.crt server.key > server.pem

# Informe ao usuário que os arquivos foram criados
echo "Os arquivos server.crt, server.key e server.pem foram criados no diretório certs."

# Volte ao diretório anterior
cd ..