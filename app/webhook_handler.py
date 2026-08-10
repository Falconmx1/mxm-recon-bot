import logging
import re
from .recon_runner import run_recon
from .github_client import post_comment, get_repo_info

logger = logging.getLogger(__name__)

def handle_webhook(event_type, payload):
    """
    Maneja diferentes tipos de eventos de GitHub.
    Por ahora, solo responde a 'issue_comment' y 'issues'.
    """
    logger.info(f"Procesando evento: {event_type}")

    if event_type == 'issue_comment':
        return handle_issue_comment(payload)
    elif event_type == 'issues':
        # Podrías manejar la creación de issues aquí si quieres
        return "Evento 'issues' recibido pero no procesado por ahora."
    else:
        logger.info(f"Evento '{event_type}' ignorado.")
        return f"Evento {event_type} ignorado."

def handle_issue_comment(payload):
    """
    Procesa el evento 'issue_comment'.
    Busca el comando /recon en el comentario.
    """
    comment_body = payload.get('comment', {}).get('body', '')
    issue_number = payload.get('issue', {}).get('number')
    repo_full_name = payload.get('repository', {}).get('full_name')
    sender = payload.get('sender', {}).get('login')

    if not issue_number or not repo_full_name:
        logger.warning("Payload incompleto: faltan issue_number o repo_full_name")
        return "Error: Payload incompleto."

    logger.info(f"Comentario de {sender} en {repo_full_name}#{issue_number}: {comment_body}")

    # Buscar el comando /recon <dominio>
    match = re.match(r'^/recon\s+(\S+)', comment_body.strip())
    if not match:
        logger.info("Comentario no contiene el comando /recon. Ignorando.")
        return "Comando no reconocido."

    target = match.group(1)
    logger.info(f"Comando /recon detectado. Objetivo: {target}")

    # Obtener información del repositorio (opcional)
    # repo_info = get_repo_info(repo_full_name)

    # Ejecutar el reconocimiento
    try:
        logger.info(f"Ejecutando reconocimiento para {target}...")
        result = run_recon(target)
        logger.info(f"Reconocimiento completado. Resultado: {result[:100]}...") # Log primeros 100 chars

        # Formatear el resultado para el comentario
        formatted_result = format_result_for_comment(target, result)
        
        # Publicar el comentario en el Issue
        post_comment(repo_full_name, issue_number, formatted_result)
        return f"Reconocimiento para {target} ejecutado y comentario publicado."
    
    except Exception as e:
        error_msg = f"Error al ejecutar el reconocimiento para {target}: {str(e)}"
        logger.error(error_msg)
        # Publicar un mensaje de error en el Issue
        post_comment(repo_full_name, issue_number, f"❌ **Error:** {error_msg}")
        return f"Error: {error_msg}"

def format_result_for_comment(target, raw_result):
    """
    Toma el resultado crudo del script y lo formatea para un comentario de GitHub.
    Puedes personalizar esto según la salida de tu script.
    """
    # Este es un ejemplo. Debes adaptarlo a la salida de tu script bugbounty-recon-mxm
    header = f"## 🚀 Reporte de Reconocimiento para `{target}`\n\n"
    footer = "\n\n---\n*Reporte generado automáticamente por [Mxm Recon Bot](https://github.com/Falconmx1/mxm-recon-bot).*"
    
    # Limitar el tamaño del comentario (GitHub tiene un límite)
    max_length = 65000  # GitHub permite hasta 65536 caracteres
    if len(raw_result) > max_length:
        raw_result = raw_result[:max_length] + "\n\n... (reporte truncado por longitud)"

    # Aquí podrías parsear el raw_result para hacerlo más bonito
    # Por ejemplo, buscar líneas con 'SUBOMINIOS:' y ponerlas en negrita.
    return header + raw_result + footer
