;テストコメント
; ";"から始まる行はコメント扱い
;オペコードとオペランドは必ず1つの空白文字で区切る
;一番右のオペランドの右に空白文字が入るとエラーが起こる
;最終行は必ず改行する
LDH REG0 0
LDL REG0 0
LDH REG1 0
LDL REG1 1
LDH REG2 0
LDL REG2 0
LDH REG3 0
LDL REG3 10
ADD REG2 REG1
ADD REG0 REG2
ST REG0 64
CMP REG2 REG3
JE 14
JMP 8
HLT
