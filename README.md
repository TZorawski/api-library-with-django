# Library API With Django

Nesse projeto foi desenvolvida uma API para gerenciamento de uma biblioteca digital moderna. O sistema permite o cadastro de livros e usuários, além de controlar todo o fluxo de empréstimos da biblioteca.

## Tecnologias utilizadas:
- Python (3.14)
- Django (5.2)
- Django Rest Framework (3.16)
- SQLite
- Pydantic

A escolha do framework foi feita pensando em uma arquitetura em camadas e na possibilidade de implementação de features futuras (testes automatizados, documentação automática com Swagger, paginação, frontend). O tempo de desenvolvimento também foi levado em conta.
O FastAPI também foi levado em consideração, mas foi descartado por não incluir ferramentas para o desenvolvimento do frontend. A forte comunidade e as diversas facilidades trazidas por suas bibliotecas foram os principais pontos para a sua escolha.
Para o banco de dados foi escolhido o SQLite, uma vez que é leve, não precisa de um SGBD e já vem por padrão na instalação do django.

## Arquitetura e decisões técnicas:
Foi escolhida uma arquitetura em camadas mais simplificada devido ao tempo de desenvolvimento.
Camada de Interface ->Camada Aplicação -> Camada de Domínio
### Camada de Domínio:
Contém a abstração da entidades da aplicação. Nela está o arquivo models.py.
### Camada de Aplicação:
Nessa camada foram absorvidas as camadas de serviços do domínio e de aplicação. É nela onde estão a lógica de negócio e a interface de operações como adicionar, salvar e editar. Ela está dividida nos arquivos services.py e validators.
### Camada de Interface
É nessa camada onde está a interface de comunicação da API. Ela trata as chamadas e respostas. Está dividida entre os arquivos views.py e serializers.py.

##Instruções de instalação e execução
1. Clonar o repositório
>git clone https://github.com/TZorawski/api-library-with-django.git
>cd btg_test_tz

2. Criar ambiente virtual
>python -m venv venv
>source venv/bin/activate  # Linux/Mac
>venv\Scripts\activate     # Windows

3. Instalar dependências
>pip install -r requirements.txt

4. Executar migrações
>python manage.py migrate

5. Rodar o servidor
>python manage.py runserver

## Funcionalidades implementadas:
####Livros:
- Listar todos os livros
- Ver detalhes de um livro
- Ver disponibilidade de um livro
- Cadastrar um livro
- Editar um livro

####Usuários:
- Listar todos os usuários
- Ver detalhes de um usuário
- Listar o histórico de empréstimo de um usuário
- Cadastrar um usuário
- Editar um usuário

####Empréstimos:
- Listar todos os empréstimos
- Listar todos os empréstimos ativos/atrasados
- Listar todos os empréstimo de um usuário
- Fazer empréstimo de um livro
- Fazer a devolução de um empréstimo

##Exemplos de uso da API:
Para acessar os serviços de livros, usuários e empréstimos da API utilize as rotas:
>{{url_servidor}}/library/books/
>{{url_servidor}}/library/users/
>{{url_servidor}}/library/loans/

####Exemplos:
Para listar todos os livros:
- Utilize o método GET
>{{url_servidor}}/library/books/

Para ver detalhes de um livro:
- Utilize o método GET
- Passe o id do livro desejado na URL
- No exemplo abaixo será retornado o livro de id = 2
>{{url_servidor}}/library/books/book/2

Para fazer empréstimo de um livro:
- Utilize o método POST
- Envie um form-data no body da requisição com os parâmetros: user_id e book_id
>{{url_servidor}}/library/loans/


