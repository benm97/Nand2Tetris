@R15
D=M

@i //init loop 1
M=-D

(LOOP1)
@i
D=M
@END
D;JGE // condition loop 1

@j
M=D //init loop 2
(LOOP2)
@j
D=M
@ENDLOOP2
D;JGE

//Condition
@R14
D=M //D is the address

@j
M=M+1 //increment loop 2
@LOOP2
0;JMP
(ENDLOOP2)

@i
M=M+1 //increment loop 1
@LOOP1
0;JMP
(END)

