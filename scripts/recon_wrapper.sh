#!/bin/bash

# scripts/recon_wrapper.sh
# Wrapper para ejecutar bugbounty-recon-mxm desde la GitHub App

set -e  # Salir si hay algún error

# --- Configuración ---
# Directorio donde está tu script principal (ajusta la ruta)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RECON_SCRIPT="${SCRIPT_DIR}/../bugbounty-recon-mxm"  # O la ruta donde tengas el script

# Variables para colores (opcional, para logs más bonitos)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# --- Funciones de ayuda ---
usage() {
    echo "Uso: $0 -d <dominio> -o <directorio_salida> [-v]"
    echo "  -d <dominio>       Dominio objetivo para el reconocimiento"
    echo "  -o <directorio>    Directorio donde guardar los resultados"
    echo "  -v                 Modo verbose (activa logs detallados)"
    exit 1
}

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# --- Validación de dependencias ---
check_dependencies() {
    local missing_deps=()
    
    # Verificar que las herramientas principales existen
    for tool in subfinder httpx nuclei nmap; do
        if ! command -v $tool &> /dev/null; then
            missing_deps+=($tool)
        fi
    done
    
    # Verificar que tu script principal existe
    if [ ! -f "$RECON_SCRIPT" ] && [ ! -x "$RECON_SCRIPT" ]; then
        log_error "No se encontró el script de reconocimiento en: $RECON_SCRIPT"
        log_error "Asegúrate de que bugbounty-recon-mxm esté en la ruta correcta."
        exit 1
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        log_warn "Faltan herramientas opcionales: ${missing_deps[*]}"
        log_warn "El reconocimiento podría no funcionar al 100%."
    fi
}

# --- Función principal de ejecución ---
run_recon() {
    local domain="$1"
    local output_dir="$2"
    local verbose="$3"
    
    log_info "Iniciando reconocimiento para dominio: $domain"
    log_info "Directorio de salida: $output_dir"
    
    # Crear directorio de salida si no existe
    mkdir -p "$output_dir"
    
    # Ejecutar el script de reconocimiento
    # Asumiendo que tu script acepta -d (dominio) y -o (salida)
    local cmd="$RECON_SCRIPT -d $domain -o $output_dir"
    
    if [ "$verbose" = "true" ]; then
        cmd="$cmd -v"
        log_info "Modo verbose activado"
    fi
    
    log_info "Ejecutando: $cmd"
    
    # Capturar salida y errores
    if eval "$cmd" 2>&1 | tee "${output_dir}/recon.log"; then
        log_info "✅ Reconocimiento completado exitosamente"
        return 0
    else
        local exit_code=$?
        log_error "❌ El reconocimiento falló con código $exit_code"
        log_error "Revisa el log en: ${output_dir}/recon.log"
        return $exit_code
    fi
}

# --- Generación de resumen (opcional) ---
generate_summary() {
    local output_dir="$1"
    local summary_file="${output_dir}/summary.txt"
    
    log_info "Generando resumen en: $summary_file"
    
    {
        echo "=== RESUMEN DE RECONOCIMIENTO ==="
        echo "Fecha: $(date)"
        echo ""
        echo "--- Subdominios encontrados ---"
        if [ -f "${output_dir}/subdomains.txt" ]; then
            wc -l "${output_dir}/subdomains.txt" | awk '{print "Total: " $1 " subdominios"}'
            head -n 10 "${output_dir}/subdomains.txt" || echo "No se encontraron subdominios"
        else
            echo "No se generó archivo de subdominios"
        fi
        echo ""
        echo "--- Puertos abiertos ---"
        if [ -f "${output_dir}/open_ports.txt" ]; then
            cat "${output_dir}/open_ports.txt" | head -n 10 || echo "No se encontraron puertos abiertos"
        else
            echo "No se generó archivo de puertos"
        fi
        echo ""
        echo "--- Vulnerabilidades (Nuclei) ---"
        if [ -f "${output_dir}/nuclei_results.txt" ]; then
            grep -c "\[" "${output_dir}/nuclei_results.txt" 2>/dev/null || echo "0" | awk '{print "Total vulnerabilidades: " $1}'
            head -n 5 "${output_dir}/nuclei_results.txt" || echo "No se encontraron vulnerabilidades"
        else
            echo "No se generó archivo de vulnerabilidades"
        fi
    } > "$summary_file"
    
    log_info "✅ Resumen generado en: $summary_file"
    cat "$summary_file"
}

# --- Main ---
main() {
    # Parsear argumentos
    local domain=""
    local output_dir=""
    local verbose="false"
    
    while getopts "d:o:vh" opt; do
        case $opt in
            d) domain="$OPTARG" ;;
            o) output_dir="$OPTARG" ;;
            v) verbose="true" ;;
            h) usage ;;
            *) usage ;;
        esac
    done
    
    # Validar argumentos obligatorios
    if [ -z "$domain" ] || [ -z "$output_dir" ]; then
        log_error "Faltan argumentos obligatorios"
        usage
    fi
    
    # Validar que el directorio de salida sea escribible
    if [ -e "$output_dir" ] && [ ! -w "$output_dir" ]; then
        log_error "El directorio $output_dir no es escribible"
        exit 1
    fi
    
    # Verificar dependencias
    check_dependencies
    
    # Ejecutar reconocimiento
    if run_recon "$domain" "$output_dir" "$verbose"; then
        # Generar resumen (útil para el comentario de GitHub)
        generate_summary "$output_dir"
        exit 0
    else
        exit 1
    fi
}

# Ejecutar main con todos los argumentos
main "$@"
