from banco import conectar

def buscar_usuario_por_login(login, senha):
    conexao = conectar()
    usuario = conexao.execute("SELECT * FROM usuarios WHERE login = ?", (login,)).fetchone()
    if usuario is None:
        return None
    if usuario["senha"] != senha:  # Assuming senha is the 4th column (index 3)
        return None
    return usuario