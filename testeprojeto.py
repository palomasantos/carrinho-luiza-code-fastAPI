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
def rota_raiz():
    return {
        "ok": True,
        "versao": "Fase 1"
    }

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

class ListaDeEnderecosDoUsuario(BaseModel):
    usuario: Usuario
    enderecos: List[Endereco] = []

class Produto(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: float

# Classe representando o carrinho de compras de um cliente com uma lista de produtos
class CarrinhoDeCompras(BaseModel):
    id_usuario: int
    id_produtos: List[Produto] = []
    preco_total: float
    quantidade_de_produtos: int

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
    
@app.get("/usuario/{id}")
async def retornar_usuario(id: int):
    if id in db_usuarios:
        return db_usuarios[id]
    return 'FALHA'

@app.get("/usuario/{nome}")
async def retornar_usuario_com_nome(nome: str):
    if nome in db_usuarios:
        return db_usuarios[nome]
    else:
        return 'Falha'

@app.delete("/usuario/{id}")
async def deletar_usuario(id: int):
    if id in db_usuarios:
        return OK
    else:
        return 'bad'
### NÃO ESTOU CONSEGUINDO FAZER ESSA PARTE   
@app.get("/usuarios/emails/")
async def retornar_emails(dominio: str):
    return FALHA

@app.post("/usuario/endereco")
async def criar_endereco(endereco:Endereco):
        if endereco.id  not in db_usuarios:
            return 'Falha'
        else:
            db_carrinhos[endereco.id] = endereco
      

@app.get("/usuario/endereco/{id}")
async def retornar_enderecos_do_usuario(id:int):
    if id in db_carrinhos:
        return db_carrinhos[id]
    else:
        return []

@app.delete("/usuario/endereco/{id}")
async def deletar_endereco(id: int):
    if id not in db_carrinhos:
        return 'Falha'
    else:  del db_carrinhos[id]

@app.post("/produto/")
async def criar_produto(produto: Produto):
    if produto.id in db_produtos:
        return 'FALHA'
    else:
        db_produtos[produto.id] = produto
        return 'ok'

@app.delete("/produto/{id}/")
async def deletar_produto(id: int):
    if id not in db_produtos:
        return 'Falha'
    else:  del db_produtos[id]
    return 'ok'   


@app.post("/carrinho/{d_usuario}/{id_produto}/")
async def adicionar_carrinho(id_usuario: int, id_produto: int,carrinho: CarrinhoDeCompras):
    if id_produto not in db_produtos or id_usuario not in db_carrinhos:
        return 'Falha'

@app.get("/carrinho/{id_usuario}/")
async def retornar_carrinho(id_usuario: int):
    if id_usuario not in db_carrinhos:
        return 'Falha'
    else:
        return db_carrinhos[id_usuario]


@app.get("/carrinho/{id_usuario}/")
async def retornar_total_carrinho(id_usuario: int,carrinho: CarrinhoDeCompras):
    if id_usuario not in db_carrinhos:
        return 'Falha'
    else:
        numero_itens = carrinho.quantidade_de_produtos
        valor_total = carrinho.preco_total
    return numero_itens, valor_total

@app.delete("/carrinho/{id_usuario}/")
async def deletar_carrinho(id_usuario: int):
    if id_usuario not in db_carrinhos:
        return 'falha'
    else:  del db_carrinhos[id_usuario]
    return 'ok'
