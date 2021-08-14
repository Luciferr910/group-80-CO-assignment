import traceback

class asm:
    op = {
        'add' : '00000',
        'sub' : '00001',
        'movi' : '00010',
        'mov' : '00011',
        'ld'  : '00100',
        'st'  : '00101',
        'mul' : '00110',
        'div' : '00111',
        'rs'  : '01000',
        'ls'  : '01001',
        'xor' : '01010',
        'or'  : '01100',
        'not' : '01101',
        'cmp' : '01110',
        'jmp' : '01111',
        'jlt' : '10000',
        'jgt' : '10001',
        'je'  : '10010',
        'hlt' : '1001100000000000',
    }

    reg = {
        'R0' : '000', 
        'R1' : '001',
        'R2' : '010',
        'R3' : '011',
        'R4' : '100',
        'R5' : '101',
        'R6' : '110',
        'FLAGS' : '111',
    }

    var = {}
    lab = {}
    ck_flag = False
    code = []
    ans = []
    mem = 1
    ll = 1

    def __init__(self):
        pass

    def binary_16(self, n):
        n = int(n)
        se = ''

        while n > 0:
            se += str(n % 2)
            n //= 2

        while (len(se) < 16):
            se += '0'

        return se[::-1]


    def binary_8(self, n):
        n = int(n)
        se = ''

        while n > 0:
            se += str(n % 2)
            n //= 2

        while (len(se) < 8):
            se += '0'

        return se[::-1]


    def binary_5(self, n):
        n = int(n)
        se = ''

        while n > 0:
            se += str(n % 2)
            n //= 2

        while (len(se) < 5):
            se += '0'

        return se[::-1]


    def input(self):
        while(1):
            l = input()

            if (l == ''):
                break

            self.code.append(l)

    def conv_pass1(self):
        for i in self.code:
            if i == '':
                continue

            l = i.split(' ')

            if (l[0] == 'var'):
                self.var[l[1]] = self.binary_8(self.mem)
                self.mem += 1

                continue

            if 'label' in l[0]:
                x = l[0][5:]
                x = x[-1]
                self.lab[l[0][:len(l[0]) - 1]] = self.binary_8(self.ll)
                self.ll += 1

    def conv_pass2(self):
        for i in self.code:
            if i == '':
                continue
            
            l = i.split(' ')

            if 'label' in l[0]:
                l = l[1:]

            if (len(l) == 1):
                aa = self.op[l[0]]
                self.ans.append(aa)

                return
            
            if '$' in i:
                l[0] += 'i'

            if (l[0] == 'var'):
                continue

            aa = ''
            aa += self.op[l[0]]

            if (len(l) == 4):
                aa += '00'

            elif 'R' in l[1] and ('R' in l[2] or 'F' in l[2]):
                aa += '00000'
            
            if 'label' in l[1]:
                aa += '0'
                aa += self.lab[l[1]]
                aa += '11'
                self.ans.append(aa)

                continue

            aa += self.reg[l[1]]

            if (len(l) == 2):
                self.ans.append(aa)

                continue

            if '$' in l[2]:
                x = l[2][1:]
                x = int(x)
                aa += self.binary_8(x)

            elif 'R' in l[2] or 'F' in l[2]:
                aa += self.reg[l[2]]

            else:
                aa += self.var[l[2]]

            if (len(l) == 3):
                self.ans.append(aa)
                
                continue

            aa += self.reg[l[3]]

            self.ans.append(aa)

    def print_sol(self):
        for x in self.ans:
            print(x)

    def fg(self):
        if "hlt" in self.code[len(self.code) - 2]: #second last hlt
            if len(self.code[len(self.code) - 1]) > 0: #last line anything
                print('General Syntax Error')
                return 0

        return 1
                

def main():
    a = asm()
    a.input()

    if(a.fg()):
        try:
            a.conv_pass1()
            a.conv_pass2()
        except:
            # traceback.print_exception()
            print('General Syntax Error')
            exit()

        a.print_sol()


if __name__ == '__main__':
    main()
