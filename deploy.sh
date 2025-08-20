#!/bin/bash

# Script para desplegar CotizApp en Docker
# Autor: Sistema de Cotizaciones
# Versión: 1.0

set -e  # Salir si hay algún error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con colores
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  Despliegue de CotizApp Docker${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Función para verificar si Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker no está instalado. Por favor instala Docker primero."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose no está instalado. Por favor instala Docker Compose primero."
        exit 1
    fi
    
    print_message "Docker y Docker Compose están instalados correctamente."
}

# Función para crear backup de la base de datos actual
create_database_backup() {
    print_message "Creando backup de la base de datos actual..."
    
    if [ -f "db.sqlite3" ]; then
        # Crear backup de SQLite
        cp db.sqlite3 db.sqlite3.backup
        print_message "Backup de SQLite creado: db.sqlite3.backup"
        
        # Convertir SQLite a SQL para PostgreSQL
        print_message "Convirtiendo datos de SQLite a PostgreSQL..."
        python manage.py dumpdata --exclude auth.permission --exclude contenttypes > backup_data.json
        print_message "Datos exportados a backup_data.json"
    else
        print_warning "No se encontró db.sqlite3. Se creará una base de datos nueva."
    fi
}

# Función para preparar la configuración de Docker
prepare_docker_config() {
    print_message "Preparando configuración de Docker..."
    
    # Crear directorios necesarios
    mkdir -p static media
    print_message "Directorios static y media creados"
}

# Función para construir y ejecutar los contenedores
build_and_run() {
    print_message "Construyendo imagen de Docker..."
    docker-compose build
    
    print_message "Iniciando servicios..."
    docker-compose up -d
    
    print_message "Esperando que la base de datos esté lista..."
    sleep 10
    
    # Ejecutar migraciones
    print_message "Ejecutando migraciones..."
    docker-compose exec web python manage.py migrate
    
    # Cargar datos de backup si existe
    if [ -f "backup_data.json" ]; then
        print_message "Cargando datos de backup..."
        docker-compose exec web python manage.py loaddata backup_data.json
        print_message "Datos cargados exitosamente"
    fi
    
    # Recolectar archivos estáticos
    print_message "Recolectando archivos estáticos..."
    docker-compose exec web python manage.py collectstatic --noinput
    
    print_message "¡Despliegue completado exitosamente!"
}

# Función para mostrar información del despliegue
show_deployment_info() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  Información del Despliegue${NC}"
    echo -e "${BLUE}================================${NC}"
    echo -e "${GREEN}Aplicación:${NC} http://localhost:8002"
    echo -e "${GREEN}Admin Django:${NC} http://localhost:8002/admin"
    
    # Leer información de la base de datos desde .env
    if [ -f ".env" ]; then
        source .env
        echo -e "${GREEN}Base de datos:${NC} PostgreSQL externa"
        echo -e "${GREEN}Host DB:${NC} ${DB_HOST:-postgreSql}"
        echo -e "${GREEN}Puerto DB:${NC} ${DB_PORT:-5432}"
        echo -e "${GREEN}Nombre DB:${NC} ${DB_NAME:-LogsyTech}"
        echo -e "${GREEN}Usuario DB:${NC} ${DB_USER:-UserSystem}"
    else
        echo -e "${GREEN}Base de datos:${NC} Configuración no encontrada"
    fi
    echo ""
    echo -e "${YELLOW}Comandos útiles:${NC}"
    echo -e "  Ver logs: ${GREEN}docker-compose logs -f${NC}"
    echo -e "  Parar servicios: ${GREEN}docker-compose down${NC}"
    echo -e "  Reiniciar: ${GREEN}docker-compose restart${NC}"
    echo -e "  Acceder al contenedor: ${GREEN}docker-compose exec web bash${NC}"
    echo ""
    echo -e "${YELLOW}Nota:${NC} Los datos se mantienen en la base de datos externa PostgreSQL"
}

# Función para limpiar recursos
cleanup() {
    print_message "Limpiando recursos..."
    docker-compose down -v
    docker system prune -f
    print_message "Limpieza completada"
}

# Función para mostrar ayuda
show_help() {
    echo "Uso: $0 [OPCIÓN]"
    echo ""
    echo "Opciones:"
    echo "  deploy     - Desplegar la aplicación (opción por defecto)"
    echo "  clean      - Limpiar contenedores y volúmenes"
    echo "  logs       - Mostrar logs de los contenedores"
    echo "  restart    - Reiniciar servicios"
    echo "  shell      - Acceder al shell del contenedor web"
    echo "  backup     - Crear backup de la base de datos"
    echo "  help       - Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 deploy    # Desplegar la aplicación"
    echo "  $0 clean     # Limpiar todo"
    echo "  $0 logs      # Ver logs"
}

# Función principal
main() {
    case "${1:-deploy}" in
        "deploy")
            print_header
            check_docker
            create_database_backup
            prepare_docker_config
            build_and_run
            show_deployment_info
            ;;
        "clean")
            print_message "Limpiando contenedores y volúmenes..."
            cleanup
            ;;
        "logs")
            docker-compose logs -f
            ;;
        "restart")
            print_message "Reiniciando servicios..."
            docker-compose restart
            ;;
        "shell")
            docker-compose exec web bash
            ;;
        "backup")
            create_database_backup
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
