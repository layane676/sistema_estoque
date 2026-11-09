from repositories import estoque_repository


def movimentar_estoque(produto_id, tipo, quantidade):
    if tipo not in ("Entrada", "Saída"):
        raise ValueError("Selecione entrada ou saída.")
    try:
        quantidade = int(quantidade)
    except (TypeError, ValueError):
        raise ValueError("A quantidade deve ser um número inteiro.") from None
    if quantidade <= 0:
        raise ValueError("A quantidade movimentada deve ser maior que zero.")
    return estoque_repository.movimentar_estoque(produto_id, tipo, quantidade)


def listar_movimentacoes(limite=100):
    return estoque_repository.listar_movimentacoes(limite)