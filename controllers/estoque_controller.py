from flask import Blueprint, flash, redirect, render_template, request, url_for

from controllers.auth_controller import login_required
from services import estoque_service, produto_service


estoque_bp = Blueprint("estoque", __name__)


@estoque_bp.route("/estoque", methods=["GET"])
@login_required
def listar():
    return render_template(
        "estoque.html",
        produtos=produto_service.listar_produtos(),
        movimentacoes=estoque_service.listar_movimentacoes(),
    )


@estoque_bp.route("/estoque/<int:produto_id>/movimentar", methods=["POST"])
@login_required
def movimentar(produto_id):
    try:
        saldo = estoque_service.movimentar_estoque(
            produto_id,
            request.form.get("tipo"),
            request.form.get("quantidade"),
        )
        if saldo is None:
            flash("Produto não encontrado.", "erro")
        else:
            flash(f"Estoque atualizado. Saldo atual: {saldo}.", "sucesso")
    except ValueError as erro:
        flash(str(erro), "erro")
    return redirect(url_for("estoque.listar"))