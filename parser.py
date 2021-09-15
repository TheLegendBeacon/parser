class Command:
    def __init__(self, command, docs: str):
        self.command = command
        self.docs = docs

    def __call__(self, *args):
        self.command(*args)

class Parser:
    def __init__(self, commands: dict[str, Command]):
        self.commands = commands
        self.commands["help"] = Command(self.help, "Prints documentation of the function.")

    def help(self, commandName: str):
        for x in self.commands:
            if x == commandName:
                print(self.commands[x].docs)

    def parse(self, inp):
        inputs = inp.split(" ")
        form_inputs = []
        temp_list = []

        inquote = False
        for x in inputs:
            if list(x).count('"') % 2 == 0:
                if not inquote:
                    form_inputs.append(x.replace('"', ''))
                else:
                    temp_list.append(x)
            else:
                if inquote == False:
                    inquote = True
                    temp_list.append(x.replace('"', ''))
                else:
                    temp_list.append(x.replace('"', ''))
                    total_string = " ".join(temp_list)
                    form_inputs.append(total_string)
                    temp_list = []
                    inquote = False


        command = form_inputs[0]
        arguments = form_inputs[1:]

        return {command: arguments}
    
    def parse_run(self, inp):
        parsed = self.parse(inp)
        command = self.commands[list(parsed.keys())[0]]
        arguments = list(parsed.values())[0]
        returned_val = command(*arguments)
        if returned_val is not None:
            print(returned_val)

# Testing
if __name__ == "__main__":
    x = Parser({"say": Command(print, "Function \"Say\": \n\tUsage: say *args\n\tDescription: echoes whatever u say") })
    x.parse_run("say hi \"how r u\"")
    x.parse("help help")
