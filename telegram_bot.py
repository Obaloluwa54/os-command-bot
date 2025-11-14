import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters
)
from core.config import TELEGRAM_TOKEN
from core.users import UserManager
from core.github_tools import GitHubManager
from core.sandbox import Sandbox
from core.logs import LogManager
from core.tools import ToolRegistry

# -------------------------
# LOGGER
# -------------------------
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# -------------------------
# INIT MODULES
# -------------------------
users = UserManager()
github = GitHubManager()
sandbox = Sandbox()
logs = LogManager()
tools = ToolRegistry()

ADMIN_CHAT_ID = None  # Put your Telegram ID here if you want admin commands restricted

# -------------------------
# COMMANDS
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id in users.list_users():
        await update.message.reply_text(
            "Welcome back! Use /help to see available commands."
        )
    else:
        await update.message.reply_text(
            "Welcome! You need an activation code to use this bot. Use /register to request access."
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
Available Commands:
/start - Start the bot
/register - Request an activation code
/activate <code> - Activate your account
/run <tool> [args] - Run a tool in sandbox
/repos - List cloned GitHub repos
/clone <repo_url> - Clone a repo
/pull <repo_name> - Pull updates from a repo
/tools - List allowed tools
/logs - List logs
/admin - Admin commands (if authorized)
"""
    await update.message.reply_text(help_text)

# -------------------------
# USER REGISTRATION
# -------------------------
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    code = users.create_activation_code()
    await update.message.reply_text(
        f"Your activation code has been created. Send it to the admin for approval: {code}"
    )

async def activate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) == 0:
        await update.message.reply_text("Usage: /activate <activation_code>")
        return
    code = args[0]
    if users.activate_user(code):
        await update.message.reply_text("Your account has been activated! You can now run tools.")
    else:
        await update.message.reply_text("Invalid activation code.")

# -------------------------
# RUN TOOL
# -------------------------
async def run_tool(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id not in users.list_users():
        await update.message.reply_text("You are not activated. Use /register and get approval.")
        return
    if len(context.args) == 0:
        await update.message.reply_text("Usage: /run <tool> [arguments]")
        return
    tool = context.args[0]
    args = " ".join(context.args[1:]) if len(context.args) > 1 else ""
    output = sandbox.run(tool, args)
    log_path = logs.save_log(tool, output)
    await update.message.reply_text(f"Output:\n{output}\nLog saved at: {log_path}")

# -------------------------
# GITHUB COMMANDS
# -------------------------
async def clone_repo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Usage: /clone <repo_url>")
        return
    url = context.args[0]
    msg = github.clone_repo(url)
    await update.message.reply_text(msg)

async def pull_repo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Usage: /pull <repo_name>")
        return
    repo = context.args[0]
    msg = github.pull_repo(repo)
    await update.message.reply_text(msg)

async def list_repos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    repo_list = github.list_repos()
    await update.message.reply_text("Cloned Repos:\n" + "\n".join(repo_list))

# -------------------------
# TOOLS & LOGS
# -------------------------
async def list_tools(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tool_list = tools.list_tools()
    await update.message.reply_text("Allowed Tools:\n" + "\n".join(tool_list))

async def list_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_list = logs.list_logs()
    await update.message.reply_text("Logs:\n" + "\n".join(log_list))

# -------------------------
# MAIN FUNCTION
# -------------------------
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Basic commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("activate", activate))
    app.add_handler(CommandHandler("run", run_tool))
    app.add_handler(CommandHandler("clone", clone_repo))
    app.add_handler(CommandHandler("pull", pull_repo))
    app.add_handler(CommandHandler("repos", list_repos))
    app.add_handler(CommandHandler("tools", list_tools))
    app.add_handler(CommandHandler("logs", list_logs))

    print("Telegram bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
