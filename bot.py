import requests
from telegram.ext import ApplicationBuilder, CommandHandler
import os

# -------------------------
# CONFIGURATION
# -------------------------
TELEGRAM_BOT_TOKEN = "7970970211:AAHrCjs6oFzgaZPBxkZYTe65MMf2_tWw2gw"
GITHUB_TOKEN = "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"   # must have workflow + repo permissions
REPO = "kumarraj1242ddis/xxx"             # <---- your repo, e.g. "myuser/myrepo"
BRANCH = "main"
# -------------------------

async def zz(update, context):
    # expecting exactly 3 numbers
    if len(context.args) != 3:
        await update.message.reply_text("Usage: /zz <num1> <num2> <num3>")
        return

    num1, num2, num3 = context.args

    # ensure all are numbers
    if not (num1.isdigit() and num2.isdigit() and num3.isdigit()):
        await update.message.reply_text("Please send only numbers.\nExample: /zz 10 20 30")
        return

    await update.message.reply_text(f"Starting workflow with: {num1} {num2} {num3}")

    url = f"https://api.github.com/repos/{REPO}/actions/workflows/run_zz.yml/dispatches"

    payload = {
        "ref": BRANCH,
        "inputs": {
            "num1": num1,
            "num2": num2,
            "num3": num3
        }
    }

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    r = requests.post(url, json=payload, headers=headers)

    if r.status_code in (201, 204):
        await update.message.reply_text("Workflow started! Running 50 parallel jobs.")
    else:
        await update.message.reply_text(f"Error starting workflow:\n{r.text}")


app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(CommandHandler("zz", zz))

app.run_polling()
