#
#@author ZPaul2Fresh8
#@category Import
#@keybinding
#@menupath
#@toolbar

#format = TYPE("FUNCTION") | NAME | ADDRESS | DESCRIPTION

from ghidra.program.model.symbol.SourceType import *
import string

functionManager = currentProgram.getFunctionManager()
c = 0 # created routines
r = 0 # renamed routines
o = 0 # omissions
l = 0 # labels
f = askFile("Give me a file to open", "Go baby go!")

for line in file(f.absolutePath):  # note, cannot use open(), since that is in GhidraScript
    line = line.strip()
    pieces = line.split("|")
    if len((pieces)) < 3:
            #line_d ="{} has less than 3 pieces, skipping it."
            #print(line_d.format(line_d))
            o += 1
            continue

    try:
        
        name = pieces[1]
        value_str = "0x" + pieces[2]
        value = int(value_str, 16)  # convert to dec
        value = (value / 8) & 0xFFFFF
        
        #value_h = hex(value_int)  # convert to hex
        
        #value.format(value, format_spec)
        address = toAddr(value)
        comment = pieces[3]        

        try:
            function_or_label = pieces[0]
        except IndexError:
            function_or_label = "l" or "RAM"
    
        if function_or_label == "f" or function_or_label == "ROUTINE":
            func = functionManager.getFunctionAt(address)
    
            if func is not None:
                old_name = func.getName()
                func.setName(name, USER_DEFINED)
                setPlateComment(address, comment)
                r+=1
            else:
                func = createFunction(address, name)
                setPlateComment(address, comment)
                c+=1
    
        else:
            #print(value)
            if value < 0xfffff:
                #address_line = "ram:" + value
                #createLabel(address, name, False)
                l+=1
            elif value < 0xff800000: # ram locations
                print(value)
                #address_line = "rom:{}" + value
                createLabel(address, name, False)
                #createLabel(value_str, name, 'ram', False, DEFAULT)
                l+=1
            #print("Created label {} at address {}".format(name, address))
            

            
    except:
        error = "Error: Line was not correct, trying next one."
        #print(error.format(pieces[0],pieces[1],pieces[2],pieces[3]))
        o+=1
        continue
print("")
print("+=======================================RESULTS========================================".format(c))
print("|   {} function created".format(c))
print("|   {} function renamed".format(r))
print("|   {} labels created".format(l))
print("|   {} lines omitted due to unexpected format.".format(o))
print("+======================================================================================".format(c))
print("")
