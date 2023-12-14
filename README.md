# Pacote de observabilidade

conjunto com as principais ferramentas do mercado para observabilidade, onde qualquer aplicação pode se conectar a ele e enviar seus dados de métrica, logs e traces. Tendo de forma simplificada e pré-configurada acesso a visualizações e alertas. O projeto segue a seguinte arquitetura:

![Texto Alternativo](./observability/imgs/arquitetura-observability.PNG)

Vale ressaltar que a aplicação feita aqui tem caráter somente de teste do pacote de observabilidade, é possível aplicar os conceitos demonstrados e utilizar o pacote de observabilidade em qualquer outra aplicação, trazendo muito valor ao projeto escolhido.

## Tabela de conteúdos
* [Tecnologias utilizadas](#tecnologias-utilizadas)
* [Requisitos para uso](#requisitos-para-uso)
* [Instalação](#instalação)
* [Observability Mtl Instument](#observability-mtl-instrument)
* [Como iniciar](#como-iniciar)
    * [Pacote de observabilidade](#pacote-de-observabilidade)
    * [Aplicação FastAPI](#aplicacao-fastapi)
* [Como usar](#como-usar)
    * [Pacote de observabilidade](#pacote-de-observabilidade)
    * [Aplicação FastAPI](#aplicacao-fastapi)
    * [Logs](#configurações)
* [Configurações Grafana](#configuracoes-grafana)
    * [Datasources](#configurações)
    * [Logs e Traces](#logs-e-traces)

## Tecnologias utilizadas
* Grafana 10.2.0
* Prometheus v2.47.2
* Pushgateway v1.6.2
* Tempo 2.2.0
* Loki 2.9.2
* Nginx 1.25.3-bookworm
* Docker 24.0.5
* Python 3.10

## Requisitos para uso
* IDE - VScode, PyCharm, etc.
* Conta no Docker.hub
* Versão Atualizada do WSL 2 

Caso esteja rodando no sistema operacional windows, é necessário instalar o WSL, seguindo o tutorial do link... [WSL](https://boom-particle-8c8.notion.site/como-instalar-o-wsl2-readme-md-02dcaa42ac7d490bb8f5bb6620669590)

## Observability Mtl Instument
Esse repositório possui a configuração de observabilidade para diversas ferramentas, porém, vale ressaltar que a aplicação de exemplo utiliza a biblioteca [observability-mtl-instrument](https://github.com/SergioRicJr/observability-mtl-instrument). Neste link é possível acessar o repositório que fala mais sobre o uso, url para documentação e tutorial de uso.

## Instalação
Execute os comandos no terminal da IDE ou no terminal de comando do sistema operacional utilizado:
* 1 - Crie uma pasta:
```
 mkdir observability-package
```
* 2 - Entre na pasta do projeto:
```
 cd observability-package
```
* 3 - Clone o repositório:
```
 git clone https://github.com/SergioRicJr/observability-package
```
* 4 - Abra o projeto:
caso esteja usando Visual Studio Code:
```
    code .
```
se não, é possível abrir diretamente pela IDE, buscando a pasta do projeto para abrir nela.

## Como iniciar

### Pacote de observabilidade
* Tendo o seu projeto já aberto, é necessário primeiramente entrar na pasta do pacote de observabilidade, com o comando:
```
    cd observability
```

* Antes de rodar o próximo comando, é necessário garantir que o Docker esteja rodando na máquina, após isso, basta utilizar o seguinte comando:
```
    docker-compose up
```
### Aplicação FastAPI
* Tendo o seu projeto já aberto, é necessário primeiramente entrar na pasta da aplicação fastAPI, com o comando:
```
    cd fastapi-app
```

* Antes de rodar o próximo comando, é necessário garantir que o Docker esteja rodando na máquina, após isso, basta utilizar o seguinte comando:
```
    docker-compose up
```

## Como usar
### Pacote de observabilidade
* 1 - Rodando em ambiente local, basta acessar o navegador

* 1 - No primeiro acesso é necessário realizar o login utilizando para username "admin", e para password "admin", e então redefinir a senha para os próximos acessos.
![Texto Alternativo](./observability/imgs/login-grafana.png)

* É possível acessar os dashboards através da navegação lateral, criar, editar e visualizar os que já foram construídos com as diferentes fontes de dados, como Prometheus, Tempo e Loki.
![Texto Alternativo](./observability/imgs/button-dashboards-grafana.png)

* É possível também ter acesso aos dados entrando em DataSources, selecionando "explore" em alguma das fontes e utilizando a linguagem de consulta de cada uma delas.
![Texto Alternativo](./observability/imgs/datasources-grafana.png)

### Aplicação FastAPI
Para gerar as métricas, traces e logs, é possível acessar através de qualquer navegador acessar os endpoints da aplicação, que são:

* Retorna uma mensagem de olá, e desejando boas vindas à aplicação.

    ```http
        http://127.0.0.1:8000/
    ```

* Retorna um numero aleatório de 0 a 100.
    ```http
        http://127.0.0.1:8000/random
    ```

* Faz uma requisição ao endpoint "/random", calcula a fatorial do número e retorna ele.
    ```http
        http://127.0.0.1:8000/factorial
    ```

* Faz requisições aos endpoints "/", "/random" e "/factorial", e retorna uma mensagem.
    ```http
        http://127.0.0.1:8000/requests
    ```

### Logs
A configuração dos logs é parte essencial do projeto, por isso a formatação escolhida para ele é necessária, e deve ser feita incluindo o trace_id e o span_id, afim de que o grafana posso conectar e criar o link para o trace que aquele log referencia, sendo feito da seguinte forma:

```
    log_format = '%(asctime)s levelname=%(levelname)s name=%(name)s file=%(filename)s:%(lineno)d trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s trace_sampled=%(otelTraceSampled)s - message="%(message)s"'
```

![Texto alternativo](./observability/imgs/logs-line-img.png)

Já em relação ao envio dos logs ao Grafana Loki, é necessário somente uma requisição HTTP, seguindo o padrão definido pela documentação do [Loki](https://grafana.com/docs/loki/latest/reference/api/), da seguinte forma:

```
{
    "streams": [
        {
        "stream": {
            "label": "value"
        },
        "values": [
            [ "<unix epoch in nanoseconds>", "<log line>" ],
            [ "<unix epoch in nanoseconds>", "<log line>" ]
        ]
        }
    ]
}
```

## Configurações Grafana
O grafana possui muitos arquivos que possibilitam sua customização, e algumas dessas configurações foram essenciais para o desenvolvimento do pacote, o conhecimento delas é importante para possíveis manutenções, resoluções de erro e adição de recursos personalizados. Essas configurações são passadas como volumes para o Grafana, da seguinte forma:

```
    grafana:
        image: grafana/grafana:10.2.0
        restart: always
        container_name: grafana
        ports:
            - 3000:3000
        volumes:
    -->     - ./etc/grafana/:/etc/grafana/provisioning/datasources
```

Nesse exemplo os arquivos no meu diretório dentro da pasta grafana, que está na pasta etc, é passada como configuração, redefinindo os conteúdos da pasta provisioning. 

### DataSources
Os DataSources são as fontes de dados que o Grafana acessa para gereção de dashboards e alertas. Assim como os demais recursos do Grafana, é possível adicionar através da interface gráfica, porém, para que isso não seja necessário caso ocorra a criação de novos containers dele, é possível configurar através de um arquivo ".yaml", da seguinte forma:

```
    apiVersion: 1

    datasources:
    - name: Prometheus
    type: prometheus
    access: proxy
    orgId: 1
    url: http://prometheus:9090
    basicAuth: false
    isDefault: true
    version: 1
    editable: true
```

Aqui um datasource do Prometheus está sendo configurado para que haja acesso a esses dados nativamente.
![Texto Alternativo](./observability/imgs/datasource-example.png)


## Logs e Traces
Para que os traces e logs estejam relacionados, é necessário que a mensagem do log contenha o trace id, e essa relação é realizada no Grafana através do datasources.yaml, onde uma expressão regular retira da mensagem de log a informação do trace e cria o link no dashboard, da seguinte forma:

```
- name: Loki
  type: loki
  access: proxy
  orgId: 1
  url: http://loki:3100
  basicAuth: false
  isDefault: false
  version: 1
  editable: true
  apiVersion: 1
  jsonData:
    derivedFields:
--->    - datasourceUid: tempo
--->    matcherRegex: "trace_id=(\\w+)"
--->    name: trace_id
--->    url: $${__value.raw}
```

![Texto Alternativo](./observability/imgs/print-logs-trace-grafana.PNG)
