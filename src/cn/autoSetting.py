# coding: gbk
# author: Rainy Chan
# version 1.01
import os,nt
dirs=[x for x in os.listdir(os.getcwd()) if nt._isdir(x)]
for p in dirs:
    st=os.listdir(p)
    if "setting.txt" not in st:
        f=[x for x in st if x[-4:]==".exe" and "pipe.exe" not in x]
        try:
            assert len(f)==1
        except:
            print p+" Ŀ¼����ʧ��"
        else:
            c=open(p+"/setting.txt","w")
            c.write(f[0])
            c.write("\nlog.txt\n")
            c.flush()
            c.close()
            print p+" Ŀ¼�Զ����óɹ�"
    else:
        print p+" Ŀ¼�Ѿ����ã��Զ�����"
raw_input("�س��˳�")