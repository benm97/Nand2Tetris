@R13
D=M
@a
M=D
@R15
M=0
@ans
M=1
(DIVIDE)
@count
M=0
@R14
D=M
@c
M=D


@R14
D=M
@a
D=M-D
@END
D;JLT


(LOOP1)
@c
D=M
@a
D=D-M
@ENDLOOP1
D;JGE

@c
M=M<<
@count
M=M+1
@LOOP1
0;JMP
(ENDLOOP1)

@count
D=M
@j
M=-D
M=M+1
(LOOP2)
@j
D=M
@ENDLOOP2
D;JGE
@ans
M=M<<
@j
M=M+1
@LOOP2
0;JMP
(ENDLOOP2)
@c
M=M>>
@ans
D=M
@R15
M=M+D
@ans
M=1
@c
D=M
@a
M=M-D
@DIVIDE
0;JMP
(END)
@END
0;JMP