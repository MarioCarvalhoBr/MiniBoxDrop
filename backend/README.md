# API Backend do Mini BoxDrop

## Visão Geral
Mini BoxDrop é um sistema abrangente de gerenciamento de arquivos projetado para lidar com as complexidades de gerenciar clientes, produtos com anexos. Construído com Python usando o framework Flask, ele integra tecnologias como SQLAlchemy para ORM, SQLite para o banco de dados e Bootstrap para design responsivo.

## Funcionalidades
- **Gerenciamento de Clientes**: Registrar, atualizar e excluir clientes.
- **Gerenciamento de Produtos**: Adicionar, editar e remover produtos.
- **Autenticação de Usuários**: Sistema seguro de login e registro para usuários.
- **Design Responsivo**: Utiliza Bootstrap para garantir uma experiência perfeita em diversos dispositivos.

## Tecnologias
- Python 3
- Flask
- SQLAlchemy
- SQLite

## Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip
- virtualenv (recomendado)

### Configuração
1. Clone o repositório:
   ```bash
   git clone https://your-repository-url.com/Mini-BoxDrop.git
   cd Mini-BoxDrop
   ```

2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows use `venv\Scripts\activate`
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Inicialize o banco de dados:
   ```bash
   python init_db.py
   ```

5. Execute a aplicação:
   ```bash
   flask run
   ```

## Uso
Navegue até `http://127.0.0.1:5000/` no seu navegador para começar a usar o Mini BoxDrop.

## Licença
Distribuído sob a Licença MIT. Veja o arquivo `LICENSE` para mais informações.

## Contato
- Mário de Araújo Carvalho - mariodearaujocarvalho@gmail.com

### Descrição das Seções

- **Visão Geral**: Uma breve descrição do projeto e suas funcionalidades.
- **Funcionalidades**: Uma lista das principais funcionalidades do projeto.
- **Tecnologias**: Tecnologias e ferramentas usadas no desenvolvimento do projeto.
- **Instalação**: Instruções passo a passo sobre como configurar o projeto localmente.
- **Uso**: Como usar o projeto após a instalação.
- **Contribuição**: Diretrizes para contribuir com o projeto.
- **Licença**: Informações sobre a licença sob a qual o projeto é distribuído.
- **Contato**: Informações de contato do autor ou mantenedor do projeto.

## Contribuição
Contribuições são o que tornam a comunidade de código aberto um lugar incrível para aprender, inspirar e criar. Qualquer contribuição que você fizer será **muito apreciada**.

1. Faça um Fork do Projeto
2. Crie sua Branch de Funcionalidade (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request
