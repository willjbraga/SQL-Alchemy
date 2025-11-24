from __future__ import annotations  # permite usar tipos entre aspas (forward references)
from typing import List

from sqlalchemy import create_engine, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
    Session,
)

# ------------------------------------------------------------------------------
# 1. CONFIGURAÇÃO BÁSICA DO BANCO E SESSÃO
# ------------------------------------------------------------------------------

# create_engine:
# - Cria a "conexão" com o banco de dados.
# - Se o arquivo SQLite não existir, ele é criado automaticamente.
engine = create_engine(
    "sqlite:///meubanco.db",
    echo=False,  # coloque True para ver os SQLs gerados no console
    future=True,
)


# SessionLocal:
# - Fabrica de sessões.
# - Cada Session é uma "conversa" com o banco: você abre, usa, faz commit/rollback e fecha.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,   # evita flush automático fora de hora
    autocommit=False,  # sempre controlar o commit na mão
    expire_on_commit=False,
)


# Base:
# - Classe base para todos os modelos declarativos.
class Base(DeclarativeBase):
    pass


# ------------------------------------------------------------------------------
# 2. MODELOS (TABELAS)
# ------------------------------------------------------------------------------

class Usuario(Base):
    """
    Representa a tabela 'usuarios'.

    Cada instância de Usuario é uma linha na tabela.
    """
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,     # não permite dois usuários com o mesmo e-mail
        nullable=False,
    )
    senha: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    ativo: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # relação 1:N -> um usuário pode ter vários livros
    livros: Mapped[List["Livro"]] = relationship(
        back_populates="dono",
        cascade="all, delete-orphan",  # se apagar o usuário, apaga os livros dele também
    )

    def __repr__(self) -> str:
        return f"Usuario(id={self.id}, nome={self.nome!r}, email={self.email!r})"


class Livro(Base):
    """
    Representa a tabela 'livros'.

    Cada Livro pertence a um Usuario via chave estrangeira.
    """
    __tablename__ = "livros"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    titulo: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    # Mantendo o nome da coluna física 'qtde_paginas' como no seu exemplo,
    # mas o atributo Python permanece 'qtd_paginas' para ficar mais legível.
    qtd_paginas: Mapped[int] = mapped_column(
        "qtde_paginas",
        Integer,
        nullable=False,
    )

    dono_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False,
    )

    # relação N:1 -> cada livro tem um único dono (Usuario)
    dono: Mapped[Usuario] = relationship(
        back_populates="livros",
    )

    def __repr__(self) -> str:
        return f"Livro(id={self.id}, titulo={self.titulo!r}, dono_id={self.dono_id})"


# ------------------------------------------------------------------------------
# 3. CRIAÇÃO DAS TABELAS
# ------------------------------------------------------------------------------

# Cria as tabelas no banco (se ainda não existirem)
Base.metadata.create_all(bind=engine)


# ------------------------------------------------------------------------------
# 4. FUNÇÃO AUXILIAR PARA OBTER SESSÃO
# ------------------------------------------------------------------------------

def get_session() -> Session:
    """
    Cria e retorna uma nova sessão de banco de dados.

    Use sempre com 'with' para garantir fechamento correto:
        with get_session() as session:
            ...
    """
    return SessionLocal()


# ------------------------------------------------------------------------------
# 5. EXEMPLO DE USO: CRUD
# ------------------------------------------------------------------------------

if __name__ == "__main__":

    # C - CREATE ---------------------------------------------------------------
    with get_session() as session:
        # Criando um usuário
        usuario = Usuario(
            nome="Lira",
            email="123@gmail.com",
            senha="123123",
        )
        session.add(usuario)
        session.commit()
        session.refresh(usuario)  # atualiza o objeto com o id gerado no banco

        # Criando um livro para esse usuário
        livro = Livro(
            titulo="Nome do Vento",
            qtd_paginas=200,  # agora é int, não string ;)
            dono=usuario,     # você pode passar o objeto Usuario diretamente
        )
        session.add(livro)
        session.commit()

    # R - READ -----------------------------------------------------------------
    with get_session() as session:
        # .all() sempre retorna uma lista
        lista_usuarios = session.query(Usuario).all()
        print("Usuários cadastrados:", lista_usuarios)

        # Pegando um usuário específico com filter_by().first()
        usuario_especifico = (
            session.query(Usuario)
            .filter_by(email="123@gmail.com")
            .first()
        )

        if usuario_especifico:
            print("Usuário encontrado:", usuario_especifico.nome)

            # Livros desse usuário (graças ao relationship)
            print("Livros do usuário:", usuario_especifico.livros)

    # U - UPDATE ---------------------------------------------------------------
    with get_session() as session:
        usuario_especifico = (
            session.query(Usuario)
            .filter_by(email="123@gmail.com")
            .first()
        )

        if usuario_especifico:
            usuario_especifico.nome = "Willinelson"
            session.commit()  # aqui precisa dos parênteses!

    # D - DELETE ---------------------------------------------------------------
    with get_session() as session:
        usuario_especifico = (
            session.query(Usuario)
            .filter_by(email="123@gmail.com")
            .first()
        )

        if usuario_especifico:
            # Deleta o usuário (e, por causa do cascade, os livros dele também)
            session.delete(usuario_especifico)
            session.commit()
