from ChemSimYacc import parser

def main():
    while True:
        try:
            s = input('ChemSim > ')
        except EOFError:
            break
        if s == 'quit': break
        if not s: continue
        result = parser.parse(s)

if __name__ == '__main__':
    main()