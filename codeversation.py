import re
import argparse

class CVInterpreter:
    def __init__(self):
        self.variables = {}
        self.if_exec = False

    def parse_line(self, line):
        line = line.strip()
        if re.match(r"^[a-zA-Z_]\w* is \d+$", line):
            var, value = line.split(" is ")
            self.variables[var.strip()] = int(value.strip())
        elif re.match(r'^[a-zA-Z_]\w* is ".*"$', line):
            var, value = line.split(" is ")
            self.variables[var.strip()] = value.strip().strip('"')
        elif line.startswith("if ") and " then" in line:
            condition = line[3:line.index(" then")].strip()
            return ("if", condition)
        elif line.strip() == "otherwise then":
            return ("else", None)
        elif line.strip() == "thats all":
            return ("end_block", None)
        elif line.startswith("can you say"):
            match = re.match(r'can you say "(.*)"\?', line)
            if match:
                message = match.group(1)
                return ("print", message)
            match = re.match(r'can you say ([a-zA-Z_]\w*)\?', line)
            if match:
                var = match.group(1)
                return ("print_var", var)
        return None

    def evaluate_condition(self, condition):
        if " is " in condition:
            var, value = condition.split(" is ")
            var = var.strip()
            value = value.strip().strip('"')
            if var in self.variables:
                if isinstance(self.variables[var], int):
                    return self.variables[var] == int(value)
                elif isinstance(self.variables[var], str):
                    return self.variables[var] == value
        return False

    def run(self, code):
        lines = code.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            parsed_line = self.parse_line(line)
            if parsed_line:
                cmd, arg = parsed_line
                if cmd == "if":
                    self.if_exec = False
                    condition = arg
                    if self.evaluate_condition(condition):
                        self.if_exec = True
                        i += 1
                        while i < len(lines) and lines[i].strip() != "thats all":
                            if lines[i].strip() == "otherwise then":
                                while i < len(lines) and lines[i].strip() != "thats all":
                                    i += 1
                                break
                            self.run_line(lines[i])
                            i += 1
                    else:
                        while i < len(lines) and lines[i].strip() != "otherwise then":
                            i += 1
                        if i < len(lines) and lines[i].strip() == "otherwise then":
                            i += 1
                            while i < len(lines) and lines[i].strip() != "thats all":
                                self.run_line(lines[i])
                                i += 1
                elif cmd == "else":
                    if not self.if_exec:
                        i += 1
                        while i < len(lines) and lines[i].strip() != "thats all":
                            self.run_line(lines[i])
                            i += 1
                    else:
                        while i < len(lines) and lines[i].strip() != "thats all":
                            i += 1
                elif cmd == "print":
                    print(arg)
                elif cmd == "print_var":
                    if arg in self.variables:
                        print(self.variables[arg])
            i += 1

    def run_line(self, line):
        parsed_line = self.parse_line(line)
        if parsed_line:
            cmd, arg = parsed_line
            if cmd == "print":
                print(arg)
            elif cmd == "print_var":
                if arg in self.variables:
                    print(self.variables[arg])

def main():
    parser = argparse.ArgumentParser(description='Run CodeVersation (CV) code.')
    parser.add_argument('filename', type=str, help='The filename of the CV code to run')
    args = parser.parse_args()

    with open(args.filename, 'r') as file:
        code = file.read()

    interpreter = CVInterpreter()
    interpreter.run(code)

if __name__ == "__main__":
    main()
 
