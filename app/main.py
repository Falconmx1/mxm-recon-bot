import os
import logging
from flask import Flask, request, Response
from .webhook_handler import handle_webhook

# Configurar logging básico
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Endpoint principal que recibe los webhooks de GitHub.
    """
    # Verificar que sea un evento de GitHub
    event_type = request.headers.get('X-GitHub-Event')
    signature = request.headers.get('X-Hub-Signature-256')
    
    if not event_type:
        logger.warning("Petición recibida sin cabecera X-GitHub-Event")
        return Response("Bad Request: Missing GitHub Event", status=400)

    # Obtener el payload en JSON
    payload = request.json
    if not payload:
        logger.warning("Petición sin payload JSON")
        return Response("Bad Request: Missing JSON Payload", status=400)

    logger.info(f"Evento recibido: {event_type}")

    # Manejar el evento usando nuestro manejador
    try:
        response_message = handle_webhook(event_type, payload)
        return Response(response_message, status=200)
    except Exception as e:
        logger.error(f"Error procesando el webhook: {e}")
        return Response(f"Internal Server Error: {e}", status=500)

@app.route('/health', methods=['GET'])
def health():
    """
    Endpoint simple para verificar que el servidor está vivo.
    """
    return "Mxm Recon Bot is running!", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Iniciando servidor en el puerto {port}")
    app.run(host='0.0.0.0', port=port)
