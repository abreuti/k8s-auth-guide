# Estudo de Readiness e Liveness no Kubernetes com Aplicação Simples (Python + Flask) + Docker

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

## Como funciona:
- A aplicação demora 10 segundos para se declarar pronta (readiness)
- Após 30 segundos de funcionamento, ela "quebra" e o livenessProbe começa a falhar
- O Kubernetes vai reiniciar o container automaticamente

### O que é testado aqui?
- Readiness Probe: controla quando o Kubernetes deve começar a enviar tráfego para o pod.
- Liveness Probe: detecta quando o container travou e precisa ser reiniciado.

---

## Construir a imagem Docker da aplicação e realizar o push para o Container Registry

Para criar a imagem Docker da aplicação, utilizei o seguinte comando:
```bash
docker build -t simple-python-app .
```

Como estou utilizando CR da Magalu Cloud, a região escolhida foi o DC da região Sudeste.
```bash
docker login https://container-registry.br-se1.magalu.cloud
```
> O comando docker login autentica o seu Docker com o Container Registry usando as credenciais obtidas pelo provedor de CR



Agora será necessário Taguear a Imagem Docker:
```bash
docker tag simple-python-app:latest container-registry.br-se1.magalu.cloud/diego-cr/simple-python-app:latest
```
> O comando docker tag associa uma imagem local com um nome e endereço de registry no Magalu Cloud. A imagem simple-python-app:latest será marcada para o registry diego-cr na região br-se1



Depois realizamos o Push da Imagem Docker:
```bash
docker push container-registry.br-se1.magalu.cloud/diego-cr/simple-python-app:latest
```
> O comando docker push envia a imagem marcada para o registry. Isso faz com que a imagem seja armazenada no Container Registry e fique disponível para uso e distribuição. Esse comando faz o upload da imagem simple-python-app:latest para o registry diego-cr na região especificada.

## Fazer o deploy no Kubernetes com a imagem no CR
Com a imagem enviada para o CR, crie o Deployment no Kubernetes usando o arquivo YAML https://github.com/abreuti/k8s-auth-guide/blob/main/liveness_readiness_files/deploy.yaml
```bash
kubectl apply -f simple-python-app.yaml
```
## Cenário Esperado
### A aplicação simula um comportamento real de serviços:
- Demora 10 segundos para se declarar pronta (/ready)
- Após 30 segundos, simula uma falha (/healthz começa a retornar erro)
### Kubernetes reage:
- Readiness: não envia tráfego até /ready retornar 200
- Liveness: reinicia o container quando /healthz retornar erro

### Como testar ?
- Verificar o Status do Pod
```bash
kubectl get pods
```
O pod vai iniciar com status 0/1, e após 10s irá para 1/1.
Depois de 30s, o container será reiniciado automaticamente pelo Kubernetes devido à falha simulada no /healthz.


## 📚 Estudo Pessoal

Este projeto foi criado como **estudo pessoal** sobre Kubernetes, probes e automação com Docker.  
Se você chegou até aqui, fique à vontade para usar como base para seus testes e estudos também!

  
