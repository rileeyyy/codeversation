import re
import argparse

class CVInterpreter:
    def __init__(self):
        self.variables = {}

    def parse_line(self, line):
        line = line.strip()
        if re.match(r"^[a-zA-Z_]\w* is \d+$", line):
            var, value = line.split(" is ")
            self.variables[var.strip()] = int(value.strip())
        elif line.startswith("if ") and " then" in line:
            condition = line[3:line.index(" then")].strip()
            return ("if", condition)
        elif line.strip() == "thats all":
            return ("end_if", None)
        elif line.strip() == "otherwise then":
            return ("else", None)
        elif line.startswith("but if ") and " then" in line:
            condition = line[7:line.index(" then")].strip()
            return ("elif", condition)
        elif line.startswith("can you say"):
            match = re.match(r'can you say "(.*)"\?', line)
            if match:
                message = match.group(1)
                return ("print", message)
        return None

    def evaluate_condition(self, condition):
        match = re.match(r"([a-zA-Z_]\w*) is (\d+)", condition)
        if match:
            var = match.group(1)
            value = int(match.group(2))
            return self.variables.get(var) == value
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
                    condition = arg
                    if self.evaluate_condition(condition):
                        i += 1
                        while i < len(lines) and lines[i].strip() not in ["thats all", "otherwise then", "but if"]:
                            self.run_line(lines[i])
                            i += 1
                        while i < len(lines) and lines[i].strip() != "thats all":
                            i += 1
                    else:
                        i += 1
                        while i < len(lines):
                            line = lines[i].strip()
                            if line.startswith("but if"):
                                condition = line[7:line.index(" then")].strip()
                                if self.evaluate_condition(condition):
                                    i += 1
                                    while i < len(lines) and lines[i].strip() not in ["thats all", "otherwise then", "but if"]:
                                        self.run_line(lines[i])
                                        i += 1
                                    break
                                else:
                                    i += 1
                            elif line == "otherwise then":
                                i += 1
                                while i < len(lines) and lines[i].strip() != "thats all":
                                    self.run_line(lines[i])
                                    i += 1
                                break
                            elif line == "thats all":
                                break
                            else:
                                i += 1
                elif cmd == "end_if":
                    pass
                elif cmd == "print":
                    print(arg)
            i += 1

    def run_line(self, line):
        parsed_line = self.parse_line(line)
        if parsed_line:
            cmd, arg = parsed_line
            if cmd == "print":
                print(arg)
            elif cmd == "if":
                condition = arg
                if self.evaluate_condition(condition):
                    return True
            elif cmd == "end_if":
                return False
        return None

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
