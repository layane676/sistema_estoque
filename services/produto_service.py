import math
import sqlite3

from repositories import produto_repository


def _inteiro(valor, campo):
    try:
        numero = int(valor)
    except (TypeError, ValueError):
        raise ValueError(f"{campo} deve ser um número inteiro.") from None
    if numero < 0:
        raise ValueError(f"{campo} não pode ser negativo.")
    return numero


def _dados_produto(nome, valor, quantidade, estoque_minimo, estoque_maximo):
    nome = (nome or "").strip()
    if not nome:
        raise ValueError("Informe o nome do produto.")

    try:
        valor = float(valor)
    except (TypeError, ValueError):
        raise ValueError("O valor deve ser um número válido.") from None
    if not math.isfinite(valor) or valor < 0:
        raise ValueError("O valor não pode ser negativo.")

    quantidade = _inteiro(quantidade, "Quantidade")
    estoque_minimo = _inteiro(estoque_minimo, "Estoque mínimo")
    estoque_maximo = _inteiro(estoque_maximo, "Estoque máximo")
    if estoque_minimo > estoque_maximo:
        raise ValueError("O estoque mínimo não pode superar o estoque máximo.")
    if quantidade > estoque_maximo:
        raise ValueError("A quantidade em estoque não pode superar o estoque máximo.")

    return {
        "nome": nome,
        "valor": valor,
        "quantidade": quantidade,
        "estoque_minimo": estoque_minimo,
        "estoque_maximo": estoque_maximo,
    }


def listar_produtos():
    return produto_repository.listar_produtos()


def obter_produto(produto_id):
    return produto_repository.buscar_produto(produto_id)


def criar_produto(nome, valor, quantidade, estoque_minimo, estoque_maximo):
    produto = _dados_produto(nome, valor, quantidade, estoque_minimo, estoque_maximo)
    try:
        return produto_repository.criar_produto(produto)
    except sqlite3.IntegrityError as erro:
        if "produtos.nome" in str(erro):
            raise ValueError("Já existe um produto com esse nome.") from None
        raise


def atualizar_produto(produto_id, nome, valor, estoque_minimo, estoque_maximo):
    atual = obter_produto(produto_id)
    if atual is None:
        return False
    produto = _dados_produto(
        nome, valor, atual["quantidade"], estoque_minimo, estoque_maximo
    )
    try:
        return produto_repository.atualizar_produto(produto_id, produto)
    except sqlite3.IntegrityError as erro:
        if "produtos.nome" in str(erro):
            raise ValueError("Já existe um produto com esse nome.") from None
        raise


def excluir_produto(produto_id):
    try:
        return produto_repository.excluir_produto(produto_id)
    except sqlite3.IntegrityError:
        raise ValueError(
            "Este produto possui movimentações e não pode ser excluído."
        ) from None