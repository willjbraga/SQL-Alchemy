# Exemplo de CRUD com SQLAlchemy (Estilo 2.0)

Este projeto é um exemplo simples de como usar **SQLAlchemy** para:

- Criar um banco de dados SQLite
- Definir modelos (tabelas) usando o estilo declarativo moderno (`DeclarativeBase`, `Mapped`, `mapped_column`)
- Criar relações 1:N entre tabelas (`Usuario` → `Livro`)
- Executar operações básicas de **CRUD** (Create, Read, Update, Delete)

O foco é **entender a estrutura** e ter um código que sirva como base para projetos pequenos ou para estudo.

---

## Tecnologias utilizadas

- Python 3.10+ (recomendado)
- [SQLAlchemy 2.x](https://docs.sqlalchemy.org/)
- SQLite (banco em arquivo local, sem precisar instalar servidor)

---

## Estrutura do arquivo

Todo o código está em um único arquivo Python (por exemplo, `main.py`), organizado em 5 blocos principais:

1. Configuração do banco de dados e sessão
2. Definição da classe base (`Base`)
3. Modelos de banco de dados (`Usuario` e `Livro`)
4. Criação das tabelas
5. Exemplo prático de CRUD (no bloco `if __name__ == "__main__":`)

---

## 1. Configuração do banco e sessão

### `engine`

```python
engine = create_engine(
    "sqlite:///meubanco.db",
    echo=False,
    future=True,
)
