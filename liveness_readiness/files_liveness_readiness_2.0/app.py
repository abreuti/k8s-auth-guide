from flask import Flask
import threading
import time

app = Flask(__name__)

is_ready = False
is_alive = True

def simulate_startup():
    global is_ready
    time.sleep(10)
    is_ready = True
    print("✅ App está pronto (readiness = true)")

def simulate_failure():
    global is_alive
    time.sleep(30)
    is_alive = False
    print("💥 App falhou (liveness = false)")

# Threads simulando comportamento
threading.Thread(target=simulate_startup).start()
threading.Thread(target=simulate_failure).start()

@app.route("/")
def index():
    return "<h1>Olá, Kubernetes!</h1>"

@app.route("/ready")
def readiness():
    return ("", 200) if is_ready else ("", 503)

@app.route("/healthz")
def liveness():
    return ("", 200) if is_alive else ("", 500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
