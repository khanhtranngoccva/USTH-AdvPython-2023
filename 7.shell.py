import os
import re
import subprocess
import bashlex


def execute(command: str):
    nodes = re.split(r'([<>|])', command)
    if len(nodes) == 1:
        subprocess.run(nodes[0])
    elif len(nodes) == 3:
        p1, token, p2 = [node.strip(" ") for node in nodes]
        print(p1, token, p2)
        if token == ">":
            with open(p2, "w") as file:
                subprocess.Popen(p1, stdout=file).wait()
        if token == "<":
            with open(p2, "r") as file:
                subprocess.Popen(p1, stdin=file).wait()
        if token == "|":
            proc1 = subprocess.Popen(p1, stdout=subprocess.PIPE)
            proc2 = subprocess.Popen(p2, stdin=proc1.stdout)
            proc1.wait()
            proc2.wait()


while True:
    print(os.getcwd(), "$", end=" ")
    cmd = input()
    execute(cmd)
