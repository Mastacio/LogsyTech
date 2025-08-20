#!/bin/bash

# Script de pruebas para verificar el despliegue Docker
# Autor: Sistema de Cotizaciones

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_message() {
    echo -e "${GREEN}[TEST]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  Pruebas de CotizApp Docker${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Función para verificar si un puerto está en uso
check_port() {
    local port=$1
    local service=$2
    
    if ss -tlnp | grep -q ":$port "; then
        print_message "$service está ejecutándose en puerto $port"
        return 0
    else
        print_error "$service NO está ejecutándose en puerto $port"
        return 1
    fi
}

# Función para verificar respuesta HTTP
check_http_response() {
    local url=$1
    local service=$2
    
    if curl -s -o /dev/null -w "%{http_code}" "$url" | grep -q "200\|302"; then
        print_message "$service responde correctamente en $url"
        return 0
    else
        print_error "$service NO responde correctamente en $url"
        return 1
    fi
}

# Función para verificar contenedores Docker
check_docker_containers() {
    print_message "Verificando contenedores Docker..."
    
    # Verificar que los contenedores estén ejecutándose
    if docker-compose ps | grep -q "Up"; then
        print_message "Contenedores Docker están ejecutándose"
        
        # Mostrar estado de contenedores
        echo ""
        docker-compose ps
        echo ""
        return 0
    else
        print_error "Contenedores Docker NO están ejecutándose"
        return 1
    fi
}

# Función para verificar base de datos
check_database() {
    print_message "Verificando conexión a base de datos externa..."
    
    # Verificar si existe el archivo .env
    if [ ! -f ".env" ]; then
        print_error "Archivo .env no encontrado"
        return 1
    fi
    
    # Cargar variables de entorno
    source .env
    
    # Verificar conexión usando Django desde el contenedor
    if docker-compose exec -T web python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotes.settings_docker')
django.setup()
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
    print('Conexión exitosa')
except Exception as e:
    print(f'Error de conexión: {e}')
    exit(1)
" >/dev/null 2>&1; then
        print_message "Conexión a PostgreSQL externa exitosa"
        return 0
    else
        print_error "Error conectando a PostgreSQL externa"
        return 1
    fi
}

# Función para verificar aplicación Django
check_django_app() {
    print_message "Verificando aplicación Django..."
    
    # Verificar que Django puede conectarse a la base de datos
    if docker-compose exec -T web python manage.py check >/dev/null 2>&1; then
        print_message "Django está configurado correctamente"
        return 0
    else
        print_error "Django NO está configurado correctamente"
        return 1
    fi
}

# Función para verificar archivos estáticos
check_static_files() {
    print_message "Verificando archivos estáticos..."
    
    if docker-compose exec -T web test -d /app/staticfiles; then
        print_message "Archivos estáticos están configurados"
        return 0
    else
        print_warning "Archivos estáticos NO están configurados"
        return 1
    fi
}

# Función para verificar logs
check_logs() {
    print_message "Verificando logs de la aplicación..."
    
    # Verificar que no hay errores críticos en los logs
    if docker-compose logs web | grep -i "error\|exception" | wc -l | grep -q "0"; then
        print_message "No se encontraron errores críticos en los logs"
        return 0
    else
        print_warning "Se encontraron errores en los logs"
        echo "Últimos logs de la aplicación:"
        docker-compose logs --tail=20 web
        return 1
    fi
}

# Función para mostrar información del sistema
show_system_info() {
    print_message "Información del sistema:"
    echo "  - Docker version: $(docker --version)"
    echo "  - Docker Compose version: $(docker-compose --version)"
    echo "  - Sistema operativo: $(uname -s) $(uname -r)"
    echo "  - Memoria disponible: $(free -h | grep Mem | awk '{print $7}')"
    echo "  - Espacio en disco: $(df -h . | tail -1 | awk '{print $4}')"
}

# Función principal de pruebas
run_tests() {
    local tests_passed=0
    local total_tests=0
    
    print_header
    show_system_info
    echo ""
    
    # Test 1: Verificar contenedores Docker
    total_tests=$((total_tests + 1))
    if check_docker_containers; then
        tests_passed=$((tests_passed + 1))
    fi
    echo ""
    
    # Test 2: Verificar base de datos
    total_tests=$((total_tests + 1))
    if check_database; then
        tests_passed=$((tests_passed + 1))
    fi
    echo ""
    
    # Test 3: Verificar aplicación Django
    total_tests=$((total_tests + 1))
    if check_django_app; then
        tests_passed=$((tests_passed + 1))
    fi
    echo ""
    
    # Test 4: Verificar puerto 8002
    total_tests=$((total_tests + 1))
    if check_port 8002 "Aplicación web"; then
        tests_passed=$((tests_passed + 1))
    fi
    echo ""
    
    # Test 5: Verificar configuración de base de datos externa
    total_tests=$((total_tests + 1))
    if [ -f ".env" ]; then
        print_message "Archivo .env encontrado - Base de datos externa configurada"
        tests_passed=$((tests_passed + 1))
    else
        print_error "Archivo .env no encontrado - Base de datos externa no configurada"
    fi
    echo ""
    
    # Test 6: Verificar respuesta HTTP
    total_tests=$((total_tests + 1))
    if check_http_response "http://localhost:8002" "Aplicación web"; then
        tests_passed=$((tests_passed + 1))
    fi
    echo ""
    
    # Test 7: Verificar archivos estáticos
    total_tests=$((total_tests + 1))
    if check_static_files; then
        tests_passed=$((tests_passed + 1))
    fi
    echo ""
    
    # Test 8: Verificar logs
    total_tests=$((total_tests + 1))
    if check_logs; then
        tests_passed=$((tests_passed + 1))
    fi
    echo ""
    
    # Mostrar resumen
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  Resumen de Pruebas${NC}"
    echo -e "${BLUE}================================${NC}"
    echo -e "Pruebas pasadas: ${GREEN}$tests_passed/$total_tests${NC}"
    
    if [ $tests_passed -eq $total_tests ]; then
        echo -e "${GREEN}🎉 ¡Todas las pruebas pasaron! Tu aplicación está funcionando correctamente.${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠️  Algunas pruebas fallaron. Revisa los errores arriba.${NC}"
        return 1
    fi
}

# Función para mostrar ayuda
show_help() {
    echo "Uso: $0 [OPCIÓN]"
    echo ""
    echo "Opciones:"
    echo "  test      - Ejecutar todas las pruebas (opción por defecto)"
    echo "  logs      - Mostrar logs de la aplicación"
    echo "  status    - Mostrar estado de contenedores"
    echo "  help      - Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 test     # Ejecutar pruebas"
    echo "  $0 logs     # Ver logs"
    echo "  $0 status   # Ver estado"
}

# Función principal
main() {
    case "${1:-test}" in
        "test")
            run_tests
            ;;
        "logs")
            docker-compose logs -f
            ;;
        "status")
            docker-compose ps
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_error "Opción desconocida: $1"
            show_help
            exit 1
            ;;
    esac
}

# Ejecutar función principal
main "$@"
