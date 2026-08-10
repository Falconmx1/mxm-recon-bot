import unittest
from unittest.mock import patch, MagicMock
from app.recon_runner import run_recon

class TestReconRunner(unittest.TestCase):
    
    @patch('app.recon_runner.subprocess.run')
    @patch('app.recon_runner.tempfile.TemporaryDirectory')
    def test_run_recon_success(self, mock_temp, mock_subprocess):
        """Prueba una ejecución exitosa del reconocimiento"""
        # Configurar mocks
        mock_temp.return_value.__enter__.return_value = "/tmp/fake_dir"
        
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Subdominios encontrados: test.com"
        mock_result.stderr = ""
        mock_subprocess.return_value = mock_result
        
        # Ejecutar
        result = run_recon("ejemplo.com")
        
        # Verificar
        self.assertIn("Subdominios encontrados", result)
        mock_subprocess.assert_called_once()
    
    @patch('app.recon_runner.subprocess.run')
    @patch('app.recon_runner.tempfile.TemporaryDirectory')
    def test_run_recon_failure(self, mock_temp, mock_subprocess):
        """Prueba que maneje errores del script"""
        mock_temp.return_value.__enter__.return_value = "/tmp/fake_dir"
        
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "Error: dominio inválido"
        mock_subprocess.return_value = mock_result
        
        with self.assertRaises(RuntimeError):
            run_recon("dominio-invalido")
    
    @patch('app.recon_runner.subprocess.run')
    def test_run_recon_timeout(self, mock_subprocess):
        """Prueba que maneje timeouts"""
        mock_subprocess.side_effect = TimeoutError("Timeout")
        
        with self.assertRaises(TimeoutError):
            run_recon("ejemplo.com")

if __name__ == '__main__':
    unittest.main()
