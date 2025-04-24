#!/bin/bash
# Script para rodar o bot Telegram em background no Ubuntu

set -e

# Instala dependências do sistema
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

# Cria ambiente virtual se não existir
test -d .venv || python3 -m venv .venv

# Ativa ambiente virtual
echo "Ativando ambiente virtual..."
source .venv/bin/activate

# Instala dependências do projeto
pip install --upgrade pip
pip install python-telegram-bot mcstatus

# Executa o bot em background
nohup python3 app.py > bot.log 2>&1 &
echo "Bot iniciado em background. Veja logs em bot.log"
