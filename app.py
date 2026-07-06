import http.server
import json
import subprocess
import os
class SimpleHandler(http.server.BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_GET(self):
        if self.path == "/test-env":
            resposta = {
                "status": "Sucesso",
                "messagem": "Lendo variáveis de ambiente locais",
                "JWT_SECRET_DETECTED": os.getenv("JWT_SUPER_SECRET") is not None
            }
            self._send_json(resposta, 200)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/v1/ping":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                dados = json.loads(body)
            except ValueError:
                self._send_json({"erro": "JSON inválido."}, 400)
                return

            if not dados or 'host' not in dados:
                self._send_json({"erro": "O campo 'host' é obrigatório."}, 400)
                return

            host = dados['host']
            comando = ["ping", "-n", "1", host]
            try:
                resultado = subprocess.check_output(comando, text=True, stderr=subprocess.STDOUT)
                self._send_json({"status": "sucesso", "output": resultado}, status=200)
            except subprocess.CalledProcessError as e:
                self._send_json({"status": "erro", "output": e.output}, status=400)
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    print("Servidor nativo rodando na porta 5000...")
    server = http.server.HTTPServer(('0.0.0.0', 5000), SimpleHandler)
    server.serve_forever()