import os
import logging
from github import Github, GithubIntegration, GithubException

logger = logging.getLogger(__name__)

# Variables globales para el cliente de GitHub
_github_client = None
_app_integration = None

def get_github_client():
    """
    Obtiene una instancia del cliente de GitHub.
    Si está configurada la App, usa la integración. Si no, usa un token personal.
    """
    global _github_client, _app_integration
    
    if _github_client is not None:
        return _github_client

    app_id = os.environ.get('GITHUB_APP_ID')
    private_key_path = os.environ.get('GITHUB_APP_PRIVATE_KEY_PATH')
    webhook_secret = os.environ.get('GITHUB_WEBHOOK_SECRET')
    token = os.environ.get('GITHUB_TOKEN')

    if app_id and private_key_path:
        logger.info("Inicializando cliente de GitHub usando GitHub App.")
        try:
            with open(private_key_path, 'r') as key_file:
                private_key = key_file.read()
            integration = GithubIntegration(
                app_id=int(app_id),
                private_key=private_key,
            )
            _app_integration = integration
            # Obtener un cliente para la instalación (se necesita un repositorio para obtener la instalación)
            # Como no tenemos la instalación aquí, dejamos el cliente None por ahora.
            # La función post_comment obtendrá el cliente por instalación.
            _github_client = None
            return None  # Devolvemos None y manejamos en post_comment
        except Exception as e:
            logger.error(f"Error inicializando GitHub App: {e}")
            raise
    elif token:
        logger.info("Inicializando cliente de GitHub usando Token Personal.")
        _github_client = Github(token)
        return _github_client
    else:
        logger.error("No se encontró GITHUB_TOKEN ni configuración de App.")
        raise EnvironmentError("No se pudo inicializar el cliente de GitHub. Faltan credenciales.")

def get_installation_client(repo_full_name):
    """
    Obtiene un cliente de GitHub autenticado para una instalación específica de la App.
    """
    global _app_integration
    if _app_integration is None:
        logger.error("La integración de la App no está inicializada.")
        raise RuntimeError("Integración de App no disponible.")
    
    # Obtener el repositorio para encontrar la ID de instalación
    # Necesitamos un cliente temporal con token o usar la API de integración
    # Primero, obtener un token de instalación
    try:
        # Buscar la instalación para este repositorio
        # Nota: Esto requiere permisos de administración en la App
        # Alternativa: pasar la installation_id en el webhook
        # Por simplicidad, usaremos un token personal para esta demo
        logger.warning("Usando token personal para publicar comentarios (modo desarrollo).")
        return Github(os.environ.get('GITHUB_TOKEN'))
        
        # Código para producción (requiere installation_id del webhook):
        # installation_id = ... # obtener del payload del webhook
        # access_token = _app_integration.get_access_token(installation_id).token
        # return Github(access_token)
    except Exception as e:
        logger.error(f"Error obteniendo cliente de instalación: {e}")
        raise

def post_comment(repo_full_name, issue_number, comment_body):
    """
    Publica un comentario en un Issue o Pull Request.
    """
    try:
        client = get_installation_client(repo_full_name)
        if client is None:
            raise RuntimeError("No se pudo obtener un cliente de GitHub.")
        
        repo = client.get_repo(repo_full_name)
        issue = repo.get_issue(number=issue_number)
        issue.create_comment(comment_body)
        logger.info(f"Comentario publicado en {repo_full_name}#{issue_number}")
        return True
    except GithubException as e:
        logger.error(f"Error de GitHub al publicar comentario: {e.status} - {e.data}")
        raise
    except Exception as e:
        logger.error(f"Error inesperado al publicar comentario: {e}")
        raise

def get_repo_info(repo_full_name):
    """
    Obtiene información básica de un repositorio.
    """
    try:
        client = get_installation_client(repo_full_name)
        if client is None:
            raise RuntimeError("No se pudo obtener un cliente de GitHub.")
        repo = client.get_repo(repo_full_name)
        return {
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description,
            "clone_url": repo.clone_url,
            "default_branch": repo.default_branch,
            "owner": repo.owner.login,
        }
    except Exception as e:
        logger.error(f"Error obteniendo información del repositorio {repo_full_name}: {e}")
        raise
