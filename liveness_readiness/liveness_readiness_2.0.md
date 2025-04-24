# Experimentos interessantes pra fazer com o objetivo de entender o comportamento de Read/Live(ness) e alguns debugs. 

## 1. Mudar a lógica da app https://github.com/abreuti/k8s-auth-guide/blob/main/liveness_readiness_1.0.md
- Deixar o readiness sempre False e vê se o pod entra no Service (não entra).
- Deixar o liveness sempre False e vê se ele reinicia em loop.

Loga tempo de requests, mostra quanto tempo demorou pra readiness ficar OK, etc.

## 2. Ver comportamento no cluster
- Fazer um watch kubectl get pods -o wide e acompanha o ciclo.
- Usar kubectl get endpoints pra ver se o pod tá no Service mesmo.

## 3. Testar escalabilidade
- Mudar replicas: 3 e vê se todos sobem certo (ou se todos caem juntos).
- Testar readiness em um só pod e vêr se o LoadBalancer manda tráfego pros outros.
