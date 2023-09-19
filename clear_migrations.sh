#!/bin/bash

# Desativando o ambiente virtual, se ativo
if [ -n "$VIRTUAL_ENV" ]; then
    source $VIRTUAL_ENV/bin/deactivate
    echo "Ambiente virtual desativado."
fi

# Contando o número de diretórios __pycache__
pycache_count=$(find . -type d -name "__pycache__" | wc -l)

# Contando o número de arquivos de migração, exceto os __init__.py
migration_files_count=$(find . -path "*/migrations/*.py" -not -name "__init__.py" | wc -l)

# Mostrando a contagem para o usuário
echo "Serão removidos:"
echo "- $pycache_count diretórios __pycache__"
echo "- $migration_files_count arquivos de migração (exceto os __init__.py)"

# Perguntando ao usuário se eles desejam proceder
read -p "Você deseja continuar? (y/N): " response

if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
then
    # Encontrando e removendo todos os diretórios __pycache__
    find . -type d -name "__pycache__" -exec rm -r {} +
    
    # Encontrando e removendo todos os arquivos de migração, exceto os __init__.py
    find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
    find . -path "*/migrations/*.pyc"  -delete

    # Imprimindo uma mensagem de conclusão
    echo "Diretórios __pycache__ e arquivos de migração foram removidos, exceto os __init__.py"
else
    echo "Operação cancelada pelo usuário."
fi
