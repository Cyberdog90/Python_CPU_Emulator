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

reg = [0] * 8  # 汎用レジスタ
rom = [0] * 256  # プログラム領域
ram = [0] * 256  # データ領域


def pce_main():
    pc = 0  # プログラムカウンタ
    ir = 0  # インストラクションレジスタ
    frag_eq = 0  # 比較用フラグ変数
    assembler()


def pce_mov():
    pass


def pce_add():
    pass


def pce_sub():
    pass


def pce_and():
    pass


def pce_or():
    pass


def pce_sl():
    pass


def pce_sr():
    pass


def pce_sra():
    pass


def pce_ldl():
    pass


def pce_ldh():
    pass


def pce_cmp():
    pass


def pce_je():
    pass


def pce_jmp():
    pass


def pce_ld():
    pass


def pce_st():
    pass


def pce_hlt():
    pass


def pce_op_code():
    pass


def pce_op_regA():
    pass


def pce_op_regB():
    pass


def pce_op_data():
    pass


def pce_op_addr():
    pass


def assembler():
    # テスト用コード
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


def read_file():
    pass


def load_order():
    pass


def state():
    pass


def utility():
    pass


if __name__ == "__main__":
    pce_main()
