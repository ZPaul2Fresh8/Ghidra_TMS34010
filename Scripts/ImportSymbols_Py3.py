#@author ZPaul2Fresh8
#@category Import
#@keybinding
#@menupath
#@toolbar

# Python 3
#format = TYPE("FUNCTION") | NAME | ADDRESS | DESCRIPTION

from ghidra.program.model.symbol import SourceType # FIXED: Don't use * import here
import string

functionManager = currentProgram.getFunctionManager()
c = 0 # created routines
r = 0 # renamed routines
o = 0 # omissions
l = 0 # labels
f = askFile("Give me a file to open", "Go baby go!")

# FIXED: 'file()' is removed in Python 3, using 'open()'
with open(f.absolutePath, 'r') as file_handle:
    for line in file_handle:
        line = line.strip()
        pieces = line.split("|")
        
        if len((pieces)) < 3:
            o += 1
            continue

        try:
            name = pieces[1]
            value_str = "0x" + pieces[2]
            value = int(value_str, 16)  # convert to dec
            
            # FIXED: Python 3 division returns float, used // for integer division
            value = (value // 8) & 0xFFFFF 
            
            address = toAddr(value)
            comment = pieces[3]        

            try:
                function_or_label = pieces[0]
            except IndexError:
                function_or_label = "l" # Default

            if function_or_label == "f" or function_or_label == "ROUTINE":
                func = functionManager.getFunctionAt(address)
    
                if func is not None:
                    old_name = func.getName()
                    # FIXED: Explicitly calling SourceType.USER_DEFINED
                    func.setName(name, SourceType.USER_DEFINED) 
                    setPlateComment(address, comment)
                    r+=1
                else:
                    func = createFunction(address, name)
                    setPlateComment(address, comment)
                    c+=1
    
            else:
                if value < 0xfffff:
                    # createLabel(address, name, False)
                    l+=1
                elif value < 0xff800000: # ram locations
                    print(value)
                    createLabel(address, name, False)
                    l+=1
            
        except Exception as e: # FIXED: Catching specific exception to see errors
            print("Error on line: " + line + " -> " + str(e))
            o+=1
            continue

print("")
print("+=======================================RESULTS========================================")
print("|   {} function created".format(c))
print("|   {} function renamed".format(r))
print("|   {} labels created".format(l))
print("|   {} lines omitted due to unexpected format or error.".format(o))
print("+======================================================================================")
print("")
