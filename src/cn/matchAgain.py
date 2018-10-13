# coding:utf-8
import json,os,sys,time
import traceback
# version 1.3
def gbkprint(statement):
    try:
        print(statement.decode('utf-8').encode('gbk'))
    except:
        print(statement)

def getTotal(dir):
    allPath = dir + '/totalgames.txt'
    try:
        g=open(allPath,'r')
        buf = int(g.read())
    except:
        g=open(allPath,'w')
        g.write('0')
        g.flush()
        g.close()
        g = open(allPath, 'r')
        buf = int(g.read())
    g.close()
    return buf

def setTotal(dir,setNo):
    allPath = dir + '/totalgames.txt'
    g=open(allPath,'w')
    g.write(str(setNo))
    g.flush()
    g.close()

def matchAgain(dir,setTo=False):
    allPath=dir+'/games.txt'
    try:
        f=open(allPath, 'r')
    except:
        print dir+' not found'  # if we cannot find it then we skip it
    else:
        js=json.loads(f.read())
        f.close()
        try:
            if js['match']==True and setTo==False:
                # 这时候需要把我们总的比赛场次缓存到totalGames.txt文件内，每次从true切换为false也就是接续比赛时，要读取本次比赛之前计数的totalcounts总数并且赋值回来
                # 这样才可以中断两次或更多的比赛
                js['count']+=getTotal(dir)
                setTotal(dir,js['count'])
            js['match']=setTo
            if setTo:
                js['count']=0
        except:
            traceback.print_exc(file=sys.stdout)
            print 'warning %s/games.txt broken!'%dir
            os.remove(allPath)
            print 'broken file deleted, run another match to repair'
        else:
            f=open(allPath, 'w')
            f.write(json.dumps(js))
            f.close()
            print '%s done!'%dir
    if setTo:
        try:
            os.remove(dir+'/totalgames.txt')
        except:
            pass

if __name__=='__main__':
    gbkprint('比赛管理工具1.4 by Rain')
    gbkprint('0.比赛被中止，我需要接续之前的比赛')
    gbkprint('1.比赛被中止或已结束，我需要重新开始新的比赛')
    gbkprint('2.开启比赛模式(记录盘数和重赛功能)')
    gbkprint('3.关闭比赛模式(所有管道将只转发引擎通信而不再干预，下一半而中断的棋请单独使用此模式补赛后再开启比赛模式)')
    gbkprint('4.比赛上暂停锁，上锁后，界面将在当前比赛打完后退出，随后锁自动删除')
    op=raw_input('choose an option(0~4):')
    if op=='2':
        f = open('state.txt', 'w')
        f.write('True')
        f.flush()
        f.close()
        gbkprint('比赛模式已开启，按回车退出程序')
        raw_input('')
        sys.exit(0)
    elif op=='3':
        f = open('state.txt', 'w')
        f.write('False')
        f.flush()
        f.close()
        gbkprint('比赛模式已关闭，按回车退出程序。若您是为了补赛，补赛完成后记得重新开启比赛模式')
        raw_input('')
        sys.exit(0)
    elif op=='1':
        st=True
    elif op=='0':
        st=False
    elif op=='4':
        open('pause.lock','w').close()
        gbkprint('比赛已上锁，当前正在进行的比赛会继续进行到完成。请勿关闭当前程序，待该比赛结束后本程序会自行退出。想要接续比赛，请重新打开此程序，选择0回车后即可')
        while 'cutechess.exe' in os.popen('tasklist | find "cutechess.exe"').read():
            time.sleep(2)
        os.remove('pause.lock')
        sys.exit(0)
    else:
        gbkprint('输入错误，按回车退出')
        raw_input('enter to quit')
        sys.exit(1)
    [ matchAgain(x,st) for x in os.listdir(os.getcwd()) if os.path.isdir(x) ]
    raw_input('all done, press enter to exit')
