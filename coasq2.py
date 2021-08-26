import matplotlib.pyplot as plt

class cpu():
    PC = '00000000'

    TIME = 0

    acc_t = []
    
    MEM = ['0000000000000000' for _ in range(256)]
    ACC_TIM = [0 for _ in range(256)]

    R = ['0000000000000000' for _ in range(8)]
    # R[7] is the flag register
    # FLAGS = '0000000000000000'

    HLT_FL = False

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
        'hlt' : '10011',
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

    
    def numb(self, str):
        ans = 0
        po2 = 1
        for i in range(len(str) - 1, -1, -1):
            if str[i] == '1':
                ans += po2

            po2 *= 2

        return ans

    def sum_bit(self, a, b):
        max_len = 16
        a = a.zfill(max_len)
        b = b.zfill(max_len)
        res = ''
        carry = 0
        for i in range(max_len - 1, -1, -1):
            r = carry
        
            r += 1 if a[i] == '1' else 0
            r += 1 if b[i] == '1' else 0
        
            res = ('1' if r % 2 == 1 else '0') + res
        
            carry = 0 if r < 2 else 1

        return res, str(carry)

    def XOR(self, a, b, n = 16):
        ans = ""
        for i in range(n):
            if (a[i] == b[i]):
                ans += "0"
            else:
                ans += "1"
        return ans

    def OR(self, a, b, n = 16):
        ans = ""
        for i in range(n):
            if (a[i] == '1' or b[i] == '1'):
                ans += "0"
            else:
                ans += "1"
        return ans

    def AND(self, a, b, n = 16):
        ans = ""
        for i in range(n):
            if (a[i] == '1' and b[i] == '1'):
                ans += "0"
            else:
                ans += "1"
        return ans

    def INV(self, a, n = 16):
        ans = ""
        for i in range(n):
            if (a[i] == '1'):
                ans += "0"
            else:
                ans += "1"
        return ans

    def exc(self, str):
        opcode = str[:5]
        pc_n = self.numb(self.PC)

        print(opcode)

        if opcode == '00000':
            #ADDITION
            reg1 = self.numb(str[7:10])
            reg2 = self.numb(str[10:13])
            reg3 = self.numb(str[13:])
            
            self.R[reg1], carry = self.sum_bit(self.R[reg2], self.R[reg3])

            if carry:
                self.R[7] = self.R[7][:12] + '1' + self.R[7][13:]

        elif opcode == '00001':
            #SUBTRACTION
            reg1 = self.numb(str[7:10])
            reg2 = self.numb(str[10:13])
            reg3 = self.numb(str[13:])

            r2 = self.numb(self.R[reg2])
            r3 = self.numb(self.R[reg3])

            an = r2 - r3

            borrow = 0

            if (an < 0):
                borrow = 1
                an += 65536

            self.R[reg1] = self.binary_16(an)

            if borrow:
                self.R[7] = self.R[7][:12] + '1' + self.R[7][13:]

        elif opcode == '00010':
            # MOVI
            reg = self.numb(str[5:8])
            val = str[8:]

            self.R[reg] = val

        elif opcode == '00011':
            # MOV
            reg1 = self.numb(str[10:13])
            reg2 = self.numb(str[13:])

            self.R[reg1] = self.R[reg2]

        elif opcode == '00100':
            # LOAD
            reg = self.numb(str[5:8])
            addr = self.numb(str[8:])

            self.R[reg] = self.MEM[addr]

            self.acc_t.append([self.TIME, addr])

        elif opcode == '00101':
            # STORE
            reg = self.numb(str[5:8])
            addr = self.numb(str[8:])

            self.MEM[addr] = self.R[reg]

            self.acc_t.append([self.TIME, addr])

        elif opcode == '00110':
            # MULTIPLY
            reg1 = self.numb(str[7:10])
            reg2 = self.numb(str[10:13])
            reg3 = self.numb(str[13:])

            r2 = self.numb(self.R[reg2])
            r3 = self.numb(self.R[reg3])

            an = r2 * r3
            carry = 0

            if an >= 65536:
                an %= 65536
                carry = 1

            self.R[reg1] = self.binary_16(an)
            
            if carry:
                self.R[7] = self.R[7][:12] + '1' + self.R[7][13:]

        elif opcode == '00111':
            # DIVIDE
            reg1 = self.numb(str[10:13])
            reg2 = self.numb(str[13:])

            r1 = self.numb(self.R[reg1])
            r2 = self.numb(self.R[reg2])

            qu = r1 // r2
            rem = r1 % r2

            self.R[0] = qu
            self.R[1] = rem

        elif opcode == '01000':
            #RIGHT SHIFT
            reg = self.numb(str[5:8])
            val = self.numb(str[8:])

            r1 = self.R[reg][len(self.R[reg]) - val:]
            r2 = self.R[reg][0:len(self.R[reg]) - val]

            self.R[reg] = r1 + r2

        elif opcode == '01001':
            #LEFT SHIFT
            reg = self.numb(str[5:8])
            val = self.numb(str[8:])

            l1 = self.R[reg][val:]
            l2 = self.R[reg][0:val]

            self.R[reg] = l1 + l2

        elif opcode == '01010':
            #XOR
            reg1 = self.numb(str[7:10])
            reg2 = self.numb(str[10:13])
            reg3 = self.numb(str[13:])
            
            self.R[reg1] = self.XOR(self.R[reg2], self.R[reg3])

        elif opcode == '01011':
            #OR
            reg1 = self.numb(str[7:10])
            reg2 = self.numb(str[10:13])
            reg3 = self.numb(str[13:])
            
            self.R[reg1] = self.OR(self.R[reg2], self.R[reg3])

        elif opcode == '01100':
            #AND
            reg1 = self.numb(str[7:10])
            reg2 = self.numb(str[10:13])
            reg3 = self.numb(str[13:])
            
            self.R[reg1] = self.AND(self.R[reg2], self.R[reg3])

        elif opcode == '01101':
            #INVERSE
            reg1 = self.numb(str[10:13])
            reg2 = self.numb(str[13:])
            
            self.R[reg1] = self.INV(self.R[reg2])

        elif opcode == '01110':
            #CMP
            reg1 = self.numb(str[10:13])
            reg2 = self.numb(str[13:])

            r1 = self.numb(self.R[reg1])
            r2 = self.numb(self.R[reg2])

            if r1 == r2:
                # set carry
                self.R[7] = self.R[7][:15] + '1'
                
            elif r1 > r2:
                # set carry
                self.R[7] = self.R[7][:13] + '1' + self.R[7][14:]
                
            else:
                # set carry
                self.R[7] = self.R[7][:14] + '1' + self.R[7][15:]

        elif opcode == '01111':
            #UNCOND JUMP
            val = str[8:]

            self.acc_t.append([self.TIME, val])

            return False, val

        elif opcode == '10000':
            #LESS THAN FLAG JUMP
            val = str[8:]

            if (self.R[7][13] == '1'):
                self.acc_t.append([self.TIME, val])
                return False, val

        elif opcode == '10001':
            #GREATER THAN FLAG JUMP
            val = str[8:]

            if (self.R[7][14] == '1'):
                self.acc_t.append([self.TIME, val])
                return False, val
        
        elif opcode == '10010':
            #EQUAL TO FLAG JUMP
            val = str[8:]

            if (self.R[7][15] == '1'):
                self.acc_t.append([self.TIME, val])
                return False, val

        elif opcode == '10011':
            return True, '00000000'

        else:
            print("!!!!!!!!!ERROR!!!!!!!!!")
            return True, '00000000'

        pc_n += 1
        
        return False, self.binary_8(pc_n)

    
    def run(self):
        i = 0
        while True:
            inp = input()

            if (len(inp) == 0):
                break

            self.MEM[i] = inp
            i += 1

        print('Input Done')

        while (not self.HLT_FL):
            pc_n = self.numb(self.PC)
            cmd = self.MEM[pc_n]

            self.HLT_FL, NEW_PC = self.exc(cmd)

            ot = self.PC

            for i in range(8):
                ot += ' ' + self.R[i]

            print(ot)
            
            self.PC = NEW_PC

            self.TIME += 1

        print('')

        for x in self.MEM:
            print(x)

        # plot
        # print(self.acc_t)

        if len(self.acc_t) == 0:
            x , y = -1 , -1
        
        else:
            x, y = zip(*self.acc_t)

        plt.scatter(x, y)
        plt.show()



def main():
    a = cpu()
    a.run()


if __name__ == '__main__':
    main()       