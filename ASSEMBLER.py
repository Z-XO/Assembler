
import re
symbols = dict()
counter = 0


with open('Program_1.txt', 'r') as fr:
    with open('first_pass.txt', 'w') as fw:
        for index, line in enumerate(fr):
            for line in fr:
                lineClean = line.split("//")
                if len(lineClean) > 1:
                    lineClean += "\n"
                if lineClean[0].rstrip():
                    # print(lineClean[0],end='')
                    
                    # First pass to handle the branches
                    m = re.search('^([A-Za-z_][A-Za-z_0-9]*):', lineClean[0])
                    if m is not None:
                        symbols[m.group(1)] = counter
                    else:
                        counter = counter + 1
                    #print(lineClean[0], end ='')
                    fw.write(lineClean[0])

for k in symbols.keys():
    print("%3d %s"%(symbols[k], k))
    
            # If trying to remove spaces add lineClean[0] = lineClean[0].replace(" ", "")
with open ('first_pass.txt', 'r') as fr:
    with open ('machine_code.txt', 'w') as fw:
        counter = 0
        offset = ""
        for line in fr:
            op_code = ""
            str_array = line.split()
            m = re.search('^([A-Za-z_][A-Za-z_0-9]*):', str_array[0])
            if m is not None:
                continue
        
            instruction = str_array[0]
           
           # print(register)

            # (00001) AND X: bitwise regX AND regI is stored into regA         
            if instruction == "AND":
                op_code = "00000"

            # R0 = R0 XOR R
            elif instruction == "XOR":
                op_code = "00001"
            
            # R0 = R0 OR RX
            elif instruction == "LOR":
                op_code = "00010"
            
            # R0 = R0 + RX
            elif instruction == "ADD":
                op_code = "00011"
            
            # R0 = R0 - RX 
            elif instruction == "SUB":
                op_code = "00100"
            
            # RX $<<$ 1
            elif instruction == "LSL":
                op_code = "00101"
            
            # RX $>>$ 1
            elif instruction == "LSR":
                op_code = "00110"
            
            # SKIP iff RX == 0
            elif instruction == "SKEQ":
                op_code = "00111"

            # SKIP iff RX $<$ 0
            elif instruction == "SKLT":
                op_code = "01000"

            # R0 = RX
            elif instruction == "LDR0":
                op_code = "01001"

            # RX = R0
            elif instruction == "STR0":
                op_code = "01010"

            # R0 = mem[RX]
            elif instruction == "LDR":
                op_code = "01011"

            # mem[RX] = R0
            elif instruction == "STR":
                op_code = "01100"
            
            #  Loads front/(back if needed) half-byte immediate
            elif instruction == "MV":
                op_code = "01101"
            
            # RX ++
            elif instruction == "INC":
                op_code = "01111"

            # BRANCH
            elif instruction == "B":
                label = str_array[1]
                if label in symbols.keys():
                    dest = symbols[label]
                    next = counter + 1
                    offset = '{0:08b}'.format(int(dest - next - 1) & 255)
                else:
                    print("label is undefined")
                    print(label)


      
            else:
                print("Not a legal op_code")


            
            register = str_array[1]
            reg_code = ""
            halfwordFlag = False

            if (register == "R0"):
                reg_code = "0000"
            
            elif (register == "R1"):
                reg_code = "0001"
            
            elif (register == "R2"):
                reg_code = "0011"

            elif (register == "R3"):
                reg_code = "0100"
            
            elif (register == "R4"):
                reg_code = "0101"

            elif (register== "R5"):
                reg_code = "0110"

            elif (register == "R6"):
                reg_code = "0111"

            elif (register == "R7"):
                reg_code = "1000"

            elif (register == "R8"):
                reg_code = "1001"

            elif (register == "R9"):
                reg_code = "1010"

            elif (register == "R10"):
                reg_code = "1011"
            
            elif (register == "R11"):
                reg_code = "1100"

            elif (register == "R12"):
                reg_code = "1101"

            elif (register == "R13"):
                reg_code = "1110"

            elif (register == "R14"):
                reg_code = "1111"

            elif (register.startswith('#')):
               immediate = str_array[1] 
               immediate = immediate[1:]
               binaryImmediate = '{0:08b}'.format(int(immediate))
               reg_code = binaryImmediate
               firstHalf = reg_code[:4]
               secondHalf = reg_code[4:]
               reg_code = secondHalf
               if '1' in str(firstHalf):
                   halfwordFlag = True
            
            else:
                pass    
            
            full_op = op_code + "_" + reg_code
            
            if(halfwordFlag == True):
                first_op = "01101" + "_" + firstHalf
                second_op = "01110" + "_" + secondHalf
                fw.write(first_op)
                #fw.write("%3d: %s\n" % (counter,first_op))
                fw.write('\n')
                fw.write(second_op)
                #fw.write("%3d: %s\n" % (counter,second_op))
                fw.write('\n')
                halfwordFlag = False
            elif instruction == "B":
                #fw.write("%3d: %s\n" % (counter,"1_" + offset))
                fw.write("1_" + offset)
                fw.write('\n')
            else:
                #fw.write("%3d: %s\n" % (counter,full_op))
                fw.write(full_op)
                fw.write('\n')
            counter = counter + 1
            
            

            