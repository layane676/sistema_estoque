from datetime import datetime

from banco import transacao


def movimentar_estoque(produto_id, tipo, quantidade):
    with transacao() as conexao:
        conexao.execute("BEGIN IMMEDIATE")
        produto = conexao.execute(
            "SELECT quantidade, estoque_maximo FROM produtos WHERE id = ?",
            (produto_id,),
        ).fetchone()
        if produto is None:
            return None

        saldo = produto["quantidade"]
        novo_saldo = saldo + quantidade if tipo == "Entrada" else saldo - quantidade
        if novo_saldo < 0:
            raise ValueError("Não há estoque suficiente para essa saída.")
        if novo_saldo > produto["estoque_maximo"]:
            raise ValueError("A movimentação ultrapassa o estoque máximo do produto.")

        conexao.execute(
            "UPDATE produtos SET quantidade = ? WHERE id = ?",
            (novo_saldo, produto_id),
        )
        conexao.execute("""
            INSERT INTO movimentacoes (produto_id, tipo, quantidade, data_hora)
            VALUES (?, ?, ?, ?)
        """, (
            produto_id,
            tipo,
            quantidade,
            datetime.now().astimezone().isoformat(timespec="seconds"),
        ))
        return novo_saldo


def listar_movimentacoes(limite=100):
    with transacao() as conexao:
        linhas = conexao.execute("""
            SELECT movimentacoes.id, movimentacoes.tipo, movimentacoes.quantidade,
                   movimentacoes.data_hora, produtos.id AS produto_id, produtos.nome
            FROM movimentacoes
            JOIN produtos ON produtos.id = movimentacoes.produto_id
            ORDER BY movimentacoes.id DESC
            LIMIT ?
        """, (limite,)).fetchall()
        return [dict(linha) for linha in linhas]