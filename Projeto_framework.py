from itertools import count
from tkinter.tix import NoteBook
from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
import pydantic
from functools import reduce

from Projeto1 import OK

db_usuarios = {}
db_produtos = {}
db_end = {}        
db_carrinhos = {}

app = FastAPI()

@app.get("/")
async def bem_vinda():
    site = "Seja bem vinda"
    return site.replace('\n', '')

class Endereco(pydantic.BaseModel):
    id : int
    rua: str
    cep: str
    cidade: str
    estado: str

class Usuario(pydantic.BaseModel):
    id: int
    nome: str
    email: str
    senha: str

class ListaDeEnderecosDoUsuario(pydantic.BaseModel):
    usuario: Usuario
    enderecos: List[Endereco] = []

class Produto(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: float


class CarrinhoDeCompras(BaseModel):
    id_usuario: int
    id_produtos: list
    preco_total: float
    quantidade_de_produtos: int

#Cadastrar usuário de modo que se já existir um id igual a o que deseja ser cadastrado retornar erro
#caso o usuário colocar o email sem @ retornar falha
#caso a senha tenha menos de 3 digitos retornar falha
@app.post("/usuario")
def criar_usuário(usuario: Usuario):
    if usuario.id in db_usuarios:
        return 'FALHA'
    elif not '@' in usuario.email:
        return 'FALHA'
    elif len(usuario.senha) < 3:
        return'falha'
    db_usuarios[usuario.id] = usuario
    return 'OK'            

#consultar usuário pelo seu id caso id inexistente retornar falha    
@app.get("/usuario/{id}")
async def retornar_usuario(id: int):
    if id in db_usuarios:
        return db_usuarios[id]
    return 'FALHA'

#pesquisar usuário pelo nome caso não exista retornar falha
@app.get("/usuario/{nome}")
async def retornar_usuario_com_nome(nome: str):
    if nome in db_usuarios:
        return db_usuarios[nome]
    else:
        return 'Falha'


#caso id do usuario existir deletar, se não retornar falha
@app.delete("/usuario/{id}")
async def deletar_usuario(id: int):
    if id in db_usuarios:
        del db_usuarios[id]
        return 'OK'
    else:
        return 'Falha'

#cadastrar endereço do usuario, caso id não existir retornar falha
@app.post("/usuario/endereco")
async def criar_endereco(endereco:Endereco):
        if endereco.id  not in db_usuarios:
            return 'Falha'
        else:
            db_carrinhos[endereco.id] = endereco
      
#pesquisar endereços do usuário, caso não existir retornar lista vazia
@app.get("/usuario/endereco/{id}")
async def retornar_enderecos_do_usuario(id:int):
    if id in db_carrinhos:
        return db_carrinhos[id]
    else:
        return []

#remover endereço do usuário apartir do seu id, caso o id não esteja cadastrado retornar falha
@app.delete("/usuario/endereco/{id}")
async def deletar_endereco(id: int):
    if id not in db_carrinhos:
        return 'Falha'
    else:  del db_carrinhos[id]

#cadastrar produto
@app.post("/produto/")
async def criar_produto(produto: Produto):
    if produto.id in db_produtos:
        return 'FALHA'
    else:
        db_produtos[produto.id] = produto
        return 'ok'

#remover produto apartir do seu id
@app.delete("/produto/{id}/")
async def deletar_produto(id: int):
    if id not in db_produtos:
        return 'Falha'
    else:  del db_produtos[id]
    return 'ok'   


#Criar carrinho e adicionar produtos
@app.post("/carrinho/")
async def criar_carrinho(carrinho: CarrinhoDeCompras):
    if carrinho.id_usuario in db_produtos:
        return 'FALHA'
    else:
        db_carrinhos[carrinho.id_usuario] = carrinho
        return db_carrinhos

#apagar produto do carrinho
# @app.post("/carrinho/{id_produto}")
# async def deletar_produto(carrinho:CarrinhoDeCompras):
#     a=0
#     if carrinho.id_produtos == '':
#         return 'falha'
#     else:  
#         for carrinho.id_produtos in db_carrinhos:
#             db_carrinhos[a][2]='' 
#             a = a +1   
#             return print(db_carrinhos)


#remover carrinho
@app.delete("/carrinho/{id_usuario}")
async def deletar_carrinho(id_usuario: int):
    if id_usuario not in db_carrinhos:
        return 'falha'
    else:  del db_carrinhos[id_usuario]
    return 'ok'


#calcular valor total do carrinho
# @app.get("/carrinho/{id_usuario}")
# async def retornar_total_carrinho(int: int,carrinho: CarrinhoDeCompras):
#     if int not in db_carrinhos:
#         return 'Falha'
#     else:
#         valor_total = carrinho.preco_total
#     return valor_total


