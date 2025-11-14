import subprocess
from core.config import SANDBOX_PATH, ALLOWED_TOOLS, DATA_DIR
import os

class Sandbox:
    def __init__(self):
        if not os.path.exists(SANDBOX_PATH):
            os.makedirs(SANDBOX_PATH)

    def run(self, tool, args=""):
        if tool not in ALLOWED_TOOLS:
            return f"Tool '{tool}' is not allowed."

        try:
            result = subprocess.run(
                [tool] + args.split(),
                cwd=SANDBOX_PATH,
                capture_output=True,
                text=True,
                timeout=300
            )
            return result.stdout + "\n" + result.stderr
        except subprocess.TimeoutExpired:
            return "Execution timed out."
        except Exception as e:
            return f"Error: {str(e)}"
