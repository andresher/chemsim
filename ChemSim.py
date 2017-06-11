from ChemSimYacc import parser
import sys

def execute_lines(lines):
    for line in lines:
        if line == 'quit': break
        if not line: continue
        result = parser.parse(line)


def main():
    isFromFile = False
    while True:
        try:
            if len(sys.argv) > 1:
                isFromFile = True
                files = sys.argv[1:len(sys.argv)]
                for f in files:
                    print("Starting to read file " + f )
                    file = open(f, "r")
                    lines = file.readlines()
                    execute_lines(lines)
                break
            elif len(sys.argv) == 1:
                s = input('ChemSim > ')



        except EOFError:
            break

        if s == 'quit': break
        if not s: continue
        result = parser.parse(s)

if __name__ == '__main__':
    main()