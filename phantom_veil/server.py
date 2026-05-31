"""HTTP server for Phantom-Veil management and metrics."""
import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from phantom_veil.core import PhantomVeil
from phantom_veil.metrics import metrics

logger = logging.getLogger("phantom-veil.server")

class VeilHandler(BaseHTTPRequestHandler):
    veil: PhantomVeil = None

    def do_GET(self):
        if self.path == "/health":
            self._json_response({"status": "ok"})
        elif self.path == "/status":
            self._json_response(self.veil.get_status())
        elif self.path == "/metrics":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(metrics.export_prometheus().encode())
        else:
            self._json_response({"error": "not found"}, 404)

    def _json_response(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        pass  # Suppress default logging

def run_server(veil: PhantomVeil, host: str = "0.0.0.0", port: int = 9090):
    VeilHandler.veil = veil
    server = HTTPServer((host, port), VeilHandler)
    logger.info(f"Phantom-Veil server running on {host}:{port}")
    server.serve_forever()

if __name__ == "__main__":
    veil = PhantomVeil()
    veil.init()
    run_server(veil)
