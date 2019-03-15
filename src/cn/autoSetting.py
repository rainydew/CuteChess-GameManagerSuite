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
            print p+" 目录处理失败"
        else:
            c=open(p+"/setting.txt","w")
            c.write(f[0])
            c.write("\nlog.txt\n")
            c.flush()
            c.close()
            print p+" 目录自动配置成功"
    else:
        print p+" 目录已经配置，自动跳过"
raw_input("回车退出")