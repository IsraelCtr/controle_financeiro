import sqlite3


class AppBD():
    def __init__(self):
        self.criarTabelas()

    def abrirConexao(self):
        try:
            self.connection = sqlite3.connect('database.db')
        except sqlite3.Error as error:
            print("Falha ao se conectar ao banco de dados", error)

    def criarTabelas(self):
        self.abrirConexao()
        create_table_query_1 = """CREATE TABLE IF NOT EXISTS despesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            data DATETIME NOT NULL,
            valor REAL NOT NULL,
            id_condicao INTEGER,
            id_status INTEGER,
            FOREIGN KEY(id_condicao) REFERENCES codicoes(id),
            FOREIGN KEY(id_status) REFERENCES status(id)
        );"""

        create_table_query_2 = """CREATE TABLE IF NOT EXISTS codicoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL UNIQUE
        );"""

        create_table_query_3 = """CREATE TABLE IF NOT EXISTS status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL UNIQUE
        );"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(create_table_query_1)
            cursor.execute(create_table_query_2)
            cursor.execute(create_table_query_3)
            self.connection.commit()
            print("Tabelas criada com sucesso")
        except sqlite3.Error as error:
            print("Falha ao criar tabela", error)
        finally:
            if self.connection:
                cursor.close()
                self.connection.close()
                print("A conexao com o sqlite foi fechada.")

    def inserirCondicoesPadrao(self, descricao_condicoes):
        self.abrirConexao()
        insert_query = """ INSERT OR IGNORE INTO codicoes (descricao) VALUES (?)"""
        try:
            cursor = self.connection.cursor()
            cursor.executemany(
                insert_query, [(descricao,) for descricao in descricao_condicoes])
            self.connection.commit()
            print("Dados de condições inseridos com sucesso")
        except sqlite3.Error as error:
            print("Falha ao inserir dados de condições", error)
        finally:
            cursor.close()
            self.connection.close()
            print("A conexão com o banco de dados foi fechada")

    def inserirStatusPadrao(self, descricao_status):
        self.abrirConexao()
        insert_query = """INSERT OR IGNORE INTO status (descricao) VALUES (?)"""
        try:
            cursor = self.connection.cursor()
            cursor.executemany(
                insert_query, [(descricao,) for descricao in descricao_status])
            self.connection.commit()
            print("Dados de status inseridos com sucesso")
        except sqlite3.Error as error:
            print("Falha ao inserir dados de status", error)
        finally:
            cursor.close()
            self.connection.close()
            print("A conexão com o banco de dados foi fechada")

    def inserirDespesa(self, descricao, data, valor, id_condicao, id_status):
        self.abrirConexao()
        insert_query = """INSERT INTO despesas (descricao, data, valor, id_condicao, id_status) VALUES (?, ?, ?, ?, ?)"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(insert_query, (descricao, data,
                           valor, id_condicao, id_status))
            self.connection.commit()
            print("Despesa inserida com sucesso")
        except sqlite3.Error as error:
            print("Falha ao inserir despesa", error)
        finally:
            if self.connection:
                cursor.close()
                self.connection.close()
                print("A conexão com o banco de dados foi fechada")

    def inserirCondicao(self, descricao):
        self.abrirConexao()
        insert_query = """INSERT INTO codicoes (descricao) VALUES (?)"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(insert_query, (descricao,))
            self.connection.commit()
            print("Condição inserida com sucesso")
        except sqlite3.Error as error:
            print("Falha ao inserir condição", error)
        finally:
            if self.connection:
                cursor.close()
                self.connection.close()
                print("A conexão com o banco de dados foi fechada")

    def inserirStatus(self, descricao):
        self.abrirConexao()
        insert_query = """INSERT INTO status (descricao) VALUES (?)"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(insert_query, (descricao,))
            self.connection.commit()
            print("Status inserido com sucesso")
        except sqlite3.Error as error:
            print("Falha ao inserir status", error)
        finally:
            if self.connection:
                cursor.close()
                self.connection.close()
                print("A conexão com o banco de dados foi fechada")

    def selecionarDespesas(self):
        self.abrirConexao()
        select_query = """SELECT despesas.id, despesas.descricao, despesas.data, despesas.valor, codicoes.descricao as condicao, status.descricao as status
                        FROM despesas
                        INNER JOIN codicoes ON despesas.id_condicao = codicoes.id
                        INNER JOIN status ON despesas.id_status = status.id
                        ORDER BY despesas.id DESC"""
        despesas = []
        try:
            cursor = self.connection.cursor()
            cursor.execute(select_query)
            despesas = cursor.fetchall()
        except sqlite3.Error as error:
            print("Falha ao retornar despesas", error)
        finally:
            if self.connection:
                cursor.close()
                self.connection.close()
                print("A conexão com o banco de dados foi fechada")
        return despesas

    def selecionarCondicoes(self):
        self.abrirConexao()
        select_query = "SELECT * FROM codicoes"
        condicoes = []
        try:
            cursor = self.connection.cursor()
            cursor.execute(select_query)
            condicoes = cursor.fetchall()
        except sqlite3.Error as error:
            print("Falha ao retornar condições", error)
        finally:
            if self.connection:
                cursor.close()
                self.connection.close()
                print("A conexão com o banco de dados foi fechada")
        return condicoes

    def selectCondicoes(self):
        self.abrirConexao()
        select_query = "SELECT * FROM codicoes"
        condicoes = []
        try:
            cursor = self.connection.cursor()
            cursor.execute(select_query)
            condicoes = cursor.fetchall()
        except sqlite3.Error as error:
            print("Falha ao retornar condições", error)
        finally:
            if self.connection:
                cursor.close()
                self.connection.close()
                print("A conexão com o banco de dados foi fechada")
        return condicoes

    def selectStatus(self):
        self.abrirConexao()
        select_query = "SELECT * FROM status"
        status = []
        try:
            cursor = self.connection.cursor()
            cursor.execute(select_query)
            status = cursor.fetchall()
        except sqlite3.Error as error:
            print("Falha ao retornar status", error)
        finally:
            if self.connection:
                cursor.close()
                self.connection.close()
                print("A conexão com o banco de dados foi fechada")
        return status

    def atualizarDespesa(self, despesa_id, descricao, data, valor, id_condicao, id_status):
        self.abrirConexao()
        update_query = "UPDATE despesas SET descricao = ?, data = ?, valor = ?, id_condicao = ?, id_status = ? WHERE id = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(update_query, (descricao, data, valor,
                           id_condicao, id_status, despesa_id))
            self.connection.commit()
            print("Despesa atualizada com sucesso")
        except sqlite3.Error as error:
            print('Falha ao atualizar a despesa', error)
        finally:
            if self.connection:
                cursor.close()
                self.connection.close()
                print("A conexão com o banco de dados foi fechada")

    def atualizarCondicao(self, condicao_id, descricao):
        self.abrirConexao()
        update_query = "UPDATE codicoes SET descricao = ? WHERE id = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(update_query, (descricao, condicao_id))
            self.connection.commit()
            print("Condição atualizada com sucesso")
        except sqlite3.Error as error:
            print('Falha ao atualizar a condição', error)
        finally:
            if self.connection:
                cursor.close()
                self.connection.close()
                print("A conexão com o banco de dados foi fechada")

    def atualizarStatus(self, status_id, descricao):
        self.abrirConexao()
        update_query = "UPDATE status SET descricao = ? WHERE id = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(update_query, (descricao, status_id))
            self.connection.commit()
            print("Status atualizado com sucesso")
        except sqlite3.Error as error:
            print('Falha ao atualizar o status', error)
        finally:
            if self.connection:
                cursor.close()
                self.connection.close()
                print("A conexão com o banco de dados foi fechada")

    def deletarDespesa(self, despesa_id):
        self.abrirConexao()
        delete_query = "DELETE FROM despesas WHERE id = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(delete_query, (despesa_id,))
            self.connection.commit()
            print('Despesa deletada com sucesso')
        except sqlite3.Error as error:
            print("Falha ao deletar despesa")
        finally:
            if self.connection:
                cursor.close()
                self.connection.close()
                print('A conexão com o banco de dados foi fechada')

    def deletarCondicao(self, descricao):
        self.abrirConexao()
        delete_query = "DELETE FROM codicoes WHERE descricao = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(delete_query, (descricao,))
            self.connection.commit()
            print('Condição deletada com sucesso')
        except sqlite3.Error as error:
            print("Falha ao deletar condição")
        finally:
            if self.connection:
                cursor.close()
                self.connection.close()
                print('A conexão com o banco de dados foi fechada')

    def deletarStatus(self, descricao):
        self.abrirConexao()
        delete_query = "DELETE FROM status WHERE descricao = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(delete_query, (descricao,))
            self.connection.commit()
            print('Status deletado com sucesso')
        except sqlite3.Error as error:
            print("Falha ao deletar status")
        finally:
            if self.connection:
                cursor.close()
                self.connection.close()
                print('A conexão com o banco de dados foi fechada')

    def obter_id_condicao_por_nome(self, nome_condicao):
        self.abrirConexao()
        select_query = "SELECT id FROM codicoes WHERE descricao = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(select_query, (nome_condicao,))
            id_condicao = cursor.fetchone()
            return id_condicao[0] if id_condicao else None
        except sqlite3.Error as error:
            print("Falha ao obter ID da condição", error)
        finally:
            if self.connection:
                cursor.close()
                self.connection.close()
                print("A conexão com o banco de dados foi fechada")

    def obter_id_status_por_nome(self, nome_status):
        self.abrirConexao()
        select_query = "SELECT id FROM status WHERE descricao = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(select_query, (nome_status,))
            id_status = cursor.fetchone()
            return id_status[0] if id_status else None
        except sqlite3.Error as error:
            print("Falha ao obter ID do status", error)
        finally:
            if self.connection:
                cursor.close()
                self.connection.close()
                print("A conexão com o banco de dados foi fechada")

    def obter_despesas_e_status(self):
        self.abrirConexao()
        select_query = """SELECT despesas.valor, status.descricao as status
                        FROM despesas
                        INNER JOIN status ON despesas.id_status = status.id"""
        despesas_status = []
        try:
            cursor = self.connection.cursor()
            cursor.execute(select_query)
            despesas_status = cursor.fetchall()
        except sqlite3.Error as error:
            print("Falha ao retornar despesas e status", error)
        finally:
            self.fecharConexao()
        return despesas_status
