# 🚀 Mxm Recon Bot

[![GitHub Marketplace](https://img.shields.io/badge/Marketplace-v1.0-blue?logo=github)](https://github.com/marketplace)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

> **🤖 GitHub App que automatiza el reconocimiento de Bug Bounty directamente desde tus Issues y Pull Requests.**

## ✨ Características

- 🔍 **Subdomain Discovery**: Encuentra subdominios activos usando herramientas como Subfinder o Amass.
- 🌐 **HTTP Probing**: Verifica qué subdominios están respondiendo y qué servicios están corriendo.
- 🛡️ **Escaneo de Vulnerabilidades**: Ejecuta Nuclei para encontrar CVEs, configuraciones inseguras y vulnerabilidades conocidas.
- 📊 **Reporte Automatizado**: Publica un comentario detallado en tu Issue o PR con los hallazgos organizados.
- 🔒 **Seguro y Aislado**: Cada escaneo se ejecuta en un entorno efímero. Versión gratuita para repositorios públicos.
- 🧩 **Fácil de usar**: Solo instala la App y usa el comando `/recon` en tus Issues.

## 🎯 Cómo Funciona

1.  **Instala** la App de Mxm Recon Bot desde GitHub Marketplace en tu repositorio.
2.  **Activa** un escaneo abriendo un Issue o Pull Request y escribiendo el comando:
    `/recon dominio.com`
    (Reemplaza `dominio.com` con el objetivo que quieras analizar).
3.  El bot **recibe el evento** a través de un webhook, clona el repositorio (o usa el contexto) y ejecuta el flujo de reconocimiento.
4.  Una vez terminado, **publica un comentario** en el Issue/PR con un resumen ejecutivo y los hallazgos detallados.

## 🛠️ Tecnologías y Dependencias

- **Backend**: Python 3.9+ con Flask.
- **Integración con GitHub**: PyGithub y la API de GitHub.
- **Herramientas de Reconocimiento** (integradas en el script `bugbounty-recon-mxm`):
    - [Subfinder](https://github.com/projectdiscovery/subfinder)
    - [HTTPx](https://github.com/projectdiscovery/httpx)
    - [Nuclei](https://github.com/projectdiscovery/nuclei)
    - [Nmap](https://nmap.org/)
- **Infraestructura**: Diseñado para ser desplegado en servicios como Railway, Heroku o AWS.

## 📦 Instalación Local para Desarrollo

Sigue estos pasos para tener una copia local y poder hacer pruebas:

```bash
# 1. Clonar el repositorio
git clone https://github.com/Falconmx1/mxm-recon-bot.git
cd mxm-recon-bot

# 2. Crear y activar un entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar las dependencias
pip install -r requirements.txt

# 4. Configurar las variables de entorno
cp .env.example .env
# Edita el archivo .env con tus credenciales (App ID, Private Key, etc.)

# 5. (Opcional) Instalar herramientas de reconocimiento
# Asegúrate de tener Subfinder, HTTPx, Nuclei y Nmap en tu PATH.

# 6. Ejecutar el servidor en modo desarrollo
python app/main.py
