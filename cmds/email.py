


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
    arg_2 = args[1] if len(args) > 1 else None
    arg_3 = args[2] if len(args) > 2 else None
    
    if arg_1 == 'create':
        email,token = await create_account()
        
        if email[0] == "Failed":
            await update.effective_message.reply_text(email['text'])
            return
        
        DataBaseJson.add_user_email(user_id,email,token)
        await update.effective_message.reply_text(f"New Temp Email Successfully Created!\n\nEmail: <code>{email}</code>\n\n When Used It AnyWhere For Get Messages Use: <code>/email messages email</code> or <code>/email msgs email</code>",parse_mode="HTML")
        
    elif arg_1 == 'list':
        user_emails = DataBaseJson.get_user_emails(user_id)
        
        if user_emails == {} or None:
            await update.effective_message.reply_text("🔰 You Have No Email Must Create Email(<code>/email create</code>) 🔰",parse_mode="HTML")
            return
        emails = "Your Emails:\n\n"
        for email in user_emails:
            emails+=f"   Email: <code>{email}</code>\n   Status: {DataBaseJson.get_user_email_status(user_id,email)}\n   Messages Count: {DataBaseJson.get_user_email_messages_count(user_id,email)}\n\n"          
            emails+=f"{"-"*40}\n"
    
        await update.effective_message.reply_text(emails,parse_mode="HTML")
        
    # i used chatgpt for make message better
    elif arg_1 == 'messages' or arg_1 == 'msgs':
        if not arg_2:
            await send_usage_message(update)
            return
        
        email = arg_2
        
        if not DataBaseJson.exist_email(user_id, email):
            await update.effective_message.reply_text("🔰 Email Not Found! 🔰")
            return

        token = DataBaseJson.get_user_email_token(user_id, email)
        messages = await get_messages(token)

        text = "Your Messages:\n\n"

        for msg in messages:
            message_id = msg['id']
            message = await get_message(token, message_id)

            subject = message.get("subject", "No subject")
            sender = message.get("from", {}).get("address", "Unknown sender")
            intro = message.get("intro", "")
            body = message.get("text", "")
            
            DataBaseJson.add_user_email_message(user_id,email,message_id,subject,sender,intro,body)

            text += (
                f"📩 **ID:** {message_id}\n"
                f"👤 **From:** {sender}\n"
                f"📌 **Subject:** {subject}\n"
                f"📝 **Preview:** {intro}\n"
                f"{'-'*40}\n"
            )

        text += f"\nTotal: {len(messages)} message(s)"

        await update.effective_message.reply_text(text, parse_mode="Markdown")
    
    elif arg_1 == 'read':
        if not arg_2 or not arg_3:
            await send_usage_message(update)
            return
        
        email = arg_2
        
        if not DataBaseJson.exist_email(user_id, email):
            await update.effective_message.reply_text("🔰 Email Not Found! 🔰")
            return
        
        message_id = arg_3
        
        message_body = DataBaseJson.get_user_email_message_body(user_id,email,message_id)
        
        await update.effective_message.reply_text(message_body)
      
    elif arg_1 == 'remove':
        if not arg_2:
            await send_usage_message(update)
            return
        
        email = arg_2
        
        if not DataBaseJson.exist_email(user_id, email):
            await update.effective_message.reply_text("🔰 Email Not Found! 🔰")
            return
        
        DataBaseJson.rem_user_email(user_id,email)
        await update.effective_message.reply_text(f"Email <code>{email}</code> Successfully Rmoved ✔",parse_mode="HTML")
        
    else:
        await send_usage_message(update)
    
# i used chatgpt for make usage message better
async def send_usage_message(update):
    """send usage message"""
    text = (
        "Usage:\n"
        " - <code>/email create</code> — Create a new temporary email\n"
        " - <code>/email list</code> — Show your created emails\n"
        " - <code>/email messages &lt;email&gt;</code> — Show received messages for that email\n"
        " - <code>/email msgs &lt;email&gt;</code> — Same as above (shortcut)\n"
        " - <code>/email read &lt;email&gt; &lt;message_id&gt;</code> — Read a full message\n"
        " - <code>/email remove &lt;email&gt;</code> — Remove an email from the system\n"
    )

    await update.effective_message.reply_text(text, parse_mode="HTML")


