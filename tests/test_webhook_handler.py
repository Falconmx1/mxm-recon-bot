import unittest
import json
from app.webhook_handler import handle_webhook, handle_issue_comment

class TestWebhookHandler(unittest.TestCase):
    
    def setUp(self):
        """Configuración antes de cada prueba"""
        self.payload_comment = {
            "comment": {
                "body": "/recon ejemplo.com"
            },
            "issue": {
                "number": 1
            },
            "repository": {
                "full_name": "Falconmx1/test-repo"
            },
            "sender": {
                "login": "test-user"
            }
        }
    
    def test_handle_issue_comment_valid_command(self):
        """Prueba que detecte el comando /recon correctamente"""
        # Esta prueba asume que no ejecutará realmente el reconocimiento
        # Por ahora, solo verificamos que no lance excepción
        try:
            result = handle_issue_comment(self.payload_comment)
            self.assertIsInstance(result, str)
        except Exception as e:
            self.fail(f"handle_issue_comment lanzó excepción: {e}")
    
    def test_handle_issue_comment_invalid_command(self):
        """Prueba que ignore comandos inválidos"""
        payload_invalid = self.payload_comment.copy()
        payload_invalid["comment"]["body"] = "Hola mundo"
        
        result = handle_issue_comment(payload_invalid)
        self.assertEqual(result, "Comando no reconocido.")
    
    def test_handle_webhook_ignore_event(self):
        """Prueba que ignore eventos no soportados"""
        result = handle_webhook("ping", {})
        self.assertEqual(result, "Evento ping ignorado.")

if __name__ == '__main__':
    unittest.main()
