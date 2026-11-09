from banco import transacao


def listar_produtos():
    with transacao() as conexao:
        linhas = conexao.execute(
            "SELECT * FROM produtos ORDER BY nome COLLATE NOCASE"
        ).fetchall()
        return [dict(linha) for linha in linhas]


def buscar_produto(produto_id):
    with transacao() as conexao:
        produto = conexao.execute(
            "SELECT * FROM produtos WHERE id = ?", (produto_id,)
        ).fetchone()
        return dict(produto) if produto else None


def criar_produto(produto):
    with transacao() as conexao:
        cursor = conexao.execute("""
            INSERT INTO produtos (nome, valor, quantidade, estoque_minimo, estoque_maximo)
            VALUES (:nome, :valor, :quantidade, :estoque_minimo, :estoque_maximo)
        """, produto)
        return cursor.lastrowid


def atualizar_produto(produto_id, produto):
    with transacao() as conexao:
        cursor = conexao.execute("""
            UPDATE produtos
            SET nome = :nome, valor = :valor,
                estoque_minimo = :estoque_minimo, estoque_maximo = :estoque_maximo
            WHERE id = :id
        """, {**produto, "id": produto_id})
        return cursor.rowcount > 0


def excluir_produto(produto_id):
    with transacao() as conexao:
        cursor = conexao.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
        return cursor.rowcount > 0
