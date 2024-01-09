# Aplicação de Loja em Python
Este repositório contém uma aplicação simples de loja implementada em Python. A aplicação é destinada a gerenciar produtos, clientes e compras, com a persistência de dados em um banco de dados SQLite. A interface gráfica é construída utilizando Tkinter.

# Estrutura do Projeto
## O projeto está organizado da seguinte forma:

loja.py: Arquivo principal contendo as classes principais da aplicação.
loja.db: Banco de dados SQLite para armazenar dados da aplicação.

# Funcionalidades Principais
## Classes de Entidades
## Produto:

Representa um produto com código, nome, descrição e preço.
from_database método de classe utilizado para criar instâncias a partir dos dados do banco.

## Cliente:
Representa um cliente com nome, endereço e telefone.
Possui o método atualizar_info para modificar informações do cliente.

## Compra:
Representa uma compra associada a um cliente.
gravar_no_banco método utilizado para registrar a compra no banco de dados.

## DatabaseManager:
Gerencia a interação com o banco de dados SQLite.
Fornece métodos para executar consultas e criar tabelas.
Lida com tratamento de exceções durante operações no banco de dados.

## Loja:
Gerencia operações relacionadas a produtos, clientes e compras.
Utiliza o DatabaseManager para interação com o banco de dados.
Implementa uma interface gráfica simples utilizando Tkinter.

## Uso da Aplicação
Execute o arquivo loja.py.
Insira o usuário e senha quando solicitado (usuário e senha hardcoded para fins de exemplo).
Utilize a interface gráfica para cadastrar produtos, clientes, realizar compras e visualizar informações.

# Aspectos a Considerar
## Autenticação de Usuário:
A lógica de autenticação é básica (usuário e senha hardcoded). Em uma aplicação real, recomenda-se implementar um sistema de autenticação mais robusto.

## Segurança:
Ao implementar o código, certifique-se também de implementar medidas adicionais de segurança, especialmente em ambientes de produção.

## Visualização Detalhada de Compras:
Adição de funcionalidade para visualizar detalhes específicos de uma compra, como produtos associados, pode ser uma melhoria futura.

## Tratamento de Exceções:
O código inclui tratamento de exceções para erros no banco de dados, garantindo uma resposta adequada em caso de problemas durante as operações.

# Contribuição:
## Contribuições são bem-vindas! Sinta-se à vontade para propor melhorias, correções de bugs ou novas funcionalidades.

