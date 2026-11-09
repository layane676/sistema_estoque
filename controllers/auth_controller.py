
from functools import wraps

from flask import Blueprint, redirect, render_template, request, session, url_for


from services.auth_service import autenticar_usuario


auth_bp = Blueprint('auth', __name__)


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapped_view


@auth_bp.route('/', methods=['GET'])
def login():
    if "usuario_id" in session:
        return redirect(url_for("produtos.listar"))
    return render_template("login.html")

@auth_bp.route('/login', methods=['POST'])
def realizar_login():
    login = request.form.get("login", "")
    senha = request.form.get("senha", "")

    usuario = autenticar_usuario(login, senha)

    if usuario is None:
        return render_template("login.html", erro="Login ou senha inválidos"), 401

    session.clear()
    session["usuario_id"] = usuario["id"]
    session["nome"] = usuario["nome"]
    session["perfil"] = usuario["perfil"]
    return redirect(url_for("produtos.listar"))


@auth_bp.route("/sair", methods=["POST"])
def sair():
    session.clear()
    return redirect(url_for("auth.login"))