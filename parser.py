class ArgumentError(Exception):
    pass

class Command:
    def __init__(self, name, command, usage: str = None, description: str = "Not Implemented.", number_of_args: int = None, aliases: list[str] = []):
        self.name = name
        self.command = command
        self.usage = usage
        if usage == None:
            self.usage = f"{self.name} *args"
        self.description = description
        self.aliases = aliases
        self.number_of_args = number_of_args


    def __call__(self, *args):
        return self.command(*args)

class Parser:
    def __init__(self, commands: list[Command]):
        self.commands: dict[str, Command] = {}
        for command in commands:
            self.add_command(command=command)

        self.add_command(Command("help", self.help, description="Provides documentation for commands.", aliases=['h']))

    def help(self, *args):

        if len(args) > 1:
            raise ArgumentError("Too Many Arguments. Help takes 0 or 1 argument.")

        if len(args) == 0:
            docs = []
            for command in set(self.commands.values()):
                docs.append(f'{command.name}: {command.description}')
            return "\n".join(docs)

        commandName = args[0]
            
        if commandName not in self.commands:
            return "Command Not Found."

        command = self.commands[commandName]
        docs = f"Function \"{command.name}\"\n\tAliases: {command.aliases}\n\tUsage: {command.usage}\n\tDescription: {command.description}"
        return docs


    def add_command(self, command: Command):
        aliases = command.aliases
        name = command.name
        for x in [name, *aliases]:
            self.commands[x] = command

    def check_commas(self, inputs: list):
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
        
        return form_inputs

    def parse(self, inp):
        inputs = inp.split(" ")
        form_inputs = self.check_commas(inputs)

        command = form_inputs[0]
        arguments = form_inputs[1:]

        if self.commands[command].number_of_args is not None:
            if len(arguments) != self.commands[command].number_of_args:
                raise ArgumentError

        return {command: arguments}
    
    def parse_run(self, inp):
        parsed = self.parse(inp)
        command = self.commands[list(parsed.keys())[0]]
        arguments = list(parsed.values())[0]
        returned_val = command(*arguments)
        return returned_val

# Testing
if __name__ == "__main__":
    def add(*args): return str(sum([int(x) for x in args]))
    def say(*args): print(*args)

    x = Parser([Command("say", print, description="Says what you ask it to say", aliases=['print'])])
    while True:
        inp = input("❯ ")
        if inp.strip() == "":
            continue
        out = x.parse_run(inp)
        if out is not None:
            print(out)

