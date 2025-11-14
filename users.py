import json
import os
import random
import string
from core.config import USERS_FILE, DATA_DIR

class UserManager:
    def __init__(self):
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        if not os.path.exists(USERS_FILE):
            with open(USERS_FILE, "w") as f:
                json.dump({}, f)

        with open(USERS_FILE, "r") as f:
            self.users = json.load(f)

    def save(self):
        with open(USERS_FILE, "w") as f:
            json.dump(self.users, f, indent=4)

    def create_activation_code(self):
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        self.users[code] = {"activated": False, "role": "user"}
        self.save()
        return code

    def activate_user(self, code):
        if code in self.users:
            self.users[code]["activated"] = True
            self.save()
            return True
        return False

    def list_users(self):
        return {k:v for k,v in self.users.items() if v["activated"]}

    def delete_user(self, code):
        if code in self.users:
            del self.users[code]
            self.save()
