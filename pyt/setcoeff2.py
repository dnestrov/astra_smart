import sys
filename1='equ/log/'+sys.argv[1]
print (filename1)
file1 = open(filename1,'r') 
Lines = file1.readlines()
file1.close()
name=sys.argv[3]
count=0 
for line in Lines:
    ab="{}:".format(line.strip())
    if ab[0:len(name)+1] == sys.argv[3]+' ':
        Lines.remove(Lines[count])
        if len(name) == 3:
            space='    '
        if len(name) == 4:
            space='   '
        if len(name) == 5:
            space='  '
        if len(name) == 6:
            space=' '
        Lines.insert(count,sys.argv[3]+space+'=  '+sys.argv[4]+'\n')
        print (str(count)+' '+ab+'-->'+sys.argv[4])
    count=count+1

filename2='equ/log/'+sys.argv[2]
file2 = open(filename2,'w')
file2.writelines(Lines)
file2.close
