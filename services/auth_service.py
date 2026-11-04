from repositories.usuario_repository import buscar_usuario_por_login

def autenticar_usuario(login, senha):
    usuario = buscar_usuario_por_login(login)
    if usuario is None:
        return None
    if usuario["senha"] != senha:
        return None
    return usuario