# Sistema Supervisório Industrial

Projeto Integrador desenvolvido em Python e Streamlit para supervisão e controle de um processo industrial simulado.

## Tecnologias

- Python
- Streamlit
- Pandas
- MySQL
- SQLAlchemy
- OPC UA
- Open Industry Project
- AWS CloudWatch
- Boto3
- Git e GitHub

## Funcionalidades

### Login
- Autenticação de usuários pelo MySQL.
- Senhas armazenadas com hash bcrypt.
- Registro de tentativas de login.
- Registro de acessos bem-sucedidos e malsucedidos.

### Processo industrial
- Comunicação OPC UA com o CLP simulado.
- Monitoramento da esteira transportadora.
- Leitura do motor e sensor de presença.
- Leitura e ajuste da velocidade.
- Comandos para ligar e desligar a esteira.
- Atualização automática das variáveis.

### Banco de dados
- Consulta de eventos no MySQL.
- Filtros por período, equipamento, usuário e evento.
- Histórico de leituras dos sensores.

### Gráficos
- Histórico de velocidade.
- Estado do motor.
- Detecções do sensor.
- Eventos por dia.
- Tempo de funcionamento observado.
- Acionamentos da esteira.

### Monitoramento de segurança
- Consulta dos logs no AWS CloudWatch.
- Identificação de tentativas inválidas.
- Identificação de usuários e horários.
- Classificação por nível de evento.
- Detecção de possíveis tentativas de força bruta.

### Cadastro de usuários
- Cadastro e edição de usuários.
- Definição de perfis.
- Ativação e desativação de contas.
- Controle de acesso por perfil.

## Perfis

| Perfil | Acesso |
|---|---|
| Administrador | Todas as telas |
| Operador | Processo e gráficos |
| Engenheiro | Todas, exceto cadastro de usuários |

## Estrutura do projeto

- app.py — aplicação principal.
- telas.py — interfaces do sistema.
- autenticacao.py — validação de login.
- conexao_banco.py — conexão com MySQL.
- classe_gerenciador.py — gerenciamento de eventos e logs.
- Classe_OPC.py — comunicação OPC UA.
- criar_usuarios.py — criação de usuários.
- main.py — consulta de teste ao banco.
- .gitignore — arquivos excluídos do versionamento.

## Banco de dados

Banco utilizado: `teste_professor`

Tabelas principais:

- `usuarios`: usuários, hashes de senha, perfis e status.
- `eventos`: eventos operacionais e de segurança.
- `leituras_sensores`: leituras recebidas do processo industrial.

## Variáveis OPC UA

| Variável | Descrição |
|---|---|
| Main.Start | Comando de partida |
| Main.Sensor | Sensor de presença |
| Main.Motor | Estado do motor |
| Main.Velocidade | Velocidade da esteira |

Endereço OPC UA padrão: `opc.tcp://10.211.55.3:4843`

O endereço pode ser configurado pela variável `OPC_UA_URL`.

## AWS CloudWatch

- Grupo: `/projeto-integrador/supervisorio`
- Região: `us-east-1`

O envio e a consulta dos logs são realizados utilizando Boto3.

As credenciais AWS são configuradas no ambiente local, sem serem inseridas diretamente no código.

## Configuração do ambiente

Criar o ambiente virtual:

`python3 -m venv .venv`

Ativar:

`source .venv/bin/activate`

Instalar as dependências:

`pip install streamlit pandas mysql-connector-python sqlalchemy pymysql bcrypt boto3 opcua`

Configurar o arquivo `.env` na raiz do projeto com as variáveis DB_HOST, DB_USER, DB_PASSWORD, DB_PORT e DB_NAME.

O arquivo `.env` não deve ser publicado no GitHub.

## Executar o sistema

`streamlit run app.py --server.port 8502`

Acesso local: `http://localhost:8502`

O simulador industrial e o servidor OPC UA precisam estar em execução para o monitoramento do processo.

## Observação sobre o processo

O simulador atualmente integrado disponibiliza sinais de partida, motor, sensor de presença e velocidade.

Indicadores de temperatura, nível, válvulas e ciclos completos dependem da futura disponibilização desses sinais no CLP.

## Versionamento

O projeto utiliza Git e GitHub para registrar a evolução do desenvolvimento.

Repositório:

https://github.com/Locatelli-1/projeto-integrador-supervisorio-industrial

## Objetivo acadêmico

Integrar conhecimentos de automação industrial, controle de processos, programação, comunicação industrial, banco de dados, segurança da informação e visualização de dados.
