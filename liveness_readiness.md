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

Ao realizar um describe no pod, recebi os seguintes eventos

![image](https://github.com/user-attachments/assets/14038f7e-ecf5-45c6-bad1-602d7cde9c3a)

## Comportamento esperado da aplicação com probes simulados
A aplicação Flask foi criada para simular dois comportamentos comuns em ambientes Kubernetes:
- Readiness Delay: demora 10 segundos para estar pronta (/ready responde 503 até então).
- Liveness Failure: "quebra" após 30 segundos de execução (/healthz passa a responder 500).

### Resultado observado
No kubectl describe pod, os eventos confirmam o comportamento:
- Readiness Probe falha inicialmente com 503, o que é esperado nos primeiros 10 segundos.
- Depois que a aplicação “quebra” (aos 30s), a Liveness Probe começa a falhar com 500.
- O Kubernetes detecta a falha e reinicia automaticamente o container, como demonstrado pelo evento Killing.

Ciclo contínuo - Esse ciclo continua indefinidamente:
- App sobe,
- após 10s fica pronta (readiness = OK),
- após 30s quebra (liveness = NOK),
- container é reiniciado,
- volta pro passo 1.


## 📚 Estudo Pessoal

Este projeto foi criado como **estudo pessoal** sobre Kubernetes, probes e automação com Docker.  
Se você chegou até aqui, fique à vontade para usar como base para seus testes e estudos também!

  
