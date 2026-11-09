from banco import transacao


def buscar_usuario_por_login(login):
    with transacao() as conexao:
        usuario = conexao.execute(
            "SELECT id, nome, login, senha, perfil FROM usuarios WHERE login = ?",
            (login,),
        ).fetchone()
        return dict(usuario) if usuario else None