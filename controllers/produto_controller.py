from flask import Blueprint, flash, redirect, render_template, request, url_for

from controllers.auth_controller import login_required
from services import produto_service


produto_bp = Blueprint("produtos", __name__)


def _pagina_produtos(produto_edicao=None):
    return render_template(
        "produtos.html",
        produtos=produto_service.listar_produtos(),
        produto_edicao=produto_edicao,
    )


@produto_bp.route("/produtos", methods=["GET"])
@login_required
def listar():
    return _pagina_produtos()


@produto_bp.route("/produtos", methods=["POST"])
@login_required
def criar():
    try:
        produto_service.criar_produto(
            request.form.get("nome"),
            request.form.get("valor"),
            request.form.get("quantidade"),
            request.form.get("estoque_minimo"),
            request.form.get("estoque_maximo"),
        )
        flash("Produto cadastrado com sucesso.", "sucesso")
    except ValueError as erro:
        flash(str(erro), "erro")
    return redirect(url_for("produtos.listar"))


@produto_bp.route("/produtos/<int:produto_id>/editar", methods=["GET"])
@login_required
def editar(produto_id):
    produto = produto_service.obter_produto(produto_id)
    if produto is None:
        flash("Produto não encontrado.", "erro")
        return redirect(url_for("produtos.listar"))
    return _pagina_produtos(produto_edicao=produto)


@produto_bp.route("/produtos/<int:produto_id>/atualizar", methods=["POST"])
@login_required
def atualizar(produto_id):
    try:
        atualizado = produto_service.atualizar_produto(
            produto_id,
            request.form.get("nome"),
            request.form.get("valor"),
            request.form.get("estoque_minimo"),
            request.form.get("estoque_maximo"),
        )
        if atualizado:
            flash("Produto atualizado com sucesso.", "sucesso")
        else:
            flash("Produto não encontrado.", "erro")
    except ValueError as erro:
        flash(str(erro), "erro")
    return redirect(url_for("produtos.listar"))


@produto_bp.route("/produtos/<int:produto_id>/excluir", methods=["POST"])
@login_required
def excluir(produto_id):
    try:
        if produto_service.excluir_produto(produto_id):
            flash("Produto excluído.", "sucesso")
        else:
            flash("Produto não encontrado.", "erro")
    except ValueError as erro:
        flash(str(erro), "erro")
    return redirect(url_for("produtos.listar"))