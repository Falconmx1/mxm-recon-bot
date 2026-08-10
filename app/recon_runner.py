import subprocess
import os
import logging
import tempfile

logger = logging.getLogger(__name__)

def run_recon(target):
    """
    Ejecuta el script de reconocimiento 'bugbounty-recon-mxm' contra un objetivo.
    Asume que el script está disponible en el sistema o en una ruta específica.
    """
    # IMPORTANTE: Ajusta la ruta a tu script. 
    # Si está en el repositorio, puedes clonarlo o embeberlo.
    # Aquí asumimos que se llama 'bugbounty-recon-mxm' y está en el PATH.
    script_name = "bugbounty-recon-mxm"
    
    # También podrías usar una ruta absoluta:
    # script_path = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'recon_wrapper.sh')
    
    logger.info(f"Preparando ejecución de {script_name} para {target}")

    # Crear un directorio temporal para resultados (opcional)
    with tempfile.TemporaryDirectory() as temp_dir:
        logger.info(f"Usando directorio temporal: {temp_dir}")
        
        # Comando a ejecutar. 
        # Asumiendo que tu script acepta -d <dominio> y -o <directorio>
        cmd = [
            script_name,
            "-d", target,
            "-o", temp_dir
        ]
        
        try:
            logger.info(f"Ejecutando comando: {' '.join(cmd)}")
            # Ejecutar el script y capturar salida
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutos máximo
                check=False   # No lanzar excepción si falla, manejamos el código de retorno
            )
            
            # Combinar stdout y stderr para tener toda la información
            output = result.stdout + "\n" + result.stderr
            
            if result.returncode != 0:
                logger.warning(f"El script terminó con código {result.returncode}. Output: {output[:500]}")
                # Podrías lanzar una excepción o devolver el error
                raise RuntimeError(f"El script falló con código {result.returncode}. Revisa los logs.")
            
            logger.info(f"Reconocimiento completado. Tamaño del output: {len(output)} caracteres")
            return output
            
        except subprocess.TimeoutExpired:
            logger.error("El reconocimiento excedió el tiempo límite (5 minutos).")
            raise TimeoutError("El reconocimiento tomó demasiado tiempo.")
        except FileNotFoundError:
            logger.error(f"No se encontró el script '{script_name}'. Asegúrate de que esté instalado y en el PATH.")
            raise FileNotFoundError(f"Script '{script_name}' no encontrado.")
        except Exception as e:
            logger.error(f"Error inesperado ejecutando el reconocimiento: {e}")
            raise
