
from flask import Blueprint, redirect, render_template, request, session, redirect, request

from services.auth_service import autenticar_usuario


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET'])
def login():
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])
def realizar_login():
    login = request.form['login']
    senha = request.form['senha']

    usuario = autenticar_usuario(login, senha)

    if usuario is None:
        return render_template('login.html', erro='Login ou senha inválidos')
    
    session['usuario_id'] = usuario['id']
    session['nome'] = usuario['nome']
    session['perfil'] = usuario['perfil']
    return redirect('/produtos')