# Repositório de Estudos K8S

## Admission Control in Kubernetes

Este manual detalha o processo para criar um processo de admissão de controles no Kubernetes.

Conteúdo absorvido no curso Introduction to Kubernetes (LFS158) da Linux Foundation Org. 
Capitulo > 10. Authentication, Authorization, Admission Control

O Admission Controller no Kubernetes é um mecanismo que permite interceptar e processar solicitações à API do Kubernetes antes que elas sejam persistidas no etcd (o armazenamento de chave-valor do Kubernetes). Ele age como um "porteiro", validando ou modificando as solicitações conforme necessário.


Validar a solicitação (Validating Admission Controller):
- Decide se a solicitação deve ser permitida ou negada.
- Exemplo: Impedir a criação de um Pod sem rótulos específicos.

Modificar a solicitação (Mutating Admission Controller):
- Altera a solicitação antes que ela seja persistida.
- Exemplo: Adicionar automaticamente um rótulo ou sidecar a um Pod.