def readfile():
    inp_file = open("50sudoku.txt","r")
    lines = inp_file.readlines()
    inp_file.close()
    #new_file = open("sample.txt","w+")
    count = 0
    for i,line in enumerate(lines):
            #print i
            if line[:4] == "Grid":
                new_file = open("%s.txt"%str(line.strip()),"w+")
            else:
                count+=1
                new_file.write(line)



if __name__ == '__main__':
    readfile()
