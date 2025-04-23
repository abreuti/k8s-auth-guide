# Simple Python Flask App com Kubernetes Utilizando Liveness e Readiness

> **Este projeto é um estudo pessoal**. A finalidade é aprender e aplicar conhecimentos sobre Liveness e Readiness em Kubernetes. O código não é voltado para produção, mas sim para fins educacionais e experimentação.

Este projeto demonstra como rodar uma aplicação simples em Python com Flask dentro de um container Docker e gerenciar sua execução no Kubernetes. A aplicação serve uma página web com a mensagem "Olá, Kubernetes!".

## Pré-requisitos

- [Docker](https://www.docker.com/get-started)
- [Kubernetes](https://kubernetes.io/docs/setup/)
- Conta na [Magalu Cloud](https://www.magalucloud.com.br/) para utilizar o CR (Container Registry)

...

## Estrutura do Projeto

O repositório contém os seguintes arquivos principais:

- **`app.py`**: Código da aplicação em Python usando Flask.
- **`Dockerfile`**: Arquivo para construir a imagem Docker da aplicação.
- **`simple-python-app.yaml`**: Configuração do Pod do Kubernetes para rodar a aplicação.
- **`liveness_readiness.md`**: Este arquivo.

  
