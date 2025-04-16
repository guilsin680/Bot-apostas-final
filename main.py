from predictor import prever_jogos_hoje
from telegram_bot import enviar_mensagem

if __name__ == "__main__":
    mensagens = prever_jogos_hoje()
    for msg in mensagens:
        enviar_mensagem(msg)
