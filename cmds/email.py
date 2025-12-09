


from telegram import Update
from telegram.ext import ContextTypes



from db.db import DataBaseJson
from helper import Permission
from api.mail import create_account,get_messages,get_message



async def email(update:Update, context:ContextTypes.DEFAULT_TYPE):
    
    user = update.effective_user
    
    user_id = user.id
        
    if not DataBaseJson.exist(user_id):
        DataBaseJson.add_user(user_id)
    
    if not Permission.have_access(user_id):
        await update.effective_message.reply_text("🔰 You Do Not Have Access To Use '/email' Command! 🔰")
        return
    
    args = context.args
    
    if not args:
        await send_usage_message(update)
        return
    
    arg_1 = args[0]
    arg_2 = args[1]
    
    if arg_1 == 'create':
        email,token = await create_account()
        
        if email['status'] == "Failed":
            await update.effective_message.reply_text(email['text'])
            return
        
        DataBaseJson.add_user_email(user_id,email,token)
        await update.effective_message.reply_text(f"New Temp Email Successfully Created!\n\nEmail: <code>{email}\n\n When Used It AnyWhere For Get Messages Use: <code>/email <messages:msgs> <email>")
        
    elif arg_1 == 'list':
        user_emails = DataBaseJson.get_user_emails(user_id)
        
        if user_emails == {} or None:
            await update.effective_message.reply_text("🔰 You Have No Email Must Create Email(<code>/email create</code>) 🔰")
            return
        
        for email in user_emails:
            emails = "Your Emails:\n\n"
            emails+=f" - <code>{email}</code>\n   Status: {DataBaseJson.get_user_email_status(email)}\n"          
        
        await update.effective_message.reply_text(emails)
        
    elif arg_1 == 'messages' or 'msgs':
        if not arg_2:
            await send_usage_message(update)
            return
        
        email = arg_2
        token = DataBaseJson.get_user_email_token(user_id,email)
        messages = await get_messages(token)
        
        for message in messages:
            text="Your Messages:\n ID - Message"
            message_id = message['id']
            message_text = get_message(token,message_id)
            text+=f" {message_id} - {message_text}\n"
        
        text+=f"Count {len(messages)}"
        await update.effective_message.reply_text(text)
        
    elif arg_1 == 'remove':
        if not arg_2:
            await send_usage_message(update)
            return
        
        email = arg_2
        
        if not DataBaseJson.exist_email(user_id, email):
            await update.effective_message.reply_text("🔰 Email Not Found! 🔰")
            return
        
        DataBaseJson.rem_user_email(user_id,email)
        await update.effective_message.reply_text(f"✔ Email <code>{email}</code> Successfully Rmoved ✔")
        
    else:
        await send_usage_message(update)
    

async def send_usage_message(update):
    """send usage message"""
    await update.effective_message.reply_text("Usage: /email <create:list> or /email <messages:msgs:remove> <email>")
    

