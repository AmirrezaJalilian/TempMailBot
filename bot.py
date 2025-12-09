


from telegram import Update
from  telegram.ext import CommandHandler, ApplicationBuilder


from cmds.start import start
from cmds.email import email



def main():
    
    
    bot = ApplicationBuilder().token("").build()
    
    
    bot.add_handler(CommandHandler("start",start))
    bot.add_handler(CommandHandler("email",email))
    
    
    bot.run_polling()



if __name__ == "__main__":
    main()


