# Guía de Configuración para Mxm Recon Bot

## Requisitos Previos

- Python 3.9 o superior
- Cuenta de GitHub con permisos para crear Apps
- (Opcional) Herramientas de reconocimiento instaladas:
  - [Subfinder](https://github.com/projectdiscovery/subfinder)
  - [HTTPx](https://github.com/projectdiscovery/httpx)
  - [Nuclei](https://github.com/projectdiscovery/nuclei)
  - [Nmap](https://nmap.org/)

## Configuración Local para Desarrollo

### 1. Clonar el Repositorio
```bash
git clone https://github.com/Falconmx1/mxm-recon-bot.git
cd mxm-recon-bot

2. Crear Entorno Virtual

python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
3. Instalar Dependencias

pip install -r requirements.txt
4. Configurar Variables de Entorno

cp .env.example .env
# Edita .env con tus credenciales
5. Configurar el Script de Reconocimiento
Coloca tu script bugbounty-recon-mxm en la raíz del proyecto o en scripts/

Asegúrate de que sea ejecutable: chmod +x scripts/recon_wrapper.sh
