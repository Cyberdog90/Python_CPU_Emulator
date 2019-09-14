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

    asm_read_file()

    while True:
        ir = rom[pc]
        pc += 1

        if pce_op_code(ir) == MOV:
            reg[pce_op_regA(ir)] = reg[pce_op_regB(ir)]

        elif pce_op_code(ir) == ADD:
            reg[pce_op_regA(ir)] += reg[pce_op_regB(ir)]

        elif pce_op_code(ir) == SUB:
            reg[pce_op_regA(ir)] -= reg[pce_op_regB(ir)]

        elif pce_op_code(ir) == AND:
            reg[pce_op_regA(ir)] &= reg[pce_op_regB(ir)]

        elif pce_op_code(ir) == OR:
            reg[pce_op_regA(ir)] |= reg[pce_op_regB(ir)]

        elif pce_op_code(ir) == SL:
            reg[pce_op_regA(ir)] = reg[pce_op_regA(ir)] << 1

        elif pce_op_code(ir) == SR:
            reg[pce_op_regA(ir)] = reg[pce_op_regA(ir)] >> 1

        elif pce_op_code(ir) == SRA:
            reg[pce_op_regA(ir)] = (reg[pce_op_regA(ir)] & 0x8000) | \
                                   (reg[pce_op_regA(ir)] >> 1)

        elif pce_op_code(ir) == LDL:
            reg[pce_op_regA(ir)] = (reg[pce_op_regA(ir)] & 0xff00) | \
                                   (pce_op_data(ir) & 0x00ff)

        elif pce_op_code(ir) == LDH:
            reg[pce_op_regA(ir)] = (pce_op_data(ir) << 8) | \
                                   (reg[pce_op_regA(ir)] & 0x00ff)

        elif pce_op_code(ir) == CMP:
            if reg[pce_op_regA(ir)] == reg[pce_op_regB(ir)]:
                frag_eq = 1
            else:
                frag_eq = 0

        elif pce_op_code(ir) == JE:
            if frag_eq == 1:
                pc = pce_op_addr(ir)

        elif pce_op_code(ir) == JMP:
            pc = pce_op_addr(ir)

        elif pce_op_code(ir) == LD:
            reg[pce_op_regA(ir)] = ram[pce_op_addr(ir)]

        elif pce_op_code(ir) == ST:
            ram[pce_op_addr(ir)] = reg[pce_op_regA(ir)]

        elif pce_op_code(ir) == HLT:
            break

        else:
            break


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
    else:
        ra = asm_reg_return(order[1])

    if len(order) == 2:
        return ra

    order[2] = order[2].strip("\n")

    if order[2].isdecimal():
        rb = int(order[2])
    else:
        rb = asm_reg_return(order[2])

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
    else:
        return REG7


if __name__ == "__main__":
    pce_main()
