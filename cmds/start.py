

from telegram import Update,Chat
from telegram.ext import ContextTypes


async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    
    try:
        chat_type = update.effective_chat.type
    except:
        chat_type = None
        
    user = update.effective_user
    
    if chat_type in ["private","PRIVATE","Private"]:
        await update.effective_message.reply_text(f"Hello {user.mention_html()}, Welcome To {context.bot.username}!")

