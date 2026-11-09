from contextlib import contextmanager
from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).resolve().with_name("estoque.db")


def conectar():
    conexao = sqlite3.connect(DB_PATH)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


@contextmanager
def transacao():
    conexao = conectar()
    try:
        yield conexao
        conexao.commit()
    except Exception:
        conexao.rollback()
        raise
    finally:
        conexao.close()


def criar_banco():
    conexao = conectar()
    try:
        conexao.executescript("""
            CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            login TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            perfil TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            valor REAL NOT NULL,
            quantidade INTEGER NOT NULL,
            estoque_minimo INTEGER NOT NULL,
            estoque_maximo INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            data_hora TEXT NOT NULL,
            FOREIGN KEY(produto_id) REFERENCES produtos(id) ON DELETE RESTRICT
            );
        """)
        conexao.executemany("""
            INSERT OR IGNORE INTO usuarios (nome, login, senha, perfil)
            VALUES (?, ?, ?, ?)
        """, [
            ("Administrador", "admin", "123", "Administrador"),
            ("Operador", "operador", "123", "Operador"),
        ])
        conexao.commit()
    finally:
        conexao.close()
