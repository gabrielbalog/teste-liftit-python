# Teste Liftit

O teste tem como objetivo a criação de um sistema para gerenciamento de veículos
e proprietários.

Deve contar com um portal para gerenciamento dos dados. Neste portal
o usuário somente deverá ver apenas seus veículos. Deverá haver autenticação
no portal.

O código deve ser feito em Python, e deve contar com testes.

## Tecnologia

- Python 3.8+
- Django 3+
- PostgreSQL 12
- Docker

## Utilização

Para utilização do projeto basta clona-lo em sua máquina utilizando o git.
Deve-se possuir também o binário do docker-compose em sua máquina.

Alguns passos devem ser feitos antes de iniciar:
- Criação do arquivo de ambiente do Django e do Postgres

### Criando os arquivos de ambiente

Copie o arquivo .env.sample para .env

Faça o mesmo para o arquivo .env.db.sample, deixando como .env.db

Estes arquivos tem as configurações inicias dos serviços. O que você irá
encontrar dentro deles são:
- Configuração do Debug do Django
- Configuração da Secret Key do Django
- Configuração do acesso ao banco de dados
- Configuração dos hosts que podem acessar o Django

No arquivo do Postgres, você irá encontrar:
- Nome, usuário e senha do banco de dados

*Importante notar que os dados no arquivo do Django deve estar em conformidade
com dados do arquivo do banco de dados para que possa funcionar corretamente.*

Por padrão o debug vem desativado.

### Iniciando os serviços

Para subir rode o seguinte comando:

```bash
$ docker-compose up --build -d
```

Neste momento ele fará o build da imagem do Django, estando terminada ele
iniciara o processo do Postgres e do Django.

Agora basta acessar o endereço http://localhost:8000 para visualizar a tela de boas
vindas do Django, somente caso o DEBUG esteja ativado, do contrário por não haver
rota ele retornara um erro. Para acessar o portal basta utilizar o endereço
http://localhost:8000/admin.

Neste ponto você não possui um usuário criado, para criar execute os seguintes
comandos:

```bash
$ docker-compose -f docker-compose.yaml exec web \
    python manage.py createsuperuser

Username (leave blank to use 'app'): 
Email address: 
Password: 
Password (again): 
```

Digite um nome para o usuário, um email, uma senha e pronto o usuário estará
criado. Volte ao login do portal e tente usar as credenciais.

### Static e Media

É importante notar que o não uso de Debug impacta na exibição das medias
e arquivos estáticos. Para resolver isso é necessário um proxy reverso,
que irá redirecionar todas as chamadas para o endpoint direto para a pasta 
dos carquivos.

## Usuários

O usuário que foi criado possui o status de superusuário. Isso signifca que
ele pode acessar todos os dados mesmo que não esteja em um grupo adequado.

Para utilização como um usuário normal, entre em "Users", e "Add User".
Preencha um nome para o usuário e uma senha. Criado o usuário é necessário atribuir
o grupo "FleetUser" a ele, para isso clique duas vezes no nome do grupo.

Tique também que o usuário seja do "Staff", sem isso ele não poderá logar
no portal.

No rodapé salve o usuário.

Acesse em uma janela anonima, ou faça logout, e logue com o novo usuário. Veja que
"Groups" e "Users" não aparecem mais, somente "Fleet" é exibido.

### Limitação de acesso aos veículos

Foi criado uma limitação para o acesso somente dos veículos que o usuário
criou. Para testar isso, logue como superuserário ou com outro usuário e
crie um veículo, acesse agora com um usuário normal. O veículo que foi criado
não aparece.

Agora crie um veículo com este usuário normal, e acesse pelo superusuário, veja que
o veículo criado aparece. Isso se deve pelo superusuário não entrar nesta
regra. Com o perfil atrelado a ele você pode ver todos os dados e fazer o que
quiser.

## API

O projeto conta com uma API para gerenciar os dados de veículos. Para acessa-la
é necessário ter um token. O mesmo pode ser obtido no portal do Django, criando
um em "Tokens", ou pela pela API, utilize o endpoint 
``/api-token-auth/``, passando um JSON com username e password no body. 

Com o Token em mãos na chamada coloque-o no Header desta forma "Authorization: Token 3727d7272f7727642624".

A documentação está disponível no link http://localhost:8000/redoc ou 
http://localhost:8000/swagger.

A API prove os seguintes endpoints:
- /fleet/vehicle (GET, POST)
- /fleet/vehicle/:id (GET, PUT, DELETE)

A API possui cobertura de testes.

## Desenvolvimento

Para desenvolver e utilizar as melhores funções disponíveis os passos
são os seguintes:
- Coloque 1 em Debug no arquivo de ambiente
- No docker-compose.yaml descomente o trecho ``- ./:/home/app/web``

Estes dois passos posibilitará que todas as alterações no host sejam feitas
dentro do docker, e que a funcionalidade de reload do Django funcione
corretamente.

### Ambiente Virtual

Ainda sim é possível não usar o docker para rodar o projeto. Para isso
crie um virtual envinroment com o python:

```
$ python -m venv venv
```

Importante que você deve possuir a versão 3.8 instalada em seu sistema.
Caso não possua, recomendo o uso da ferramente pyenv para sua instalação.

Com o ambiente criado, basta entra nele e instalar o requirements:

```
$ source venv/bin/activate
$ (venv) pip install -r requirements.txt
```

Outra coisa é necessário notar são os dados de ambiente necessários para
rodar o Django. Exporte-os manualmente para seu ambiente com os dados
adequados.




## Testes

Para rodar os testes rode o seguinte comando:

```
$ docker-compose -f docker-compose.yaml exec web \
    python manage.py test apps/fleet

Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..
----------------------------------------------------------------------
Ran 2 tests in 0.263s

OK
Destroying test database for alias 'default'...
```

O resultado dos testes será disponibilizado abaixo do comando.

