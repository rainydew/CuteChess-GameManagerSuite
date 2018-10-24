# coding: utf-8
import threading,subprocess,time,os
from sys import exit,stdout
# version:1.0
try:
    f=open('setting.txt','r')
except:
    print('configuration file setting.txt not found. The first line here should be console program and the second line should be the logfile')
    time.sleep(5)
    exit(-1)
conf=f.readlines()
try:
    assert len(conf)==2
except:
    print('Parse config failed. The first line here should be console program and the second line should be the logfile')
    if len(conf)<2:
        time.sleep(5)
        exit(-1)

f.close()
conf=[x.replace('\n','') for x in conf]

f=open(conf[1],'a')
f.write('<pipe start...'+time.ctime()+'\r\n')
f.flush()

waiter=True

def blockData(chan):
    global f,waiter,use960
    while waiter:
        line=chan.stdout.readline().replace('\r','').replace('\n','')
        if line:
            stdout.write(line + '\n')
            stdout.flush()
            f.write(line+ '\r\n')
            f.flush()

def watchdog(chan):
    global waiter,f
    while waiter and (chan.poll() is None):
        time.sleep(5)
    print('pipe disconnected by foreign program')
    f.write('<WARN pipe disconnected by foreign program\r\n')
    f.flush()
    waiter=False
    f.close()
    pid=os.getpid()
    os.system('taskkill /pid %d /f>nul' % pid)

try:
    s=subprocess.Popen(conf[0],stdin=subprocess.PIPE,stdout=subprocess.PIPE,shell=False)
except:
    print('application execute failed...')
    f.write('<ERROR application cannot start\r\n')
    f.flush()
    f.close()
    exit(-2)

t=threading.Thread(target=blockData,args=(s,))
w=threading.Thread(target=watchdog,args=(s,))
t.setDaemon(True)
w.setDaemon(True)
t.start()
w.start()

while waiter:
    bufb=raw_input('')
    try:
        s.stdin.write(bufb+'\n')
        s.stdin.flush()
        f.write('>'+bufb+'\r\n')
        f.flush()
    except:
        time.sleep(1)
        break