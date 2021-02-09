// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
(START)
@24576
D=M
@BLACKEN
D;JGT
@CLEAR
D;JEQ
@START
0;JMP
(BLACKEN)
@i
M=0
@8191
D=A
@i
M=M-D
(LOOPBLACK)
@i
D=M
@ENDLOOPBLACK
D;JGT
@SCREEN
A=A-D
M=-1
@i
M=M+1
@LOOPBLACK
0;JMP
(ENDLOOPBLACK)
@START
0;JMP

(CLEAR)
@i
M=0
@8191
D=A
@i
M=M-D
(LOOPWHITE)
@i
D=M
@ENDLOOPWHITE
D;JGT
@SCREEN
A=A-D
M=0
@i
M=M+1
@LOOPWHITE
0;JMP
(ENDLOOPWHITE)
@START
0;JMP
