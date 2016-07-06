# CSU Student Success File Processor

import re, copy, sys

def menu():
    print("Menu - What type of file to process?")
    print("B1. Census Class File")
    print("B2. EOT Grade File")
    print("C. Remedial Courses")
    print("D. GE Courses")
    print("E. EOT Processing")
    print("F1. EO1037 Forgiven Averages")
    print("F2. EO1037 Reporting Totals")
    print("H. Online ICE/CourseMatch Classes")
    print("J. Proven Course Redesign")
    print("O. Online/Distance Learning")
    print("P. Crse Sect Attrib Online State EE CalStT")
    print("ESP. Early Start Program")
    print("ERSS. Enrollment Reporting System - Student")
    choice = input("Type the letter of the report above. ")
    choice = choice.upper()
    return choice

#based on menu load the report specifications
def fileType(choice):
#the following arrays define the maximum number of characters for each field in order
    fileSpecsB = [9,15,9,4,1,2,5,4,3,2,3,3,30]
    fileSpecsC = [4,1,2,5,4,3,3,1,30,1,3,2,1,1]
    fileSpecsH = [4,1,2,5,4,3,2,3,1,30,1,3,1,1]
    fileSpecsJ = [4,1,2,5,4,3,3,1,30,1,3,1,1]
    fileSpecsD = [4,1,2,5,4,3,3,1,30,1,3,2,1,1]
    fileSpecsE = [9,15,9,4,1,2,5,2,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,3,3,3,3,1,1,1,1,1]
    fileSpecsO = [5,1,1,1,2,3,1,5,4,3,2,1,4,1,3,1,2,2,1,6,1,4,1,1,1,4,1,2,1,9,1,1]
    fileSpecsP = [4,1,2,5,4,3,2,3,1,30,1,2,1]
    fileSpecsF1 = [9,15,9,4,1,2,5,4,2,254,2,254,2,3,3,254,2,3,3,254,26]
    fileSpecsF2 = [30,30,9,15,9,4,1,2,4,5,1,5,5,5,6,1,5,1,5,6,1,1,5,5,5,6,1,1,5,5,5,6,1,5,6,26]
    fileSpecsERSS = [9,4,1,2,8,1,1,1,4,4,4,1,6,5,1,1,1,1,1,5,1,3,1,1,4,3,3,4,3,1,1,1,1,1,1,6,1,1,1,1,2,1,3,2,1,1,1,3,3,3,3,2,1,2,2,2,2,2,8,2,2,2,2,3,3,3,3,3,3,4,2,2,2,2,2,2,2,2,3,1,4,3,1,8,2,1,3,3,4,1,1,2,2,1,1,2,1,1,9,15,5,1,1,84]
    fileSpecsESP = [2,9,2,9,9,23,30,30,30,15,10,55,55,55,30,6,12,3,24,6,70,8,10,5,30,9,3,3,10,10,3,3,8,10,5,30,9,3,3,10,10,3,3,8,10,5,30,9,3,3,10,10,3,3,8,10,5,30,9,3,3,10,10,3,6,11]
    if choice == "B1":
        return fileSpecsB
    elif choice == "B2":
        return fileSpecsB
    elif choice == "C":
        return fileSpecsC
    elif choice == "H":
            return fileSpecsH   
    elif choice == "J":
                return fileSpecsJ
    elif choice == "D":
        return fileSpecsD
    elif choice == "E":
        return fileSpecsE
    elif choice == "F1":
        return fileSpecsF1  
    elif choice == "F2":
        return fileSpecsF2 
    elif choice == "O":
        return fileSpecsO
    elif choice == "P":
        return fileSpecsP    
    elif choice == "ERSS":
        return fileSpecsERSS      
    elif choice == "ESP":
            return fileSpecsESP       
    else:
        print("Invalid choice!\n")
        return -1
#writes to output filename
def fullName(choice):
    if choice == "B2":
        return "B_EOT_Grade"
    elif choice == "B1":
        return "B_Census_Class"
    elif choice == "C":
        return "C_Census_Rem_CA"
    elif choice == "H":
        return "H_Census_CourseMatch"    
    elif choice == "J":
            return "J_EOT_Proven_Cour_Red"    
    elif choice == "D":
        return "D_Census_GE_CA"
    elif choice == "E":
        return "E_EOT_Proc"
    elif choice == "F1":
        return "F_EO1037_Avg"
    elif choice == "F2":
        return "F_EO1037_Rpt"
    elif choice == "O":
        return "APDB.IPEDS.extract."
    elif choice == "P":
        return "P_Census_Online_CourseSec"    
    elif choice == "ERSS":
        return "ERSS"        
    elif choice == "ESP":
            return "Early Start_Program"          
    else:
        print("Invalid choice!\n")
        return "Error"

#resizes the string to match number of characters in filespecs
def makeItFit(field,size,pad):
    field = field.strip()
    if pad == "0":
        if (len(field) >= size):
            str = field[:size]
        else:
            str = "0" * (size - len(field)) + field
    else:
        if (len(field) >= size):
            str = field[:size]
        else:
            str = field + " " * (size - len(field))
    return str


#this main program - loads a file, asks if there is a header to skip, converts a delimited line to a fixed format line based on report specifications, and writes the output file
def getFile(choice):
    fileSpecs = fileType(choice)
    if fileSpecs == -1:
        return
    #print(fileSpecs)
    linecount = 0
    row = 0
    infile = input("What is the delimited file name? ")
    docin = open(infile)
    year = input("For what year is this file?: ")
    term = input("Term code (1/2/3/4):  ")    
    session = input("Is this for (1) State (2) Self Support (3) CalState Teach (0) Ignore: ")
    if (session == 1 or session == '1'):
        sessionStr = "_State"
    elif (session == 2 or session == '2'):
        sessionStr = "_Self"
    elif (session == 3 or session == '3'):
        sessionStr = "_CST"    
    elif (session == 0 or session == '0'):
            sessionStr = ""        
    if (choice=="O"):
        outfile = fullName(choice) + year + term +  "06.txt"
    else:
        if (choice=="J"):
            outfile = "sss06_" + fullName(choice) + "_" + str(year) + str(term) + ".txt"
        else:    
            outfile = "sss06_" + fullName(choice) + sessionStr + "_" + str(year) + str(term) + ".txt"
    docout = open(outfile,"w")
    hasHeader = input("Does this file have the column names on the first line? Y/N \n")
    if (hasHeader == 'Y' or hasHeader == 'y'):
        linecount = 0
    elif (hasHeader == 'N' or hasHeader == 'n'):
        linecount = linecount + 1
    else:
        print("Invalid choice\n")
    for line in docin:
        newline = ""
        field = re.split("\t",line)        
        if (linecount > 0):
            if (row > 0):
                docout.write("\n")
            if len(field) != len(fileSpecs):
                print("Error! Input file and selected format do not match\n")
                err = "Input file has " + str(len(field)) + " fields but should have " + str(len(fileSpecs)) + " fields."
                print(err)
                break
            for i in range(0,len(field)):
                if choice == "E" and i > 6:
                    newline = newline + makeItFit(field[i],fileSpecs[i],"0")
                elif choice == "ERSS" or choice == "ESP":
                    newline = newline + makeItFit(field[i],fileSpecs[i],"space")                
                elif field[i].isdigit():
                    newline = newline + makeItFit(field[i],fileSpecs[i],"0")
                else:
                    newline = newline + makeItFit(field[i],fileSpecs[i],"space")
            #print(newline)
            docout.write(newline)
            row = row + 1
        linecount = linecount + 1
        
    print("Data saved to file " + outfile + " in the current directory.\n")

runProgram = "Y"
while runProgram == "Y" or runProgram == "y":
    choice = menu()
    getFile(choice)
    runProgram = input("Process another file? Y/N \n")
print("Goodbye\n")

