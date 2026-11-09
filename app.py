import os

from flask import Flask
from controllers.auth_controller import auth_bp
from controllers.estoque_controller import estoque_bp
from controllers.produto_controller import produto_bp
from banco import criar_banco


def criar_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "chave-local-de-desenvolvimento"
    )
    app.register_blueprint(auth_bp)
    app.register_blueprint(produto_bp)
    app.register_blueprint(estoque_bp)
    criar_banco()
    return app


app = criar_app()


if __name__ == "__main__":
    app.run(debug=True)