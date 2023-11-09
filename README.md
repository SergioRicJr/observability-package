# Pacote de observabilidade

conjunto com as principais ferramentas do mercado para observabilidade, tratado de forma agnóstica, onde qualquer aplicação pode se conectar a ele e enviar seus dados de métrica, logs e traces. Tendo de forma simplificada e pré-configurada acesso a visualizações e alertas. O projeto segue a seguinte arquitetura:

![Texto Alternativo](./observability/imgs/arquitetura-observability.PNG)

## Tabela de conteúdos
* [Tecnologias utilizadas](#tecnologias-utilizadas)
* [Requisitos para uso](#requisitos-para-uso)
* [Instalação](#instalação)
* [Como iniciar](#como-iniciar)
    * [Pacote de observabilidade](#pacote-de-observabilidade)
    * [Aplicação FastAPI](#aplicacao-fastapi)
* [Como usar](#como-usar)
    * [Pacote de observabilidade](#pacote-de-observabilidade)
    * [Aplicação FastAPI](#aplicacao-fastapi)
* [Configurações](#configurações)
    * [Aplicações](#aplicacoes)
    * [Métricas](#configurações)
    * [Traces](#configurações)
    * [Logs](#configurações)
    * [Grafana](#configurações)

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
 git clone https://github.com/Senai-Sorocaba-IC-2023-2/Sergio
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
* 1 - No primeiro acesso é necessário realizar o login utilizando para username "admin", e para password "admin", e então redefinir a senha para os próximos acessos.
![Texto Alternativo](./observability/imgs/login-grafana.png)

* É possível acessar os dashboards através da navegação lateral, criar, editar e visualizar os que já foram construídos com as diferentes fontes de dados, como Prometheus, Tempo e Loki.
![Texto Alternativo](./observability/imgs/button-dashboards-grafana.png)

* É possível também ter acesso aos dados entrando em DataSources, selecionando "explore" em alguma das fontes e utilizando a linguagem de consulta de cada uma delas.
![Texto Alternativo](./observability/imgs/datasources-grafana.png)

### Aplicação FastAPI
Para gerar as métricas, traces e logs e acessar através do Grafana, é possível acessar 