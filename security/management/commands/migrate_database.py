import os
import sqlite3
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Listar tabelas e seus dados do SQLite'

    def handle(self, *args, **kwargs):
        database_path = "db.sqlite3"  # Path do seu arquivo db.sqlite3

        # Verificar se o arquivo db.sqlite3 existe
        if not os.path.exists(database_path):
            raise CommandError(f"O arquivo {database_path} não foi encontrado.")

        # Conectar ao banco SQLite
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        # Consultar todas as tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Mostrar as tabelas e seus dados
        self.stdout.write('Tabelas no banco de dados SQLite e seus dados:')
        for table in tables:
            table_name = table[0]
            self.stdout.write(f"\nTabela: {table_name}")

            # Consultar e mostrar os dados da tabela
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            for row in rows:
                self.stdout.write(str(row))

        # Fechar a conexão
        conn.close()
