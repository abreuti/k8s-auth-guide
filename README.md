# Repositório de Estudos K8S

## Autenticação e Autorização no Kubernetes com certificado CSR

Este manual detalha o processo para criar um usuário no Kubernetes utilizando um certificado CSR, configurar RBAC e garantir que ele tenha permissão para listar pods.

Conteúdo absorvido no curso Introduction to Kubernetes (LFS158) da Linux Foundation Org. 
capitulo > 10. Authentication, Authorization, Admission Control

Pré-Requisitos:

Criar o namespace lfs158
```bash
kubectl create namespace lfs158
```
Criar um deployment simples para gerar pods àfim de testarmos as permissões posteriormente.
```bash
kubectl create deployment nginx-deployment --image=nginx:latest -n lfs158
```

Agora sim, partimos do ponto em que o ambiente possuí um namespace específico chamado lfs158 e nós temos uma aplicação nginx na qual está rodando nos pods. O objetivo final é garantir que o usuário bob não consiga listar os pods deste namespace.

---------------------------------------------BEGIN-------------------------------------------------

### 1. Gerar Chave Privada e CSR

Cada usuário no Kubernetes precisa de um certificado assinado pela CA do cluster. Primeiro, criamos a chave privada e o CSR.

O CSR (do inglês Certificate Signing Request, ou Pedido de Assinatura de Certificado) é um arquivo ou mensagem que contém informações sobre uma entidade (como um usuário, servidor ou dispositivo) que deseja obter um certificado digital assinado por uma Autoridade Certificadora (CA).No contexto do Kubernetes, o CSR é usado para solicitar que a CA do cluster assine um certificado digital para um usuário ou componente, permitindo que ele se autentique de forma segura no cluster.

Antes de criar um CSR, você gera uma chave privada (um arquivo criptográfico que só o solicitante deve ter). A chave privada é usada para criar o CSR e, posteriormente, para assinar transações ou autenticar o usuário.

### 1.1 Gerar a Chave Privada
```yaml
openssl genpkey -algorithm RSA -out bob.key
```
### 1.2 Gerar um CSR (Certificate Signing Request)
O CSR é gerado a partir da chave privada e contém informações como:
- Nome do solicitante (por exemplo, o nome do usuário no Kubernetes).
- Domínio ou endereço (se aplicável).
- Chave pública (derivada da chave privada).
Essas informações são codificadas em um formato padrão (como PEM) e enviadas para a CA.
```yaml
openssl req -new -key bob.key -out bob.csr -subj "/CN=bob/O=developers"
```
CN=bob → Nome do usuário

O=developers → Grupo do usuário

### 2. Criar um CSR no Kubernetes

O Kubernetes precisa assinar nosso CSR. A Autoridade Certificadora (CA) verifica as informações no CSR e, se tudo estiver correto, assina o CSR com sua própria chave privada. Isso gera um certificado digital que pode ser usado pelo solicitante para se autenticar.

### 2.1 Converter o CSR para Base64
O Kubernetes espera que o CSR seja codificado em Base64 antes de ser enviado.
```yaml
cat bob.csr | base64 | tr -d '\n'
```
### 2.2 Criar o YAML do CSR

Crie o arquivo bob-csr.yaml:
```yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: bob-csr
spec:
  request: LS0tLS1...(CSR codificado em Base64)
  signerName: kubernetes.io/kube-apiserver-client
  usages:
    - digital signature
    - key encipherment
    - client auth
```
Substitua LS0tLS1... pelo CSR codificado em Base64.

### 2.3 Aplicar o CSR no Kubernetes
```bash
kubectl apply -f bob-csr.yaml
```
### 2.4 Aprovar o CSR
```bash
kubectl certificate approve bob-csr
```
### 2.5 Obter o Certificado Assinado
```bash
kubectl get csr bob-csr -o jsonpath='{.status.certificate}' | base64 --decode > bob.crt
```
Agora temos:
bob.key → Chave privada
bob.crt → Certificado assinado

### 3. Configurar Permissões com RBAC

Por padrão, o usuário não tem permissão para acessar o cluster.

### 3.1 Criar uma Role para acessar pods

Crie bob-role.yaml:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list"]
```
### 3.2 Criar um RoleBinding para associar o usuário

Crie bob-rolebinding.yaml:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  namespace: default
  name: bob-rolebinding
subjects:
  - kind: User
    name: bob  # CN do certificado
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```
### 3.3 Aplicar as permissões no Kubernetes
```bash
kubectl apply -f bob-role.yaml
kubectl apply -f bob-rolebinding.yaml
```
### 4. Configurar o Usuário no Kubectl

Agora, adicionamos bob ao kubectl.

### 4.1 Adicionar o Usuário
```bash
kubectl config set-credentials bob \
  --client-certificate=bob.crt \
  --client-key=bob.key \
  --embed-certs=true
```
### 4.2 Criar um Contexto para o Usuário
No Kubernetes, contexto (ou context) é um conceito usado para gerenciar múltiplos clusters, usuários e namespaces de forma organizada. Neste guide vamos usar diferentes contextos para setar credenciais do usuário bob e testar as permissões.
```bash
kubectl config set-context bob-context \
  --cluster=$(kubectl config view --minify -o jsonpath='{.clusters[0].name}') \
  --namespace=default \
  --user=bob
```
### 4.3 Alternar para o Contexto de bob
```bash
kubectl config use-context bob-context
```
### 5. Testar Acesso aos Pods

Agora testamos se bob consegue acessar os pods.
```bash
kubectl get pods
```
Se funcionar, você verá a lista de pods. Se aparecer "Forbidden", verifique se os RoleBindings estão aplicados corretamente.

Conclusão

Este manual cobre desde a criação do certificado CSR até a autenticação e permissões no Kubernetes usando RBAC.

Agora, o usuário bob pode acessar e listar pods no namespace lfs158 de forma segura. 🚀