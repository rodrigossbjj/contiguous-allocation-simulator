#!/bin/bash

# Script para compilar o simulador de alocação contígua em um executável autônomo

echo "================================================="
echo "  Preparando a compilação do Simulador...        "
echo "================================================="

# Diretório do ambiente virtual temporário
TEMP_VENV="build_venv"

# 1. Verificar se o pyinstaller já está disponível globalmente
if command -v pyinstaller &> /dev/null; then
    echo "✔ PyInstaller encontrado no sistema."
    echo "🚀 Iniciando a compilação..."
    pyinstaller --onefile --name simulador main.py
else
    echo "PyInstaller não encontrado. Criando ambiente virtual temporário..."
    
    # Cria o ambiente virtual
    python3 -m venv "$TEMP_VENV"
    if [ $? -ne 0 ]; then
        echo "❌ Erro ao criar o ambiente virtual."
        exit 1
    fi
    
    # Ativa o ambiente virtual
    source "$TEMP_VENV"/bin/activate
    
    # Instala o pyinstaller no ambiente virtual
    echo "Instalando o PyInstaller no ambiente virtual..."
    pip install --upgrade pip &> /dev/null
    pip install pyinstaller
    
    if [ $? -ne 0 ]; then
        echo "❌ Erro ao instalar o PyInstaller no ambiente virtual."
        deactivate
        rm -rf "$TEMP_VENV"
        exit 1
    fi
    
    # Executar a compilação
    echo "🚀 Iniciando a compilação com PyInstaller..."
    pyinstaller --onefile --name simulador main.py
    COMPILE_STATUS=$?
    
    # Desativa e remove o venv temporário
    deactivate
    rm -rf "$TEMP_VENV"
    
    if [ $COMPILE_STATUS -ne 0 ]; then
        echo "❌ Ocorreu um erro durante a compilação."
        exit 1
    fi
fi

# 2. Limpeza dos arquivos temporários gerados pelo pyinstaller
echo "🧹 Limpando arquivos de compilação temporários..."
rm -rf build/ simulador.spec

if [ -f "dist/simulador" ]; then
    echo "================================================="
    echo "🎉 COMPILAÇÃO CONCLUÍDA COM SUCESSO!"
    echo "O executável autônomo foi gerado no caminho:"
    echo "👉 ./dist/simulador"
    echo "================================================="
else
    echo "❌ Arquivo executável não encontrado em dist/."
    exit 1
fi
