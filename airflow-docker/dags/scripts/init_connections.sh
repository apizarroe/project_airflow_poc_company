#!/bin/bash
# Script para inicializar conexiones SMTP en Airflow

echo "Verificando conexión SMTP..."

# Verificar si la conexión smtp_default ya existe
if /entrypoint airflow connections get smtp_default > /dev/null 2>&1; then
    echo "Conexión smtp_default ya existe"
else
    echo "Creando conexión smtp_default para Yahoo..."
    /entrypoint airflow connections add 'smtp_default' \
        --conn-type 'smtp' \
        --conn-host 'smtp.mail.yahoo.com' \
        --conn-port 587 \
        --conn-login "${YAHOO_USER}" \
        --conn-password "${YAHOO_APP_PASSWORD}" \
        --conn-extra '{"disable_ssl": true, "from_email": "'"${YAHOO_USER}"'"}'

    echo "Conexión smtp_default creada exitosamente"
fi
