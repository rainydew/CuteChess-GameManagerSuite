# coding:utf-8
import json,os,sys,time
import traceback
# version 1.3


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
                # We need totalGames.txt to buffer the total games count for an engine. When we use this program to re-match, we need to read this file to find how many games it played
                # So we can re-match more than 2 times now
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
    print('Tournament Admin Tool 1.4 by Rain')
    print('0.Tournament paused, I need to resume')
    print('1.Tournament finished or cancelled, I need to start a new tournament')
    print('2.Switch RR mode on (enable game count recording and rematch function)')
    print('3.Switch RR mode off (all pipes only traffic communications between engines and GUI. Choose it if you have a game interrupted middleway and need to replay)')
    print('4.Enable a pause lock so GUI will terminate after current game ends. Then the lock will released automatically. Recommand to pause a tournament by this way')
    op=raw_input('choose an option(0~4):')
    if op=='2':
        f = open('state.txt', 'w')
        f.write('True')
        f.flush()
        f.close()
        print('RR mode enabled. Enter to exit')
        raw_input('')
        sys.exit(0)
    elif op=='3':
        f = open('state.txt', 'w')
        f.write('False')
        f.flush()
        f.close()
        print('RR mode disabled. Enter to exit. Re-enable it after critical game replayed during tournaments')
        raw_input('')
        sys.exit(0)
    elif op=='1':
        st=True
    elif op=='0':
        st=False
    elif op=='4':
        open('pause.lock','w').close()
        print("Tournament locked. All will exit after board finished so don't close me! To resume a tournament, open me again and choose 0")
        while 'cutechess.exe' in os.popen('tasklist | find "cutechess.exe"').read():
            time.sleep(2)
        os.remove('pause.lock')
        sys.exit(0)
    else:
        print('Invalid input, try again')
        raw_input('enter to quit')
        sys.exit(1)
    [ matchAgain(x,st) for x in os.listdir(os.getcwd()) if os.path.isdir(x) ]
    raw_input('all done, press enter to exit')
