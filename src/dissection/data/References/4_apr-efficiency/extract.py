import json
import re

if __name__ == "__main__":
    with open('./rules.md', 'r') as file:
        content = file.read()

    number_of_rules = 16

    rules = ["R" + str(index) for index in range(number_of_rules)]
    parts = re.split(str(rules).replace("', '", "|")[2:-2], content)

    results = []

    for index in range(number_of_rules):
        tool_lines = parts[index+1].split(">")

        for tool_line in tool_lines:
            tool = re.findall(r'\*\*.*?:\*\*', tool_line)
            
            if tool:
                t = tool[0].replace("**", "").replace(":", "")

                bugs = re.findall(r'\[.*?\]', tool_line)

                for bug in bugs:
                    b = bug.replace("-", "_").replace("[", "").replace("]", "")

                    if t == "RSRepair":
                        t = "RSRepair-A"

                    if t == "GenProg":
                        t = "GenProg-A"

                    if t == "KaliA":
                        t = "Kali-A"

                    results.append((rules[index], t, b))
