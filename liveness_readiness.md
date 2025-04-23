# Estudo de Readiness e Liveness no Kubernetes com Aplicação Simples (Python + Flask) + Docker

> **Este projeto é um estudo pessoal**. A finalidade é aprender e aplicar conhecimentos sobre Liveness e Readiness em Kubernetes. O código não é voltado para produção, mas sim para fins educacionais e experimentação.

Este projeto demonstra como rodar uma aplicação simples em Python com Flask dentro de um container Docker e gerenciar sua execução no Kubernetes. A aplicação serve uma página web com a mensagem "Olá, Kubernetes!".

## Pré-requisitos

- [Docker](https://www.docker.com/get-started)
- [Kubernetes](https://kubernetes.io/docs/setup/)
- Conta na [Magalu Cloud](https://console.magalu.cloud/) para utilizar o CR (Container Registry)

...

## Estrutura do Projeto

A pasta https://github.com/abreuti/k8s-auth-guide/tree/main/liveness_readiness_files 
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
Antes de acessar o Container Registry da Magalu Cloud no cluster Kubernetes, precisei configurar uma secret para o K8S conseguir baixar a imagem.

Usei este comando substituindo os valores corretamente, segue exemplo abaixo:
```bash
kubectl create secret docker-registry regcred \
  --docker-server=container-registry.br-se1.magalu.cloud \
  --docker-username=<seu-usuario> \
  --docker-password=<seu-token-ou-senha> \
  --docker-email=<seu-email>
```
>**Um ponto de atenção aqui e que ocorreu erro em meu deploy, foi que esqueci de referenciar a secret no arquivo yaml, isso gerou erro ao realizar pull da imagem do CR. Importante setar esta configuração usando o 
        imagePullSecrets:
        - name: regcred**

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

Deixei o pod rodando por alguns minutos e percebi que haviam 5 restarts realizados

![image](https://github.com/user-attachments/assets/07b1a74f-9e8f-4011-bf1f-6725c056e395)

Ao realizar um describe no pod, recebi os seguintes eventos

![image](https://github.com/user-attachments/assets/06672018-2cb5-4492-b414-b25baef17d13)

## Eventos Observados
Abaixo está a lista de eventos observados no Kubernetes para o pod simple-python-app, com explicações sobre cada etapa.

Assigned to Node - O pod foi agendado com sucesso em um nó do cluster Kubernetes.
```bash
Normal   Scheduled  6m35s                  default-scheduler  Successfully assigned default/simple-python-app-5dcb55c65b-45sfk to np-default-jvztq-nzpcl
```

Image Pulled - A imagem foi puxada com sucesso do container registry da Magalu Cloud.
```bash
Normal   Pulled     6m29s                  kubelet            Successfully pulled image "container-registry.br-se1.magalu.cloud/diego-cr/simple-python-app:latest" in 6.098s (6.098s including waiting). Image size: 55337330 bytes.
```

Container Created & Started - O container foi criado e iniciado com sucesso.
```bash
Normal   Created    4m19s (x3 over 6m29s)  kubelet            Created container simple-python-app
Normal   Started    4m19s (x3 over 6m28s)  kubelet            Started container simple-python-app
```
Readiness Probe Failed (503) - A Readiness Probe falhou inicialmente, retornando 503. Isso é esperado, pois a aplicação simula um tempo de inicialização e só se torna "pronta" após 10 segundos.
```bash
Warning  Unhealthy  4m11s (x5 over 6m23s)  kubelet            Readiness probe failed: HTTP probe failed with statuscode: 503
```
Liveness Probe Failed (500) - Após 30 segundos, a aplicação simulou uma falha e a Liveness Probe retornou 500. Isso indicou que o aplicativo não estava saudável.
```bash
Warning  Unhealthy  3m45s (x3 over 5m55s)  kubelet            Liveness probe failed: HTTP probe failed with statuscode: 500
```
Container Restarted - Como a Liveness Probe falhou, o Kubernetes reiniciou o container automaticamente.
```bash
Normal   Killing    3m45s (x3 over 5m55s)  kubelet            Container simple-python-app failed liveness probe, will be restarted
```
Re-pulling Image - O Kubernetes tentou puxar novamente a imagem do registry para criar um novo pod.
```bash
Normal   Pulled     3m14s                  kubelet            Successfully pulled image "container-registry.br-se1.magalu.cloud/diego-cr/simple-python-app:latest" in 440ms (440ms including waiting). Image size: 55337330 bytes.
```

## Comportamento esperado da aplicação com probes simulados
A aplicação Flask foi criada para simular dois comportamentos comuns em ambientes Kubernetes:
- Readiness Delay: demora 10 segundos para estar pronta (/ready responde 503 até então).
- Liveness Failure: "quebra" após 30 segundos de execução (/healthz passa a responder 500).


## 📚 Estudo Pessoal

Este projeto foi criado como **estudo pessoal** sobre Kubernetes, probes e automação com Docker.  
Se você chegou até aqui, fique à vontade para usar como base para seus testes e estudos também!

  
