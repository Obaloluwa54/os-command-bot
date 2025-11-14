from core.users import UserManager

class Admin:
    def __init__(self):
        self.users = UserManager()

    def approve_user(self, code):
        """Activate a pending user"""
        return self.users.activate_user(code)

    def delete_user(self, code):
        self.users.delete_user(code)

    def list_pending(self):
        return [k for k,v in self.users.users.items() if not v["activated"]]

    def broadcast(self, message, telegram_app, chat_ids):
        """
        Send a message to all users via Telegram bot
        telegram_app: telegram.ext.Application instance
        chat_ids: list of user chat IDs
        """
        for cid in chat_ids:
            try:
                telegram_app.bot.send_message(chat_id=cid, text=message)
            except Exception as e:
                print(f"Failed to send to {cid}: {str(e)}")
