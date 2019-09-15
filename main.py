MOV = 0
ADD = 1
SUB = 2
AND = 3
OR = 4
SL = 5
SR = 6
SRA = 7
LDL = 8
LDH = 9
CMP = 10
JE = 11
JMP = 12
LD = 13
ST = 14
HLT = 15
REG0 = 0
REG1 = 1
REG2 = 2
REG3 = 3
REG4 = 4
REG5 = 5
REG6 = 6
REG7 = 7

reg = [0] * 8
rom = [0] * 256
ram = [0] * 256


def pce_main():
    pc = 0
    frag_eq = 0

    count = 1

    asm_read_file()
    print("|{}{}{}|".format("-" * 87, "reg status", "-" * 87))
    while True:
        ir = rom[pc]
        print("count : {:5}   program_counter {:5}   ir : {:4x}   "
              "reg[0] : {:5}   reg[1] : {:5}   reg[2] : {:5}   reg[3] : {:5}  "
              " reg[4] : {:5}   reg[5] : {:5}   reg[6] : {:5}   reg[7] : {:5}"
              .format(count, pc, ir, reg[0], reg[1], reg[2], reg[3],
                      reg[4], reg[5], reg[6], reg[7]))
        count += 1
        pc += 1
        op_code = pce_op_code(ir)
        if op_code == MOV:
            reg[pce_op_regA(ir)] = reg[pce_op_regB(ir)]

        elif op_code == ADD:
            reg[pce_op_regA(ir)] += reg[pce_op_regB(ir)]

        elif op_code == SUB:
            reg[pce_op_regA(ir)] -= reg[pce_op_regB(ir)]

        elif op_code == AND:
            reg[pce_op_regA(ir)] &= reg[pce_op_regB(ir)]

        elif op_code == OR:
            reg[pce_op_regA(ir)] |= reg[pce_op_regB(ir)]

        elif op_code == SL:
            reg[pce_op_regA(ir)] = reg[pce_op_regA(ir)] << 1

        elif op_code == SR:
            reg[pce_op_regA(ir)] = reg[pce_op_regA(ir)] >> 1

        elif op_code == SRA:
            reg[pce_op_regA(ir)] = (reg[pce_op_regA(ir)] & 0x8000) | \
                                   (reg[pce_op_regA(ir)] >> 1)

        elif op_code == LDL:
            reg[pce_op_regA(ir)] = (reg[pce_op_regA(ir)] & 0xff00) | \
                                   (pce_op_data(ir) & 0x00ff)

        elif op_code == LDH:
            reg[pce_op_regA(ir)] = (pce_op_data(ir) << 8) | \
                                   (reg[pce_op_regA(ir)] & 0x00ff)

        elif op_code == CMP:
            if reg[pce_op_regA(ir)] == reg[pce_op_regB(ir)]:
                frag_eq = 1
            else:
                frag_eq = 0

        elif op_code == JE:
            if frag_eq == 1:
                pc = pce_op_addr(ir)

        elif op_code == JMP:
            pc = pce_op_addr(ir)

        elif op_code == LD:
            reg[pce_op_regA(ir)] = ram[pce_op_addr(ir)]

        elif op_code == ST:
            ram[pce_op_addr(ir)] = reg[pce_op_regA(ir)]

        elif op_code == HLT:
            break

        else:
            break

    print("\n|{}{}{}|".format("-" * 87, "rom status", "-" * 87))
    for i in range(0, 256):
        print("rom[{:3}] = {:5}   ".format(i, rom[i]), end="")
        if (i + 1) % 8 == 0:
            print()

    print("\n|{}{}{}|".format("-" * 87, "ram status", "-" * 87))
    for i in range(0, 256):
        print("ram[{:3}] = {:5}   ".format(i, ram[i]), end="")
        if (i + 1) % 8 == 0:
            print()


def pce_mov(ra, rb):
    return (MOV << 11) | (ra << 8) | (rb << 5)


def pce_add(ra, rb):
    return (ADD << 11) | (ra << 8) | (rb << 5)


def pce_sub(ra, rb):
    return (SUB << 11) | (ra << 8) | (rb << 5)


def pce_and(ra, rb):
    return (AND << 11) | (ra << 8) | (rb << 5)


def pce_or(ra, rb):
    return (OR << 11) | (ra << 8) | (rb << 5)


def pce_sl(ra):
    return (SL << 11) | (ra << 8)


def pce_sr(ra):
    return (SR << 11) | (ra << 8)


def pce_sra(ra):
    return (SRA << 11) | (ra << 8)


def pce_ldl(ra, ival):
    return (LDL << 11) | (ra << 8) | (ival & 0x00ff)


def pce_ldh(ra, ival):
    return (LDH << 11) | (ra << 8) | (ival & 0x00ff)


def pce_cmp(ra, rb):
    return (CMP << 11) | (ra << 8) | (rb << 5)


def pce_je(addr):
    return (JE << 11) | (addr & 0x00ff)


def pce_jmp(addr):
    return (JMP << 11) | (addr & 0x00ff)


def pce_ld(ra, addr):
    return (LD << 11) | (ra << 8) | (addr & 0x00ff)


def pce_st(ra, addr):
    return (ST << 11) | (ra << 8) | (addr & 0x00ff)


def pce_hlt():
    return HLT << 11


def pce_op_code(ir):
    return ir >> 11


def pce_op_regA(ir):
    return (ir >> 8) & 0x0007


def pce_op_regB(ir):
    return (ir >> 5) & 0x0007


def pce_op_data(ir):
    return ir & 0x00ff


def pce_op_addr(ir):
    return ir & 0x00ff


def asm_read_file():
    with open("test.asm", "r", encoding="utf-8") as f:
        data = f.readlines()

        counter = 0

        for i in data:
            if i[0] == ";":
                continue
            counter = asm_load_instruction(i, counter)


def asm_load_instruction(order, counter):
    order = order.split(" ")
    if order[0] == "MOV":
        ra, rb = asm_parse_mnemonic(order)
        rom[counter] = pce_mov(ra, rb)

    elif order[0] == "ADD":
        ra, rb = asm_parse_mnemonic(order)
        rom[counter] = pce_add(ra, rb)

    elif order[0] == "SUB":
        ra, rb = asm_parse_mnemonic(order)
        rom[counter] = pce_sub(ra, rb)

    elif order[0] == "AND":
        ra, rb = asm_parse_mnemonic(order)
        rom[counter] = pce_and(ra, rb)

    elif order[0] == "OR":
        ra, rb = asm_parse_mnemonic(order)
        rom[counter] = pce_or(ra, rb)

    elif order[0] == "SL":
        ra = asm_parse_mnemonic(order)
        rom[counter] = pce_sl(ra)

    elif order[0] == "SR":
        ra = asm_parse_mnemonic(order)
        rom[counter] = pce_sr(ra)

    elif order[0] == "SRA":
        ra = asm_parse_mnemonic(order)
        rom[counter] = pce_sra(ra)

    elif order[0] == "LDL":
        ra, rb = asm_parse_mnemonic(order)
        rom[counter] = pce_ldl(ra, rb)

    elif order[0] == "LDH":
        ra, rb = asm_parse_mnemonic(order)
        rom[counter] = pce_ldh(ra, rb)

    elif order[0] == "CMP":
        ra, rb = asm_parse_mnemonic(order)
        rom[counter] = pce_cmp(ra, rb)

    elif order[0] == "JE":
        ra = asm_parse_mnemonic(order)
        rom[counter] = pce_je(ra)

    elif order[0] == "JMP":
        ra = asm_parse_mnemonic(order)
        rom[counter] = pce_jmp(ra)

    elif order[0] == "LD":
        ra, rb = asm_parse_mnemonic(order)
        rom[counter] = pce_ld(ra, rb)

    elif order[0] == "ST":
        ra, rb = asm_parse_mnemonic(order)
        rom[counter] = pce_st(ra, rb)

    elif order[0] == "HLT\n":
        rom[counter] = pce_hlt()

    return counter + 1


def asm_parse_mnemonic(order):
    order[1] = order[1].strip("\n")

    if order[1].isdecimal():
        ra = int(order[1])
    elif "REG" in order[1]:
        ra = asm_reg_return(order[1])
    else:
        ra = None

    if len(order) == 2:
        return ra

    order[2] = order[2].strip("\n")

    if order[2].isdecimal():
        rb = int(order[2])
    elif "REG" in order[2]:
        rb = asm_reg_return(order[2])
    else:
        rb = None

    return ra, rb


def asm_reg_return(arg_reg):
    if arg_reg == "REG0":
        return REG0
    elif arg_reg == "REG1":
        return REG1
    elif arg_reg == "REG2":
        return REG2
    elif arg_reg == "REG3":
        return REG3
    elif arg_reg == "REG4":
        return REG4
    elif arg_reg == "REG5":
        return REG5
    elif arg_reg == "REG6":
        return REG6
    elif arg_reg == "REG7":
        return REG7
    else:
        return None


if __name__ == "__main__":
    pce_main()
