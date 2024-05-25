import sys

class Console_handler:
    def __init__(self, MainFrame):
        self.MainFrame = MainFrame

    def get_console_input(self, text):
        lines = text.split("\n")
        command = self.get_last_non_empty_line(lines)
        if command:
            self.command_list(command)

    def get_last_non_empty_line(self, lines):
        for line in reversed(lines):
            if line.strip():
                return line.strip().split()

    def command_list(self, commands):
        if not commands:
            return
        elif commands[0] == "Exit":
            sys.exit(0)
        elif commands[0] == "Save":
            if len(commands) > 1:
                if commands[1] == "--all":
                    self.MainFrame.main_terminal.append("Saving all\n")
                elif commands[1] == "--mnplot":
                    self.MainFrame.main_terminal.append("Saving numerical method plot\n")
                elif commands[1] == "--numpyplot":
                    self.MainFrame.main_terminal.append("Saving numpy plot\n")
                elif commands[1] == "--scipyplot":
                    self.MainFrame.main_terminal.append("Saving scipy plot\n")
                else:
                    self.MainFrame.main_terminal.append(f"Invalid Save command: {commands[1]}\n")
            else:
                self.MainFrame.main_terminal.append("Save command requires an argument\n")
        elif commands[0] == "Refresh":
            if len(commands) > 1:
                if commands[1] == "--all":
                    self.MainFrame.main_terminal.append("Refreshing all\n")
                elif commands[1] == "--mnplot":
                    self.MainFrame.main_terminal.append("Saving numerical method plot\n")
                elif commands[1] == "--numpyplot":
                    self.MainFrame.main_terminal.append("Saving numpy plot\n")
                elif commands[1] == "--scipyplot":
                    self.MainFrame.main_terminal.append("Saving scipy plot\n")
                else:
                    self.MainFrame.main_terminal.append(f"Invalid Refresh command: {commands[1]}\n")
            else:
                self.MainFrame.main_terminal.append("Refresh command requires an argument\n")
        elif commands[0] == "Clear":
            if len(commands) >1:
                if commands[1] == "console":
                    self.MainFrame.main_terminal.clear()
                else:
                    self.MainFrame.main_terminal.append(f"Invalid Clear command: {commands[1]}\n")
            else:
                self.MainFrame.main_terminal.append("Clear command requires an argument\n")
        else:
            self.MainFrame.main_terminal.append(f"There is no such command as: {commands[0]}\n")