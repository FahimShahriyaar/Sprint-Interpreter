# Programming Language: Sprint
# Creator: Fahim Shahriyar

import parser
import interpreter
import sys

if __name__ == "__main__":

    if len(sys.argv) == 2:
        if sys.argv[1]=='--version':
            print('1.0.0')
        else:
            try:
                if sys.argv[1][-4:]!='.spr':
                    raise Exception('Error: sprint file missing')
                with open(sys.argv[1]) as file:
                    data = file.read()
                    if data=='': raise SystemExit

                    prog = parser.parse(data)
                    if prog is None: raise SystemExit
                    
                    b = interpreter.Interpret(prog)
                    b.run()
            except Exception as e:
                print(e)
            
    elif len(sys.argv)==1:
        print('Welcome To Sprint Language')