import sqlite3
from tkinter import Tk, Label, Button, Entry, StringVar, Listbox, END
from typing import List
from sqlite3 import DatabaseError

class Produto:
    def __init__(self, codigo: int, nome: str, descricao: str, preco: float):
        self.codigo = codigo
        self.nome = nome
        self.descricao = descricao
        self.preco = preco

    @classmethod
    def from_database(cls, codigo, nome, descricao, preco):
        return cls(codigo, nome, descricao, preco)

class Cliente:
    def __init__(self, nome: str, endereco: str, telefone: str):
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone

    def atualizar_info(self, novo_endereco: str, novo_telefone: str):
        self.endereco = novo_endereco
        self.telefone = novo_telefone

class Compra:
    def __init__(self, codigo: int, cliente: Cliente):
        self.codigo = codigo
        self.cliente = cliente
        self.produtos: List[Produto] = []

    def gravar_no_banco(self, conn: sqlite3.Connection) -> None:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Compras (codigo, cliente_nome) VALUES (?, ?)", (self.codigo, self.cliente.nome))
            for produto in self.produtos:
                cursor.execute("INSERT INTO Compra_Produtos (compra_codigo, produto_codigo) VALUES (?, ?)",
                               (self.codigo, produto.codigo))
            conn.commit()
            print("Compra registrada com sucesso!")
        except sqlite3.Error as e:
            print(f"Erro ao gravar compra no banco de dados: {e}")
            conn.rollback()
            raise DatabaseError(str(e))
        except Exception as e:
            print(f"Erro desconhecido ao gravar compra: {e}")
            raise

class DatabaseManager:
    def __init__(self, database_path: str):
        self.database_path = database_path

    def execute_query(self, query: str, values: tuple) -> None:
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, values)
                conn.commit()
                print("Operação concluída com sucesso.")
            except sqlite3.Error as e:
                print(f"Erro ao executar a query: {e}")
                conn.rollback()
                raise DatabaseError(str(e))
            except Exception as e:
                print(f"Erro desconhecido: {e}")
                raise
            finally:
                cursor.close()

    def create_tables(self) -> None:
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            try:
                # Criação das tabelas
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Produtos (
                        codigo INTEGER PRIMARY KEY,
                        nome TEXT,
                        descricao TEXT,
                        preco REAL
                    )
                ''')
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Clientes (
                        nome TEXT PRIMARY KEY,
                        endereco TEXT,
                        telefone TEXT
                    )
                ''')
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Compras (
                        codigo INTEGER PRIMARY KEY,
                        cliente_nome TEXT,
                        FOREIGN KEY (cliente_nome) REFERENCES Clientes (nome)
                    )
                ''')
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Compra_Produtos (
                        compra_codigo INTEGER,
                        produto_codigo INTEGER,
                        FOREIGN KEY (compra_codigo) REFERENCES Compras (codigo),
                        FOREIGN KEY (produto_codigo) REFERENCES Produtos (codigo)
                    )
                ''')
                conn.commit()
            except sqlite3.Error as e:
                print(f"Erro ao criar tabelas: {e}")
                conn.rollback()
                raise DatabaseError(str(e))
            except Exception as e:
                print(f"Erro desconhecido: {e}")
                raise
            finally:
                cursor.close()

class Loja:
    def __init__(self, nome: str, endereco: str, telefone: str, database_path: str):
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.lista_produtos: List[Produto] = []
        self.lista_clientes: List[Cliente] = []
        self.database_path = database_path
        self.db_manager = DatabaseManager(database_path)
        self.db_manager.create_tables()
        self.lista_produtos = self.obter_produtos_do_banco()

    def autenticar_usuario(self) -> bool:
        usuario = input("Digite o usuário: ")
        senha = input("Digite a senha: ")

        # Lógica de autenticação (apenas exemplo, ajuste conforme necessidade)
        return usuario == "ADMIN" and senha == "AÇAÍ"

    def cadastrar_produto(self) -> None:
        codigo = int(input("Digite o código do produto: "))
        nome = input("Digite o nome do produto: ")
        descricao = input("Digite a descrição do produto: ")
        preco = float(input("Digite o preço do produto: "))
        produto = Produto(codigo=codigo, nome=nome, descricao=descricao, preco=preco)

        self.lista_produtos.append(produto)
        self.db_manager.execute_query("INSERT INTO Produtos (codigo, nome, descricao, preco) VALUES (?, ?, ?, ?)",
                                      (produto.codigo, produto.nome, produto.descricao, produto.preco))

    def atualizar_produto(self) -> None:
        codigo = int(input("Digite o código do produto a ser atualizado: "))
        nome = input("Digite o novo nome do produto: ")
        descricao = input("Digite a nova descrição do produto: ")
        preco = float(input("Digite o novo preço do produto: "))

        self.db_manager.execute_query("UPDATE Produtos SET nome=?, descricao=?, preco=? WHERE codigo=?",
                                      (nome, descricao, preco, codigo))

    def excluir_produto(self) -> None:
        codigo = int(input("Digite o código do produto a ser excluído: "))

        self.db_manager.execute_query("DELETE FROM Produtos WHERE codigo=?", (codigo,))
        self.lista_produtos = [produto for produto in self.lista_produtos if produto.codigo != codigo]

    def cadastrar_cliente(self) -> None:
        nome = input("Digite o nome do cliente: ")
        endereco = input("Digite o endereço do cliente: ")
        telefone = input("Digite o telefone do cliente: ")

        self.db_manager.execute_query("INSERT INTO Clientes (nome, endereco, telefone) VALUES (?, ?, ?)",
                                      (nome, endereco, telefone))

    def atualizar_cliente(self) -> None:
        nome_cliente = input("Digite o nome do cliente a ser atualizado: ")
        if not self.cliente_existe(nome_cliente):
            print("Cliente não encontrado.")
            return

        novo_endereco = input("Digite o novo endereço do cliente: ")
        novo_telefone = input("Digite o novo telefone do cliente: ")

        self.atualizar_cliente_na_lista(nome_cliente, novo_endereco, novo_telefone)

        self.db_manager.execute_query("UPDATE Clientes SET endereco=?, telefone=? WHERE nome=?",
                                      (novo_endereco, novo_telefone, nome_cliente))
        print("Informações do cliente atualizadas com sucesso!")

    def cliente_existe(self, nome_cliente: str) -> bool:
        conn = sqlite3.connect(self.database_path)
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT nome FROM Clientes WHERE nome=?", (nome_cliente,))
            return cursor.fetchone() is not None
        finally:
            conn.close()

    def atualizar_cliente_na_lista(self, nome_cliente: str, novo_endereco: str, novo_telefone: str) -> None:
        for cliente in self.lista_clientes:
            if cliente.nome == nome_cliente:
                cliente.atualizar_info(novo_endereco, novo_telefone)
                break

    def registrar_compra(self) -> None:
        cliente_nome = input("Digite o nome do cliente: ")
        produtos = self.obter_produtos_do_banco()
        compra = Compra(codigo=len(produtos) + 1, cliente=Cliente(nome=cliente_nome, endereco="", telefone=""))
        compra.produtos = produtos

        self.lista_produtos.extend(compra.produtos)

        with sqlite3.connect(self.database_path) as conn:
            compra.gravar_no_banco(conn)
        print("Compra registrada com sucesso!")

        self.lista_produtos = self.obter_produtos_do_banco()

    def obter_produtos_do_banco(self) -> List[Produto]:
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT codigo, nome, descricao, preco FROM Produtos")
            produtos_from_db = cursor.fetchall()

        produtos = [Produto.from_database(*produto) for produto in produtos_from_db]

        return produtos

    def visualizar_produtos(self) -> None:
        print("\nPRODUTOS CADASTRADOS:")
        for produto in self.lista_produtos:
            print(f"{produto.codigo}: {produto.nome} - {produto.preco}")

    def visualizar_clientes(self) -> None:
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nome, endereco, telefone FROM Clientes")
            clientes_from_db = cursor.fetchall()

        print("\nCLIENTES CADASTRADOS:")
        for cliente in clientes_from_db:
            nome, endereco, telefone = cliente
            print(f"{nome} - {endereco} - {telefone}")

    def visualizar_compras(self) -> None:
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT codigo, cliente_nome FROM Compras")
            compras_from_db = cursor.fetchall()

        print("\nCOMPRAS REGISTRADAS:")
        for compra in compras_from_db:
            codigo, cliente_nome = compra
            print(f"Código: {codigo} - Cliente: {cliente_nome}")

    def run(self):
        if not self.autenticar_usuario():
            print("Autenticação falhou. Saindo.")
            return

        root = Tk()
        root.title("Loja Açaí do Marujo")

        label = Label(root, text="Bem-vindo à Loja Açaí do Marujo", font=("Helvetica", 16))
        label.grid(row=0, column=0, columnspan=2)


        button_cadastrar_produto = Button(root, text="Cadastrar Produto", command=self.cadastrar_produto)
        button_cadastrar_produto.grid(row=1, column=0)

        button_atualizar_produto = Button(root, text="Atualizar Produto", command=self.atualizar_produto)
        button_atualizar_produto.grid(row=1, column=1)

        button_excluir_produto = Button(root, text="Excluir Produto", command=self.excluir_produto)
        button_excluir_produto.grid(row=2, column=0)

        button_cadastrar_cliente = Button(root, text="Cadastrar Cliente", command=self.cadastrar_cliente)
        button_cadastrar_cliente.grid(row=2, column=1)

        button_atualizar_cliente = Button(root, text="Atualizar Cliente", command=self.atualizar_cliente)
        button_atualizar_cliente.grid(row=3, column=0)

        button_registrar_compra = Button(root, text="Registrar Compra", command=self.registrar_compra)
        button_registrar_compra.grid(row=3, column=1)

        button_visualizar_produtos = Button(root, text="Visualizar Produtos", command=self.visualizar_produtos)
        button_visualizar_produtos.grid(row=4, column=0)

        button_visualizar_clientes = Button(root, text="Visualizar Clientes", command=self.visualizar_clientes)
        button_visualizar_clientes.grid(row=4, column=1)

        button_visualizar_compras = Button(root, text="Visualizar Compras", command=self.visualizar_compras)
        button_visualizar_compras.grid(row=5, column=0)

        button_sair = Button(root, text="Sair", command=root.destroy)
        button_sair.grid(row=5, column=1)

        root.mainloop()

if __name__ == "__main__":
    try:
        database_path = 'loja.db'
        loja = Loja(nome="Açaí do Marujo", endereco="Av. Principal, 123", telefone="972262615", database_path=database_path)
        loja.run()
    except DatabaseError as e:
        print(f"Erro no banco de dados ao iniciar a loja: {e}")
    except Exception as e:
        print(f"Erro desconhecido ao iniciar a loja: {e}")
