import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from mcstatus import JavaServer
from dotenv import load_dotenv
import os

# Configurar logging para ver as informações
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Função que será executada quando o comando /start for recebido
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Olá! Eu sou o seu bot. Use /help para ver os comandos disponíveis.')

# Função que será executada para qualquer mensagem de texto que não seja um comando
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Você disse: {update.message.text}')

# Função para mostrar o status do servidor Minecraft
async def mcstatus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        server = JavaServer.lookup("177.143.63.131:25565")
        status = server.status()
        resposta = (
            f"Servidor online!\n"
            f"Jogadores online: {status.players.online}/{status.players.max}\n"
            f"Versão: {status.version.name}"
        )
    except Exception as e:
        resposta = f"Servidor offline ou não foi possível obter o status.\nErro: {e}"
    await update.message.reply_text(resposta)

# Função principal para configurar e rodar o bot
def main():
    # Usa o token do arquivo .env
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

    # Cria a aplicação do bot
    application = ApplicationBuilder().token(TOKEN).build()

    # Adiciona handlers (manipuladores) para diferentes tipos de mensagens
    # CommandHandler para comandos (ex: /start)
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # CommandHandler para /ServerMine
    servermine_handler = CommandHandler('ServerMine', mcstatus)
    application.add_handler(servermine_handler)

    # Remover o handler antigo do /mcstatus
    # application.add_handler(mcstatus_handler)

    # MessageHandler para mensagens de texto que não são comandos
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)

    # Inicia o bot (usa long polling para receber atualizações)
    logging.info("Bot started...")
    application.run_polling(poll_interval=3)
    logging.info("Bot stopped.")

if __name__ == '__main__':
    main()



