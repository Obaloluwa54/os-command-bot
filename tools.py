class ToolRegistry:
    def __init__(self):
        # List all tools your bot can run
        self.tools = ["python", "bash", "node"]

    def list_tools(self):
        return self.tools

    def add_tool(self, tool_name):
        if tool_name not in self.tools:
            self.tools.append(tool_name)
            return True
        return False

    def remove_tool(self, tool_name):
        if tool_name in self.tools:
            self.tools.remove(tool_name)
            return True
        return False
