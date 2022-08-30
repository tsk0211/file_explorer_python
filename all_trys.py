from os import walk

print("VALk" in "VALORENT.lnk")

'''
f = walk("D:\\Updated\\File_Explorer_By_Tushar")
yl=[]
fl=[]
path_l = []
path_e = []

for X, Y, Z in f :
    for d in Y :
        if len(d) > 0 :
            path_e.append(X + "\\" + d)
            yl.append(d)

    for s in Z :
        path_l.append(X + "\\" + s)
        fl.append(s)

for i in range(len(yl)) :
    print(yl[i] + "  |  " + path_e[i])

for i in range(len(fl)) :
    print(fl[i] + "  |  " + path_l[i])

for x, y, z in f :
    yl.append(y)
    for d in z :
        print(d + "   ::-->>  " + x+"\\"+d)

print("\n\nSub-Folders\n")
for c in yl :
    for d in c :
        if len(d) >0 :
            print(d)
'''