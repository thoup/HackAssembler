Assembler.hack is a 16-bit machine language assembler for the 16-bit Hack Assembly Language. 
4
This project was completed as part of building a complete 16-bit computer from the grounds up through a course known as Nand2Tetris.
5
​
6
## Description
7
​
8
Assembler.hack takes a program source code file written in the Hack Assembly Language, an .asm text file, and then transforms it into binary machine code in the Hack Machine Language. 
9
The assembled machine code program is then added to a new .hack text file with the same name.
10
This machine code can then be ran on the Hack CPU, which was also designed previously in this course.
11
​
12
The Assembling process is implemented in two passes. 
13
The first pass scans the whole program, adding only the labels to the Symbol Table.
14
The second pass scans the whole program once again, registering all variables in the Symbol Table. It also parses and computes every instruction, generating binary machine code and writing this code to the new .hack text file.
15
​
16
17
​
18
1. **Assembler.py**: The main module. Implements both passes, parsing every instruction and computing the corresponding binary code, which is added to the destination file.
19
​
20
​
21
## Example Usage
22
​
25
```
26
$ python Assembler.py <file>
27
```
28
​
29
### Max.asm
30
​
31
```asm
// Given two numbers stored in register R0 and R1,
// compute the maximum and store it in the R2 register.

  @R0
  D=M              // Get first number
  @R1
  D=D-M            // Subtract second number from first
  @OUTPUT_FIRST
  D;JGT            // if D>0 (first is greater) goto output_first
  @R1
  D=M              // Otherwise, store second number
  @OUTPUT_D
  0;JMP            // goto output_d

(OUTPUT_FIRST)
  @R0
  D=M              // D = first number

(OUTPUT_D)
  @R2
  M=D              // Store greatest number

(INFINITE_LOOP)
  @INFINITE_LOOP
  0;JMP            // infinite loop
```


### Max.hack

```
0000000000000000
1111110000010000
0000000000000001
1111010011010000
0000000000001010
1110001100000001
0000000000000001
1111110000010000
0000000000001100
1110101010000111
0000000000000000
1111110000010000
0000000000000010
1110001100001000
0000000000001110
1110101010000111
```
