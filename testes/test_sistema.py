import importlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import banco

_diretorio_importacao = tempfile.TemporaryDirectory()
_patch_importacao = patch.object(
    banco, "DB_PATH", Path(_diretorio_importacao.name) / "inicializacao.db"
)
_patch_importacao.start()
app = importlib.import_module("app").app
_patch_importacao.stop()
_diretorio_importacao.cleanup()


class SistemaEstoqueTestCase(unittest.TestCase):
    def setUp(self):
        self.diretorio = tempfile.TemporaryDirectory()
        self.db_patch = patch.object(
            banco, "DB_PATH", Path(self.diretorio.name) / "teste.db"
        )
        self.db_patch.start()
        banco.criar_banco()
        app.config.update(TESTING=True, SECRET_KEY="chave-de-teste")
        self.client = app.test_client()

    def tearDown(self):
        self.db_patch.stop()
        self.diretorio.cleanup()

    def login(self):
        return self.client.post(
            "/login", data={"login": "admin", "senha": "123"}
        )

    def criar_produto(self, **overrides):
        dados = {
            "nome": "Caderno",
            "valor": "12.50",
            "quantidade": "5",
            "estoque_minimo": "2",
            "estoque_maximo": "10",
        }
        dados.update(overrides)
        return self.client.post("/produtos", data=dados, follow_redirects=True)

    def test_login_protege_telas_e_permite_sair(self):
        resposta = self.client.get("/produtos")
        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(resposta.location, "/")

        resposta = self.login()
        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(resposta.location, "/produtos")
        self.assertIn(b"Produtos", self.client.get("/produtos").data)

        self.client.post("/sair")
        self.assertEqual(self.client.get("/produtos").status_code, 302)

    def test_cadastro_edicao_e_exclusao_de_produto(self):
        self.login()
        resposta = self.criar_produto()
        self.assertIn("Produto cadastrado com sucesso.".encode(), resposta.data)

        from repositories.produto_repository import listar_produtos

        item = listar_produtos()[0]
        self.assertEqual(
            self.client.get(f"/produtos/{item['id']}/editar").status_code, 200
        )
        resposta = self.client.post(
            f"/produtos/{item['id']}/atualizar",
            data={
                "nome": "Caderno grande",
                "valor": "15",
                "estoque_minimo": "3",
                "estoque_maximo": "12",
            },
            follow_redirects=True,
        )
        self.assertIn("Produto atualizado com sucesso.".encode(), resposta.data)
        self.assertEqual(listar_produtos()[0]["quantidade"], 5)

        resposta = self.client.post(
            f"/produtos/{item['id']}/excluir", follow_redirects=True
        )
        self.assertIn("Produto excluído.".encode(), resposta.data)
        self.assertEqual(listar_produtos(), [])

    def test_validacoes_e_movimentacoes_sao_atomicas(self):
        self.login()
        resposta = self.criar_produto(estoque_maximo="4")
        self.assertIn("quantidade em estoque não pode superar".encode(), resposta.data)

        self.criar_produto(quantidade="3", estoque_maximo="10")
        from repositories.produto_repository import listar_produtos

        produto = listar_produtos()[0]
        resposta = self.client.post(
            f"/estoque/{produto['id']}/movimentar",
            data={"tipo": "Entrada", "quantidade": "8"},
            follow_redirects=True,
        )
        self.assertIn("ultrapassa o estoque máximo".encode(), resposta.data)
        self.assertEqual(listar_produtos()[0]["quantidade"], 3)

        resposta = self.client.post(
            f"/estoque/{produto['id']}/movimentar",
            data={"tipo": "Saída", "quantidade": "4"},
            follow_redirects=True,
        )
        self.assertIn("Não há estoque suficiente".encode(), resposta.data)
        self.assertEqual(listar_produtos()[0]["quantidade"], 3)

        self.client.post(
            f"/estoque/{produto['id']}/movimentar",
            data={"tipo": "Entrada", "quantidade": "2"},
            follow_redirects=True,
        )
        atual = listar_produtos()[0]
        self.assertEqual(atual["quantidade"], 5)
        self.assertIn(b"Hist\xc3\xb3rico recente", self.client.get("/estoque").data)

    def test_produto_com_historico_nao_pode_ser_excluido(self):
        self.login()
        self.criar_produto(quantidade="0")
        from repositories.produto_repository import listar_produtos

        produto = listar_produtos()[0]
        self.client.post(
            f"/estoque/{produto['id']}/movimentar",
            data={"tipo": "Entrada", "quantidade": "1"},
        )
        resposta = self.client.post(
            f"/produtos/{produto['id']}/excluir", follow_redirects=True
        )
        self.assertIn("possui movimentações".encode(), resposta.data)
        self.assertEqual(len(listar_produtos()), 1)

    def test_login_invalido_e_produto_duplicado(self):
        resposta = self.client.post(
            "/login", data={"login": "admin", "senha": "errada"}
        )
        self.assertEqual(resposta.status_code, 401)
        self.login()
        self.criar_produto()
        resposta = self.criar_produto()
        self.assertIn("Já existe um produto".encode(), resposta.data)


if __name__ == "__main__":
    unittest.main()