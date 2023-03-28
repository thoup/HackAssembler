import sys
import regex as re



# Initialize symbol table and computation dicts
symbol_table = {
    "R0":"0", 
    "R1":"1", 
    "R2":"2", 
    "R3":"3", 
    "R4":"4", 
    "R5":"5", 
    "R6":"6", 
    "R7":"7", 
    "R8":"8", 
    "R9":"9", 
    "R10":"10", 
    "R11":"11", 
    "R12":"12", 
    "R13":"13", 
    "R14":"14", 
    "R15":"15", 
    "SCREEN":"16384", 
    "KBD":"24576", 
    "SP" : "0", 
    "LCL": "1", 
    "ARG": "2", 
    "THIS":"3", 
    "THAT":"4"
    }

dest_dict = {
    "null": "000",
    "M": "001",
    "D": "010",
    "A": "100",
    "MD": "011",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
    }

comp_dict = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
    }

jump_dict = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
    }


# Parser methods used to parse every instruction
class Parser:
    
    CompPattern = r"(?<=\S+=)[^;/ ]*"  # Pattern used in comp
    JumpPattern = r"(?<=;)[^/ ]*"  # Pattern used in jump
    
    # A instructions
    @staticmethod
    def Ainstruction(inst):
        return inst[1:]  # Simply remove "@"

    # dest
    @staticmethod
    def dest(inst):
        if inst.find("=") == -1:  # If no "=", no dest
            return "null"
        else:
            return inst.split("=")[0]  # Get value before "="
        
    # comp
    @staticmethod
    def comp(inst):
        if inst.find("=") == -1:  # If no "=", get value before ";"
            return inst.split(";")[0]
        else:
            match = re.search(Parser.CompPattern, inst)  # Get value of computation
            return match.group()
        
    # jump
    @staticmethod
    def jump(inst):
        match = re.search(Parser.JumpPattern, inst)
        if match:
            return match.group()
        else:
            return "null"



# Translator comomputes binary values
class Translator:
    
    @staticmethod
    def Ainstruction(inst):  # Convert A value to binary
        binary = bin(int(inst))
        val = (binary.replace("b", ""))
        length = 16 - len(val)
        return ("0" * length + val)
    
    @staticmethod
    def dest(inst):
        return(dest_dict[inst])  # Convert dest to binary
    
    @staticmethod
    def comp(inst):
        return(comp_dict[inst])  # Convert comp to binary
    
    @staticmethod
    def jump(inst):
        return(jump_dict[inst])  # Convert jump to binary
    


# Manage symbol table
class Symbols():

    SymbolPattern = r"(?<=\()\S+(?=\))"  # Used to extract name from label              

    @staticmethod
    def Add_Label(inst):
        index = content.index(inst)  # Don't need +1, since this label is deleted from list
        content.remove(inst)
        match = re.search(Symbols.SymbolPattern, inst)
        symbol = match.group()
        symbol_table[symbol] = index
    

# Every instruction is in content
content = []
            
def main():
    
    length = len(sys.argv)

    if length != 2: 
        sys.exit("Error: Provide a File")
    else:
        [file] = sys.argv[1:]  # Unpack full file name to variable
        name = file.split(".")[0]  # Get file name, without extension
        name += ".hack"  # Used for output
    
    with open(file) as f:
        for line in f:
            if (line[0] != "\n") and (line[0] != "/"):  # Add only instructions
                content.append(line.strip())


    # Pass 1: Add all labels
    i = 0
    while i < (len(content)):
        if content[i][0] == "(":
            Symbols.Add_Label(content[i])  # Don't increment i if adding label, since this label is removed from list
        else:
            i += 1

    hack = open(name, "w")
    variable_value = 16

    # Pass 2: Compute values
    for line in content:
        if line[0] == "@":  # A-Instruction
        
            Presult = Parser.Ainstruction(line)
            
            if not (Presult.isnumeric()):
                
                if symbol_table.get(Presult):  # If value is in symbol table, then it is a label
                    Presult = symbol_table[Presult]
                else:  # Else, it is a variable
                    symbol_table[Presult] = variable_value
                    Presult = variable_value
                    variable_value += 1
                
            result = Translator.Ainstruction(Presult)
                
        else:  # C-Instruction
            
            Pcomp = Parser.comp(line)
            Pdest = Parser.dest(line)
            Pjump = Parser.jump(line)
            
            comp = Translator.comp(Pcomp)
            dest = Translator.dest(Pdest)
            jump = Translator.jump(Pjump)
            
            result = "111" + comp + dest + jump

        hack.write(result + "\n")  # Add to destination file
    
    

# Run Assembler
main()