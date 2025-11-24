from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base 

#create engine é ele que cria o banco de dados. Ele conecta com o banco de dados caso ele já exista
#model geralmente é a definição das tabelas

#como funciona: 
# 1 - você abre uma sessão 
# 2 - edita 
# 3 - commita para salvar 
# 4 - fecha a conexão


db = create_engine("sqlite:///meubanco.db")

#O bind é o banco ou o nome dele
#Aqui você cria a sessão e carrega ela em session
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

#criação das tabelas

#Tabela Usuario
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome =  Column("nome", String)
    email = Column("email", String)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)

    def __init__(self, nome, email, senha, ativo=True):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
    
#Livros
class Livro(Base):
    __tablename__ = "livros"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    titulo = Column("titulo", String)
    qtd_paginas = Column("qtde_paginas", Integer)
    dono = Column("dono", ForeignKey("usuarios.id"))

    def __init__(self, titulo, qtd_paginas, dono):
        self.titulo = titulo
        self.qtd_paginas = qtd_paginas
        self.dono = dono

Base.metadata.create_all(bind=db)

#create_engine("Lik do banco de dados com usuario e senha")

#---------------------------------------------------------------------------------------------------------------------------------
# CRUD
# Create
# Read
# Update
# Delete

# C - Create
# Com criate basta criar uma instancia do Usuario com a variavel usuario adicionar ela na sessão e commitar para fazer um create Usuario
usuario = Usuario(nome="Lira", email="123@gmail.com", senha="123123")
session.add(usuario)
session.commit()

# R - Read
# os métodos query().all() sempre retornam uma lista
lista_usuario = session.query(Usuario).all()


# Para pegar um usuario especifico é usado o filter_by()
usuario_especifico = session.query(Usuario).filter_by(email="123@gmail.com").first()
print(usuario_especifico.nome)

#Para criar um livro com um usuário especifico 
livro = Livro(titulo="Nome do Vento", qtd_paginas="200", dono=usuario_especifico.id)

# U - Update
# Atualizando o nome de um usuário que ja foi lido
usuario_especifico.nome = "Willinelson"
session.add(usuario_especifico)
session.commit

# D - Delete
session.delete(usuario_especifico)
session.delete
session.commit