#!/bin/bash

echo "🚀 Configurando Bot Monitor Dashboard..."

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env..."
    cp .env.example .env
    echo "⚠️  Recuerda configurar tu TWITTER_BEARER_TOKEN en .env"
fi

# Crear directorios necesarios
mkdir -p static/css static/js templates config

echo ""
echo "✅ ¡Entorno configurado!"
echo ""
echo "📋 Próximos pasos:"
echo "   1. Configura .env con tu Twitter Bearer Token"
echo "   2. Edita config/bots.yml con tus bots"
echo "   3. Ejecuta: python app.py"
echo "   4. Abre: http://localhost:5000"
echo ""
echo "📚 Documentación: cat README.md"
echo ""
