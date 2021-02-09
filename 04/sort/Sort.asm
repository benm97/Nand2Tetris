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
D+1;JGE

//Condition
@j
D=M //D=j

@count //j-i
M=D

@i
D=M //D=i

@count
M=M-D

@count
D=M

@R14
D=M+D //D is the address
@firstAddress
M=D
A=D

D=M //D=arr[j]
@arrj
M=D
@compare
M=D

@count
D=M+1
@R14
D=M+D //A is the address
@secondAddress
M=D
A=D

D=M //D=arr[j+1]
@arrjplusone
M=D
@compare
M=M-D
D=M
@ENDCOND
D;JGE

//swap
@arrjplusone
D=M
@firstAddress
A=M
M=D

@arrj
D=M
@secondAddress
A=M
M=D

(ENDCOND)
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
@END
0;JMP
