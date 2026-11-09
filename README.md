# Sistema de estoque

Aplicação web simples em Flask e SQLite para cadastrar produtos e acompanhar o estoque.

## Executar

```powershell
python -m pip install -r requirements.txt
python app.py
```

Abra `http://127.0.0.1:5000`. O banco `estoque.db` é criado automaticamente na pasta do projeto.

## Acesso inicial

- Administrador: `admin` / `123`
- Operador: `operador` / `123`

Altere as senhas padrão antes de usar o sistema em um ambiente compartilhado. Defina também a variável de ambiente `SECRET_KEY` para proteger as sessões.

## Recursos

- Cadastro, edição e exclusão de produtos.
- Registro de entradas e saídas com validação de saldo e estoque máximo.
- Alertas de estoque baixo e histórico das últimas 100 movimentações.
- Acesso às telas de produtos e estoque somente após login.

## Testes

```powershell
python -m unittest discover -s testes -v
```
