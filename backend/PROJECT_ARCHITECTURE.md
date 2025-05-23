### 1. Configurações Básicas e Inicialização
1. **`app/config.py`**: Arquivo de configuração global para o projeto.
2. **`app/__init__.py`**: Inicializa a aplicação Flask e configura as extensões.
3. **`.env` e `.flaskenv`**: Arquivos para variáveis de ambiente necessárias para a configuração e execução local.

### 2. Modelos de Dados
4. **`app/models/__init__.py`**: Prepara o pacote de modelos.
5. **`app/models/models.py`**: Define os modelos SQLAlchemy para o seu banco de dados.

### 3. Formulários
6. **`app/forms/__init__.py`**: Prepara o pacote de formulários.
7. **`app/forms/forms.py`**: Define os formulários Flask-WTF usados para entrada de dados do usuário.

### 4. Rotas e Controladores
8. **`app/routes/__init__.py`**: Prepara o pacote de rotas.
9. **`app/routes/auth.py`**: Implementa rotas para autenticação (login, logout, registro).
10. **`app/routes/home.py`**: Rotas para a página inicial e outras rotas relacionadas à navegação principal.
11. **`app/routes/product.py`**: Rotas para criar, visualizar, editar e excluir produtos.

### 6. Recursos Estáticos
20. **`app/static/uploads/`**: Diretório para armazenar arquivos enviados.

### 7. Utilitários e Outros
22. **`app/utils/helpers.py`**: Funções auxiliares e utilitários que podem ser usados em toda a aplicação.

### 8. Execução e Manutenção
23. **`run.py`**: Script para iniciar o servidor Flask.
24. **`requirements.txt`**: Lista de dependências a serem instaladas com pip.
25. **`README.md`**: Documentação básica do projeto.
26. **`LICENSE`**: Arquivo de licença para o projeto.