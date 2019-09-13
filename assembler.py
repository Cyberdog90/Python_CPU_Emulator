"""
def read_file():
    with open("test.asm", "r", encoding="utf-8") as f:
        data = f.readlines()

        counter = 0

        for i in data:
            if i[0] == ";":
                continue
            load_instruction(i, counter)


def load_instruction(order, counter):
    order = order.split(" ")
    if order[0] == "MOV":
        counter = mov_instruction_set(order, counter)

    elif order[0] == "ADD":
        counter = add_instruction_set(order, counter)

    elif order[0] == "SUB":
        counter = sub_instruction_set(order, counter)

    elif order[0] == "AND":
        counter = and_instruction_set(order, counter)

    elif order[0] == "OR":
        counter = or_instruction_set(order, counter)

    elif order[0] == "SL":
        counter = sl_instruction_set(order, counter)

    elif order[0] == "SR":
        counter = sr_instruction_set(order, counter)

    elif order[0] == "SRA":
        counter = sra_instruction_set(order, counter)

    elif order[0] == "LDL":
        counter = ldl_instruction_set(order, counter)

    elif order[0] == "LDH":
        counter = ldh_instruction_set(order, counter)

    elif order[0] == "CMP":
        counter = cmp_instruction_set(order, counter)

    elif order[0] == "JE":
        counter = je_instruction_set(order, counter)

    elif order[0] == "JMP":
        counter = jmp_instruction_set(order, counter)

    elif order[0] == "LD":
        counter = ld_instruction_set(order, counter)

    elif order[0] == "ST":
        counter = st_instruction_set(order, counter)

    elif order[0] == "HLT":
        counter = hlt_instruction_set(counter)

    return counter


def mov_instruction_set(order, counter):
    if order[1].isdecimal():
        ra = int(order[1])
    elif "REG" in order[1]:
        ra = reg_return(order[1])
    else:
        ra = order[1]

    if order[2].isdecimal():
        rb = int(order[2])
    elif "REG" in order[1]:
        rb = reg_return(order[1])
    else:
        rb = order[2]

    rom[counter] = pce_mov(ra, rb)
    return counter + 1


def add_instruction_set(order, counter):
    if order[1].isdecimal():
        ra = int(order[1])
    elif "REG" in order[1]:
        ra = reg_return(order[1])
    else:
        ra = order[1]

    if order[2].isdecimal():
        rb = int(order[2])
    elif "REG" in order[1]:
        rb = reg_return(order[1])
    else:
        rb = order[2]

    rom[counter] = pce_add(ra, rb)
    return counter + 1


def sub_instruction_set(order, counter):
    if order[1].isdecimal():
        ra = int(order[1])
    elif "REG" in order[1]:
        ra = reg_return(order[1])
    else:
        ra = order[1]

    if order[2].isdecimal():
        rb = int(order[2])
    elif "REG" in order[1]:
        rb = reg_return(order[1])
    else:
        rb = order[2]

    rom[counter] = pce_sub(ra, rb)
    return counter + 1


def and_instruction_set(order, counter):
    if order[1].isdecimal():
        ra = int(order[1])
    elif "REG" in order[1]:
        ra = reg_return(order[1])
    else:
        ra = order[1]

    if order[2].isdecimal():
        rb = int(order[2])
    elif "REG" in order[1]:
        rb = reg_return(order[1])
    else:
        rb = order[2]

    rom[counter] = pce_and(ra, rb)
    return counter + 1


def or_instruction_set(order, counter):
    if order[1].isdecimal():
        ra = int(order[1])
    elif "REG" in order[1]:
        ra = reg_return(order[1])
    else:
        ra = order[1]

    if order[2].isdecimal():
        rb = int(order[2])
    elif "REG" in order[1]:
        rb = reg_return(order[1])
    else:
        rb = order[2]

    rom[counter] = pce_or(ra, rb)
    return counter + 1


def sl_instruction_set(order, counter):
    if order[1].isdecimal():
        ra = int(order[1])
    elif "REG" in order[1]:
        ra = reg_return(order[1])
    else:
        ra = order[1]

    rom[counter] = pce_sl(ra)
    return counter + 1


def sr_instruction_set(order, counter):
    if order[1].isdecimal():
        ra = int(order[1])
    elif "REG" in order[1]:
        ra = reg_return(order[1])
    else:
        ra = order[1]

    rom[counter] = pce_sr(ra)
    return counter + 1


def sra_instruction_set(order, counter):
    if order[1].isdecimal():
        ra = int(order[1])
    elif "REG" in order[1]:
        ra = reg_return(order[1])
    else:
        ra = order[1]

    rom[counter] = pce_sra(ra)
    return counter + 1


def ldl_instruction_set(order, counter):
    if order[1].isdecimal():
        ra = int(order[1])
    elif "REG" in order[1]:
        ra = reg_return(order[1])
    else:
        ra = order[1]

    if order[2].isdecimal():
        rb = int(order[2])
    elif "REG" in order[1]:
        rb = reg_return(order[1])
    else:
        rb = order[2]

    rom[counter] = pce_ldl(ra, rb)
    return counter + 1


def ldh_instruction_set(order, counter):
    if order[1].isdecimal():
        ra = int(order[1])
    elif "REG" in order[1]:
        ra = reg_return(order[1])
    else:
        ra = order[1]

    if order[2].isdecimal():
        rb = int(order[2])
    elif "REG" in order[1]:
        rb = reg_return(order[1])
    else:
        rb = order[2]

    rom[counter] = pce_ldh(ra, rb)
    return counter + 1


def cmp_instruction_set(order, counter):
    if order[1].isdecimal():
        ra = int(order[1])
    elif "REG" in order[1]:
        ra = reg_return(order[1])
    else:
        ra = order[1]

    if order[2].isdecimal():
        rb = int(order[2])
    elif "REG" in order[1]:
        rb = reg_return(order[1])
    else:
        rb = order[2]

    rom[counter] = pce_cmp(ra, rb)
    return counter + 1


def je_instruction_set(order, counter):
    if order[1].isdecimal():
        ra = int(order[1])
    elif "REG" in order[1]:
        ra = reg_return(order[1])
    else:
        ra = order[1]

    rom[counter] = pce_je(ra)
    return counter + 1


def jmp_instruction_set(order, counter):
    if order[1].isdecimal():
        ra = int(order[1])
    elif "REG" in order[1]:
        ra = reg_return(order[1])
    else:
        ra = order[1]

    rom[counter] = pce_jmp(ra)
    return counter + 1


def ld_instruction_set(order, counter):
    if order[1].isdecimal():
        ra = int(order[1])
    elif "REG" in order[1]:
        ra = reg_return(order[1])
    else:
        ra = order[1]

    if order[2].isdecimal():
        rb = int(order[2])
    elif "REG" in order[1]:
        rb = reg_return(order[1])
    else:
        rb = order[2]

    rom[counter] = pce_ld(ra, rb)
    return counter + 1


def st_instruction_set(order, counter):
    if order[1].isdecimal():
        ra = int(order[1])
    elif "REG" in order[1]:
        ra = reg_return(order[1])
    else:
        ra = order[1]

    if order[2].isdecimal():
        rb = int(order[2])
    elif "REG" in order[1]:
        rb = reg_return(order[1])
    else:
        rb = order[2]

    rom[counter] = pce_st(ra, rb)
    return counter + 1


def hlt_instruction_set(counter):
    pce_hlt()
    return counter + 1


def reg_return(arg_reg):
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
"""
