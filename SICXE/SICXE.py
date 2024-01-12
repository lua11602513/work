# 導入必要的模塊
import json
import math

# 寄存器的編號和十六進制字典
num_of_register = {'A': 0, 'X': 1, 'L': 2, 'B': 3, 'S': 4, 'T': 5, 'F': 6, 'PC': 8, 'SW': 9}
HexDict = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7',
           8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}
DecDict = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
           '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}

# 二進制轉十六進制函數
def Bin2Hex(Bin):
    Hex = ''
    if (len(Bin) > 4):
        fill = (4 - (len(Bin) % 4))
        if (fill == 4):
            fill = (fill - 4)
        Bin = ('0'*fill + Bin)
        for i in range(0, len(Bin), 4):
            Hex += Bin2Hex(Bin[i:(i*4+4)])
    else:
        Dec = 0
        for i, digit in enumerate(Bin):
            Dec += (int(digit) * math.pow(2, (3-i)))
        Hex = Dec2Hex(Dec)
    return Hex

# 十進制轉十六進制函數
def Dec2Hex(Dec: int):
    Hex = ''
    while (Dec >= 16):
        Hex = (HexDict[Dec % 16] + Hex)
        Dec //= 16
    Hex = (HexDict[Dec] + Hex)
    return Hex

# 十六進制轉十進制函數
def Hex2Dec(Hex: str):
    Dec = 0
    times = 0
    while (len(Hex) > 0):
        Dec += int(DecDict[Hex[-1]] * math.pow(16, times))
        Hex = Hex[:-1]
        times += 1
    return Dec

# 處理BYTE指令的函數
def BYTE(parms):
    mode = parms[0]
    data = parms[2:-1]
    objCode = ''
    if (mode == 'C'):
        for i in data:
            objCode += (Dec2Hex(ord(i))).zfill(2)
    elif (mode == 'X'):
        objCode += data
    else:
        print('BYTE Error')
    location_add = (len(objCode)//2)
    return location_add, objCode

# 處理WORD指令的函數
def WORD(parms):
    if (int(parms) >= 0):
        objCode = Dec2Hex(int(parms)).zfill(6)
    else:
        full_hex = Hex2Dec('1000000')
        objCode = Dec2Hex(full_hex + int(parms)).zfill(6)
    location_add = (len(objCode)//2)
    return location_add, objCode

# 處理RESB指令的函數
def RESB(parms):
    objCode = ' '
    location_add = int(parms)
    return location_add, objCode

# 處理RESW指令的函數
def RESW(parms):
    objCode = ' '
    location_add = (int(parms) * 3)
    return location_add, objCode

# 寄存器類別
class Register():
    A = False
    X = False
    L = False
    B = False
    S = False
    T = False
    F = False
    PC = False
    SW = False

    # 載入寄存器
    def Load(self, instrucet, parms):
        if (instrucet == 'LDA'):
            self.A = parms
        elif (instrucet == 'LDX'):
            self.X = parms
        elif (instrucet == 'LDL'):
            self.L = parms
        elif (instrucet == 'LDB'):
            self.B = parms
        elif (instrucet == 'LDS'):
            self.S = parms
        elif (instrucet == 'LDT'):
            self.T = parms
        elif (instrucet == 'LDF'):
            self.F = parms

    # 清除寄存器
    def Clear(self, parms):
        if (parms == 'A'):
            self.A = 0
        elif (parms == 'X'):
            self.X = 0
        elif (parms == 'L'):
            self.L = 0
        elif (parms == 'B'):
            self.B = 0
        elif (parms == 'S'):
            self.S = 0
        elif (parms == 'T'):
            self.T = 0
        elif (parms == 'F'):
            self.F = 0
        elif (parms == 'PC'):
            self.PC = 0
        elif (parms == 'SW'):
            self.SW = 0

    # 寄存器位置的計算
    def Location_of_rigster(self):
        if self.A:
            self.A = self.Parms_computing(self.A)
        elif self.X:
            self.X = self.Parms_computing(self.X)
        elif self.L:
            self.L = self.Parms_computing(self.L)
        elif self.B:
            self.B = self.Parms_computing(self.B)
        elif self.S:
            self.S = self.Parms_computing(self.S)
        elif self.T:
            self.T = self.Parms_computing(self.T)
        elif self.F:
            self.F = self.Parms_computing(self.F)

    # 操作數計算
    def Parms_computing(self, parms):
        if (parms[0] == '#'):
            parms = parms[1:]
            return function_[parms]

# 初始化寄存器
register = Register()

# 打開包含組合語言代碼的文件
f = open('./Input.txt', 'r')
Input = f.readlines()
f.close()

# 讀取SIC/XE指令集信息的JSON文件
with open('./instrucetion_SICXE.json', 'r', encoding='utf-8') as j:
    instrucetion = json.load(j)

# 初始化操作數字典
function_ = {}

# 處理第一行的指令
temp = Input[0].replace('\n', '').split(' ')
if (len(temp) == 3):
    information = [[5, temp[2].zfill(4), temp[0], temp[1], temp[2], ' ']]
    function_[temp[0]] = Hex2Dec(information[0][4])
else:
    information = [[5, temp[2].zfill(4), '', temp[0], temp[1], ' ']]

# 初始化行號和位置
line = 10
location = Hex2Dec(information[0][4])

# 處理剩餘的指令
for i in Input[1:]:
    line += 5

    # 處理註解
    if (i[0] == '.'):
        information.append([line, '', '.', i.replace(
            '.', '').replace('\n', ''), '', ' '])
        continue

    # 分割指令
    i = i.replace('\n', '').split(' ')

    # 根據指令的不同，處理不同的情況
    if (len(i) == 1):
        information.append(
            [line, Dec2Hex(location).zfill(4), '', i[0], '', ''])
    elif (len(i) == 2):
        information.append(
            [line, Dec2Hex(location).zfill(4), '', i[0], i[1], ''])
    elif (len(i) == 3):
        information.append(
            [line, Dec2Hex(location).zfill(4), i[0], i[1], i[2], ''])

        function_[i[0]] = Dec2Hex(location).zfill(4)

    # 計算下一個指令的位置
    if (information[-1][3][0] == '+'):
        location += 4
    elif (information[-1][3] not in instrucetion['pseudo']):
        location += int(instrucetion['instrucetion'][information[-1][3]][1])

        # 清除CLEAR指令
        if (information[-1][3] == 'CLEAR'):
            register.Clear(information[-1][4])
    else:
        # 處理偽指令
        if (information[-1][3] == 'BYTE'):
            location_add, objectCode = BYTE(information[-1][4])
        elif (information[-1][3] == 'RESB'):
            location_add, objectCode = RESB(information[-1][4])
        elif (information[-1][3] == 'RESW'):
            location_add, objectCode = RESW(information[-1][4])
        elif (information[-1][3] == 'WORD'):
            location_add, objectCode = WORD(information[-1][4])
        elif (information[-1][3] == 'BASE'):
            # 處理BASE指令
            register.Load(information[-2][3], information[-2][4])
            information[-1][1] = ''
            information[-1][5] = ' '
            continue
        elif (information[-1][3] == 'END'):
            # 處理END指令
            information[-1][1] = ''
            objectCode = ' '

        # 更新位置和指令碼
        location += location_add
        information[-1][-1] = objectCode

# 計算寄存器位置
register.Location_of_rigster()
# 迴圈處理指令列表中的每一個元素
for now_index, infor in enumerate(information):
    # 複製元素
    infor = infor.copy()
    next_index = now_index
    
    # 如果該指令還未生成目標碼
    if infor[5] == '':
        # 判斷指令的格式，根據不同格式生成目標碼
        if (instrucetion["instrucetion"][infor[3].replace('+', '')][1] == '2'):
            # 處理2位元指令
            infor[4] = infor[4].split(',')
            if (len(infor[4]) == 2):
                information[now_index][5] = f'{instrucetion["instrucetion"][infor[3]][0]}{num_of_register[infor[4][0]]}{num_of_register[infor[4][1]]}'
            else:
                information[now_index][5] = f'{instrucetion["instrucetion"][infor[3]][0]}{num_of_register[infor[4][0]]}0'

        elif (instrucetion["instrucetion"][infor[3].replace('+', '')][1] == '3'):
            # 處理3位元指令
            if (infor[3] == 'RSUB'):
                information[now_index][5] = '4F0000'
                continue

            # 找到下一個非註解行的指令
            next_index += 1
            while information[next_index][1] == '':
                next_index += 1

            # 設定PC寄存器
            register.PC = information[next_index][1]

            # 判斷地址運算符的類型
            if (infor[4][0] == '@'):
                infor[4] = infor[4][1:]
                n, i = 1, 0
            elif (infor[4][0] == '#'):
                infor[4] = infor[4][1:]
                n, i = 0, 1
            else:
                n, i = 1, 1

            # 判斷是否有索引
            if ',X' in infor[4]:
                infor[4] = infor[4].replace(',X', '')
                x = 1
            else:
                x = 0

            # 判斷是否為擴展格式指令
            if (infor[3][0] == '+'):
                infor[3] = infor[3][1:]
                e = 1
            else:
                e = 0

            # 取得指令的opcode
            opcode = f'{instrucetion["instrucetion"][infor[3]][0]}0'

            # 初始化B、P、E的值
            b, p = 0, 0

            # 判斷是擴展格式指令還是基本格式指令
            if e:
                # 計算地址
                if (not n and i and (infor[4].isdigit())):
                    address = Dec2Hex(int(infor[4])).zfill(5)
                else:
                    address = function_[infor[4]].zfill(5)

                # 生成目標碼
                information[now_index][5] = f'{Dec2Hex(Hex2Dec(opcode) + Hex2Dec(Bin2Hex(f"{n}{i}{x}{b}{p}{e}"))).zfill(3)}{address}'

            else:
                # 計算相對位移
                if (not n and i and (infor[4].isdigit())):
                    disp = Dec2Hex(int(infor[4])).zfill(3)
                else:
                    disp = (
                        Hex2Dec(function_[infor[4]]) - Hex2Dec(register.PC))

                    if x:
                        disp -= register.X

                    if ((disp >= 4096) or ((disp <= -4096))):
                        b, p = 1, 0
                        disp = (
                            Hex2Dec(function_[infor[4]]) - Hex2Dec(register.B))

                        if x:
                            disp -= register.X
                    else:
                        b, p = 0, 1

                    if (disp < 0):
                        disp = Dec2Hex(disp + Hex2Dec('1000')).zfill(3)
                    else:
                        disp = Dec2Hex(disp).zfill(3)

                information[now_index][5] = f'{Dec2Hex(Hex2Dec(opcode) + Hex2Dec(Bin2Hex(f"{n}{i}{x}{b}{p}{e}"))).zfill(3)}{disp[-3:]}'

# 輸出結果
print(" %-10s %-10s %-10s %-10s %-10s %-17s" %
      ('Line', 'Location', '', 'Original', '', 'Object code'))
for i in information:
    if (i[2] == '.'):
        print(" %-10s %-10s %-10s %-39s" % (i[0], i[1], i[2], i[3]))
    else:
        print(" %-10s %-10s %-10s %-10s %-10s %-17s" %
              (i[0], i[1], i[2], i[3], i[4], i[5]))
