import config
from chatbot import Butler

if __name__ == '__main__':
  alfred = Butler(config.BOT_EMAIL, config.BOT_PASSWORD, config.OUTPUTDIR)
  alfred.listen()
