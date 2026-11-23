# SmartSpace

**Sistema de monitoramento inteligente de ambientes de estudo utilizando IoT, Python, MQTT e Docker.**

## 1. Sobre o projeto

O SmartSpace é um sistema de monitoramento de ambientes de estudo que simula o funcionamento de sensores IoT instalados em salas de uma biblioteca universitária.

O objetivo é coletar informações sobre as condições ambientais e a ocupação dos espaços, permitindo acompanhar suas condições em tempo real.

O sistema utiliza sensores virtuais desenvolvidos em Python, que enviam informações para um broker MQTT. Um servidor recebe e processa esses dados, armazenando as medições em um banco de dados SQLite.

### Informações monitoradas

- **Temperatura:** temperatura ambiente da sala.
- **Ocupação:** se a sala está ocupada ou não.

## 2. Arquitetura do sistema

O projeto é dividido em três containers principais:

| Container | Responsabilidade |
|---|---|
| `sensors` | Simular sensores IoT e publicar medições. |
| `mosquitto` | Receber e distribuir mensagens utilizando o protocolo MQTT. |
| `server` | Receber mensagens, processar informações e armazená-las no SQLite. |

### Comunicação entre os componentes

1. Os sensores virtuais geram medições ambientais.
2. Os sensores publicam os dados no broker Mosquitto por meio do protocolo MQTT.
3. O servidor Python recebe as mensagens publicadas.
4. Os dados são processados e armazenados no banco SQLite.
5. As informações ficam disponíveis para consultas posteriores e integração com um dashboard.

### Tecnologias utilizadas

- Python 3.11
- Docker
- Docker Compose
- Eclipse Mosquitto
- MQTT
- Paho-MQTT
- SQLite

## 3. Estrutura do projeto

```text
pjbl/
│
├── broker/
│   └── mosquitto.conf
│
├── sensors/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── simulator.py
│
├── server/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   └── database.py
│
├── docker-compose.yml
│
└── README.md
```

## 4. Pré-requisitos

Antes de executar o projeto, é necessário ter instalado:

- Docker Engine ou Docker Desktop.
- Docker Compose (plugin `docker compose`).

Para verificar se as ferramentas estão disponíveis, execute:

```bash
docker --version
docker compose version
```

Não é necessário instalar Python, Paho-MQTT, Flask ou SQLite diretamente na máquina para executar a versão conteinerizada do projeto. As dependências Python são instaladas nas respectivas imagens Docker.

## 5. Inicialização dos containers

A execução do sistema é realizada por meio do Docker Compose, responsável por construir, inicializar e conectar os containers.

### Etapa 1 — Acessar o diretório do projeto

Abra o terminal e navegue até a pasta principal:

```bash
cd pjbl
```

Certifique-se de que o arquivo `docker-compose.yml` está presente nesse diretório.

### Etapa 2 — Construir as imagens

Execute:

```bash
docker compose build
```

Esse comando constrói as imagens dos serviços que possuem Dockerfiles, como `sensors` e `server`.

O Mosquitto utiliza uma imagem oficial disponibilizada pelo Docker Hub.

### Etapa 3 — Inicializar os containers

Execute:

```bash
docker compose up -d
```

O parâmetro `-d` executa os containers em segundo plano.

O Docker Compose inicializará:

1. **Mosquitto:** broker responsável pela comunicação MQTT.
2. **Sensors:** simulador de sensores virtuais.
3. **Server:** servidor responsável pelo recebimento e armazenamento das medições.

Os containers são conectados à rede privada `smartspace-net`, permitindo a comunicação entre eles por meio dos nomes dos serviços.

### Etapa 4 — Verificar o funcionamento

Para verificar se os containers estão em execução:

```bash
docker compose ps
```

Para visualizar os logs:

```bash
docker compose logs
```

Para visualizar os logs de um serviço específico:

```bash
docker compose logs sensors
docker compose logs mosquitto
docker compose logs server
```

O servidor deverá apresentar uma mensagem indicando a conexão com o broker MQTT e a inicialização do banco de dados.

O simulador deverá apresentar as medições geradas para cada ambiente.

### Etapa 5 — Acessar o banco de dados

O banco SQLite é armazenado no caminho:

```text
/data/smartspace.db
```

Esse diretório está associado ao volume persistente `smartspace_data`.

Para verificar se o arquivo foi criado:

```bash
docker compose exec server ls -la /data
```

Para consultar os registros utilizando Python dentro do container:

```bash
docker compose exec server python
```

No interpretador Python:

```python
import sqlite3

conn = sqlite3.connect("/data/smartspace.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM measurements")

for row in cursor.fetchall():
    print(row)

conn.close()
```

## 6. Gerenciamento dos containers

### Visualizar os containers ativos

```bash
docker compose ps
```

### Visualizar os logs em tempo real

```bash
docker compose logs -f
```

Para acompanhar apenas o servidor:

```bash
docker compose logs -f server
```

### Reiniciar os serviços

```bash
docker compose restart
```

### Parar os containers

```bash
docker compose stop
```

### Parar e remover os containers

```bash
docker compose down
```

**Importante:** o comando `docker compose down` não remove os volumes nomeados por padrão. Portanto, os dados armazenados no banco SQLite permanecem disponíveis quando os containers são recriados.

Para remover também os volumes e apagar os dados persistidos:

```bash
docker compose down -v
```

**Atenção:** esse último comando apaga permanentemente os dados armazenados nos volumes do projeto.

## 7. Rede e comunicação

Os serviços utilizam uma rede Docker do tipo bridge chamada `smartspace-net`.

Essa rede permite que os containers se comuniquem sem precisar expor todas as portas para a máquina hospedeira.

O broker MQTT utiliza a porta:

```text
1883
```

A comunicação entre sensores e servidor ocorre internamente na rede Docker, utilizando o nome do serviço `mosquitto` como endereço do broker.

O servidor pode ser acessado externamente pela porta `8000`, caso o dashboard/API esteja implementado e configurado para essa porta.

## 8. Persistência dos dados

O SmartSpace utiliza um volume Docker chamado `smartspace_data` para armazenar o banco SQLite.

Essa estratégia permite preservar as medições mesmo quando os containers são removidos e recriados.

O volume é associado ao diretório `/data` dentro do container do servidor.

## 9. Solução de problemas

**Os containers não inicializam:**

Verifique os logs:

```bash
docker compose logs
```

**O servidor não consegue conectar ao broker MQTT:**

Verifique se o container Mosquitto está ativo e se o endereço utilizado pelo servidor é `mosquitto`, e não `localhost`.

**O banco de dados não é criado:**

Verifique se a variável de ambiente `DATABASE_PATH` está configurada como `/data/smartspace.db` e se a função de inicialização do banco está sendo executada.

**Os sensores não enviam dados:**

Verifique se o simulador está conectado ao broker e se os tópicos MQTT utilizados pelos sensores correspondem aos tópicos assinados pelo servidor.

**As dependências Python não são encontradas:**

Verifique os arquivos `requirements.txt` e reconstrua as imagens:

```bash
docker compose up --build -d
```

## 10. Considerações finais

O SmartSpace demonstra a integração de conceitos de Internet das Coisas (IoT), comunicação em redes, protocolos de mensagens, persistência de dados e conteinerização.

A utilização do Docker Compose facilita a reprodução do ambiente, enquanto o MQTT permite a comunicação entre os componentes de forma desacoplada.

A arquitetura também permite futuras expansões, como a implementação de um dashboard, o cálculo de índices de conforto ambiental e a geração de recomendações sobre a utilização dos espaços de estudo.
