# Simple Python Flask App com Kubernetes Utilizando Liveness e Readiness

> **Este projeto é um estudo pessoal**. A finalidade é aprender e aplicar conhecimentos sobre Liveness e Readiness em Kubernetes. O código não é voltado para produção, mas sim para fins educacionais e experimentação.

Este projeto demonstra como rodar uma aplicação simples em Python com Flask dentro de um container Docker e gerenciar sua execução no Kubernetes. A aplicação serve uma página web com a mensagem "Olá, Kubernetes!".

## Pré-requisitos

- [Docker](https://www.docker.com/get-started)
- [Kubernetes](https://kubernetes.io/docs/setup/)
- Conta na [Magalu Cloud](https://www.magalucloud.com.br/) para utilizar o CR (Container Registry)

...

## Estrutura do Projeto

O repositório https://github.com/abreuti/k8s-auth-guide/tree/main/liveness_readiness_files 
contém os seguintes arquivos principais:

- **`app.py`**: Código da aplicação em Python usando Flask.
- **`Dockerfile`**: Arquivo para construir a imagem Docker da aplicação.
- **`simple-python-app.yaml`**: Configuração do Pod do Kubernetes para rodar a aplicação.

## Construir a imagem Docker da aplicação:

Para criar a imagem Docker da aplicação, utilizei o seguinte comando:
```bash
docker build -t simple-python-app .
```

Como estou utilizando CR da Magalu Cloud, a região escolhida foi o DC da região Sudeste.
```bash
docker login https://container-registry.br-se1.magalu.cloud
```
> ** O comando docker login autentica o seu Docker com o Container Registry usando as credenciais obtidas pelo provedor de CR **

Agora será necessário Taguear a Imagem Docker:
```bash
docker tag simple-python-app:latest container-registry.br-se1.magalu.cloud/diego-cr/simple-python-app:latest
```
O comando docker tag associa uma imagem local com um nome e endereço de registry no Magalu Cloud. A imagem simple-python-app:latest será marcada para o registry diego-cr na região br-se1.

Agora será necessário realizar o Push da Imagem Docker:
```bash
docker push container-registry.br-se1.magalu.cloud/diego-cr/simple-python-app:latest
```
O comando docker push envia a imagem marcada para o registry. Isso faz com que a imagem seja armazenada no Container Registry e fique disponível para uso e distribuição. Esse comando faz o upload da imagem simple-python-app:latest para o registry diego-cr na região especificada.





  
