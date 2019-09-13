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
    ir = 0
    frag_eq = 0
    assembler()

    while True:
        ir = rom[pc]
        print("{} {:x} {} {} {} {}"
              .format(pc, ir, reg[0], reg[1], reg[2], reg[3]))
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

    print("ram[64] = {}".format(ram[64]))


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


def assembler():
    rom[0] = pce_ldh(REG0, 0)
    rom[1] = pce_ldl(REG0, 0)
    rom[2] = pce_ldh(REG1, 0)
    rom[3] = pce_ldl(REG1, 1)
    rom[4] = pce_ldh(REG2, 0)
    rom[5] = pce_ldl(REG2, 0)
    rom[6] = pce_ldh(REG3, 0)
    rom[7] = pce_ldl(REG3, 10)
    rom[8] = pce_add(REG2, REG1)
    rom[9] = pce_add(REG0, REG2)
    rom[10] = pce_st(REG0, 64)
    rom[11] = pce_cmp(REG2, REG3)
    rom[12] = pce_je(14)
    rom[13] = pce_jmp(8)
    rom[14] = pce_hlt()


"""
def read_file():
    with open("test.asm", "r", encoding="utf-8") as f:
        data = f.readlines()
        counter = 0
        for i in data:
            if i[0] == ";":
                continue
            load_order(i, counter)


def load_order(order, counter):
    order = order.split(" ")
    


def state():
    pass


def utility():
    pass

"""
if __name__ == "__main__":
    pce_main()
