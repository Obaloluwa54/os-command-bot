import os
import time
from core.users import UserManager
from core.github_tools import GitHubManager
from core.sandbox import Sandbox
from core.logs import LogManager
from core.tools import ToolRegistry
from core.config import Config

class DevOpsNinja:
    def __init__(self):
        self.users = UserManager()
        self.github = GitHubManager()
        self.sandbox = Sandbox()
        self.logs = LogManager()
        self.tools = ToolRegistry()
        self.running = True

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def banner(self):
        print("""
██████╗ ███████╗██╗   ██╗ ██████╗ ██████╗ ███████╗
██╔══██╗██╔════╝██║   ██║██╔═══██╗██╔══██╗██╔════╝
██████╔╝█████╗  ██║   ██║██║   ██║██║  ██║█████╗  
██╔══██╗██╔══╝  ██║   ██║██║   ██║██║  ██║██╔══╝  
██║  ██║███████╗╚██████╔╝╚██████╔╝██████╔╝███████╗
╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝ ╚══════╝
    DevOps Ninja — Terminal Control System
        """)

    def main_menu(self):
        while self.running:
            self.clear()
            self.banner()

            print("""
[1] User Management
[2] GitHub Manager
[3] Run Tool (Sandbox)
[4] Logs Viewer
[5] Registered Tools
[6] Exit
""")
            choice = input("Select: ")

            if choice == "1":
                self.menu_users()

            elif choice == "2":
                self.menu_github()

            elif choice == "3":
                self.menu_run_tool()

            elif choice == "4":
                self.menu_logs()

            elif choice == "5":
                self.menu_registered_tools()

            elif choice == "6":
                self.running = False

    # ---------------------------
    # User Menu
    # ---------------------------
    def menu_users(self):
        self.clear()
        print("== USER MANAGEMENT ==")
        print("""
[1] Create Activation Code
[2] View Users
[3] Delete User
[0] Back
""")

        choice = input("Select: ")

        if choice == "1":
            code = self.users.create_activation_code()
            print(f"\nActivation Code Created: {code}")
            input("\nPress Enter...")

        elif choice == "2":
            print("\nRegistered Users:")
            for user in self.users.list_users():
                print(f"- {user}")
            input("\nPress Enter...")

        elif choice == "3":
            uid = input("Enter user ID to delete: ")
            self.users.delete_user(uid)
            print("User removed.")
            input("\nPress Enter...")

    # ---------------------------
    # GitHub Menu
    # ---------------------------
    def menu_github(self):
        self.clear()
        print("== GITHUB MANAGER ==")
        print("""
[1] Clone Repository
[2] Pull Updates
[3] List Repos
[0] Back
""")

        choice = input("Select: ")

        if choice == "1":
            url = input("GitHub Repo URL: ")
            self.github.clone_repo(url)
            input("\nPress Enter...")

        elif choice == "2":
            repo = input("Repo Name: ")
            self.github.pull_repo(repo)
            input("\nPress Enter...")

        elif choice == "3":
            repos = self.github.list_repos()
            for r in repos:
                print("-", r)
            input("\nPress Enter...")

    # ---------------------------
    # Tool Runner
    # ---------------------------
    def menu_run_tool(self):
        self.clear()
        print("== RUN TOOL IN SANDBOX ==")

        tool = input("Tool Name: ")
        args = input("Arguments (optional): ")

        output = self.sandbox.run(tool, args)
        print("\n=== TOOL OUTPUT ===\n")
        print(output)

        log_path = self.logs.save_log(tool, output)
        print(f"\nLog saved at: {log_path}")

        input("\nPress Enter...")

    # ---------------------------
    # Logs Viewer
    # ---------------------------
    def menu_logs(self):
        self.clear()
        print("== LOGS ==")
        logs = self.logs.list_logs()

        for l in logs:
            print("-", l)

        fname = input("\nOpen log file: ")
        print("\n" + self.logs.read_log(fname))

        input("\nPress Enter...")

    # ---------------------------
    # Registered Tools
    # ---------------------------
    def menu_registered_tools(self):
        self.clear()
        print("== REGISTERED TOOLS ==")
        for t in self.tools.list_tools():
            print("-", t)
        input("\nPress Enter...")


if __name__ == "__main__":
    app = DevOpsNinja()
    app.main_menu()
