# coding: utf-8
import threading, subprocess, time, os, json
from sys import exit, stdout, argv

VERSION = '2.21'
if len(argv) > 1:
    if 'version' in argv[1]:
        print('PythonPipe UCI AutoLogger & Engine Controller')
        print('By Rain rainydew@qq.com Version %s' % VERSION)
    elif 'help' in argv[1]:
        print('setting.txt to set which program to run and which file to log')
        print('example:')
        print('  stockfish.exe')
        print('  log.txt')
        print('sometimes engine will disconnect because of ending mode autodetect result not stable')
        print('you can make a file named force.txt')
        print('and write lf/crlf/cr in it to force it to use specified end')
        print('usually BugChess needs Lf')
        print('any engines unexpect disconnect reports to rainydew@qq.com')
    exit(0)


def getcommon():
    try:
        f = open('../state.txt', 'r')
    except:
        f = open('../state.txt', 'w')
        f.write('False')
        f.flush()
        f.close()
        f = open('../state.txt', 'r')
    g = eval(f.read())
    f.close()
    return g


def addone():
    try:
        f = open('games.txt', 'r')
    except:
        js = {'match': True, 'count': 0}
        p = json.dumps(js)
        f = open('games.txt', 'w')
        f.write(p)
        f.flush()
        f.close()
        f = open('games.txt', 'r')
    js = json.loads(f.read())
    f.close()
    if js['match']:
        js['count'] += 1
    else:
        js['count'] -= 1
        if js['count'] == 0:
            js['match'] = True
    f = open('games.txt', 'w')
    f.write(json.dumps(js))
    f.flush()
    f.close()
    if js['count'] == 0:
        js['match'] = False
    return js  # The return value here is very important. If it's True, the game will continue otherwise be skipped


def quitCheck():
    try:
        f = open('games.txt', 'r')
    except:
        return True
    else:
        js = json.loads(f.read())
        f.close()
        if not js['match']:
            js['count'] -= 1
            if js['count'] == 0:
                js['match'] = True
            f = open('games.txt', 'w')
            f.write(json.dumps(js))
            f.flush()
            f.close()
            return False
        else:
            return True


try:
    f = open('setting.txt', 'r')
except:
    print(
        'configuration file setting.txt not found. The first line here should be console program and the second line should be the logfile')
    time.sleep(5)
    exit(-1)
conf = f.readlines()
try:
    assert len(conf) == 2
except:
    if len(conf) < 2:
        print(
            'Parse config failed. The first line here should be console program and the second line should be the logfile')
        exit(-1)

f.close()
conf = [x.replace('\n', '') for x in conf]

f = open(conf[1], 'a')
f.write('<pipe start...' + time.ctime() + '\r\n')
f.flush()

waiter = True

getuci = False  # We open stdin pipe of this program after engine responses
opbuff = []
ucitogui = False
guiSendStop = False  # True if GUI send stop command to engine. Usually connection stalls


def killsub(s):
    """
    :param subprocess.Popen s:
    :return:
    """
    global f
    if s.poll() is None:
        pid = s.pid
        try:
            f.write('<WARN engine cannot exit and will be forced to close\r\n')
            f.flush()
        except:
            pass
        while s.poll() is None:
            os.system('taskkill /pid %d /f>nul' % pid)
            os.system('taskkill /im %s /f>nul' % conf[0])
            time.sleep(1)
    try:
        f.close()  # Only work if s.poll() is not None, or program will be terminated by watchdog before reaching here.
    except:
        pass


def blockData(chan):
    global f, waiter, getuci, opbuff, ucitogui, guiSendStop
    mainSendUci=False
    while waiter:
        line = chan.stdout.readline().replace('\r', '').replace('\n', '')
        if line:
            if getuci:
                if line[:7] == 'option ':
                    if mainSendUci:
                        continue
                    if not ucitogui:
                        ucitogui = True

                stdout.write(line + '\n')
                if line[:5] == 'uciok':
                    mainSendUci=True
                stdout.flush()
                f.write(line + '\r\n')
                f.flush()
                if guiSendStop:
                    if line[:8] == 'bestmove':
                        guiSendStop = False

            else:
                if 'uciok' in line:
                    getuci = True
                elif line[:7] == 'option ':
                    opbuff.append(line)
                else:
                    f.write('# '+line + '\r\n')
                    f.flush()

safeQuit=False

def watchdog(chan):
    global waiter, f, getuci, opbuff, ucitogui, safeQuit
    while getuci == False and (chan.poll() is None):
        time.sleep(0.1)
    tm = time.time()
    while ucitogui == False and time.time() < tm + 2:
        time.sleep(0.1)
    if not ucitogui:
        for x in opbuff:
            stdout.write(x + '\n')
            stdout.flush()
            f.write(x + '\r\n')
            f.flush()
        stdout.write('uciok\n')
        stdout.flush()
        f.write('uciok\r\n')
        f.flush()

    # now we start
    while waiter and (chan.poll() is None):
        time.sleep(1)
    os.system('taskkill /im cmd.exe /f>nul')  # With ensuring program to exit, kill extra commandline processes
    if not safeQuit:  # Work if engine exits but GUI doesn't send quit command.
        # If this variable is ignored, pipe may disconnect to GUI (=engine disconnect) due to suspicious crash by engine
        f.write('<WARN pipe disconnected by foreign program\r\n')
        f.flush()
    waiter = False
    f.close()
    pid = os.getpid()
    os.system('taskkill /pid %d /f>nul' % pid)  # 这里是线程内，exit(0)不起作用，只能用命令行杀掉自己


switch = getcommon()  # If here occurs an error, we don't need to open a child process. So keep this line here

if os.path.exists('../pause.lock'):  # The lock before a child process start
    while 'cutechess.exe' in os.popen('tasklist | find "cutechess.exe"').read():
        os.system('taskkill /im cutechess.exe /f>nul')
        time.sleep(2)
    exit(0)

try:
    s = subprocess.Popen(conf[0], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
except:
    stdout.write('info string application execute failed...\n')
    stdout.flush()
    f.write('<ERROR application cannot start\r\n')
    f.flush()
    f.close()
    exit(-2)
else:
    f.write('<application start...' + time.ctime() + '\r\n')
    f.flush()

t = threading.Thread(target=blockData, args=(s,))
w = threading.Thread(target=watchdog, args=(s,))
t.setDaemon(True)
w.setDaemon(True)
t.start()
w.start()

time.sleep(0.8)  # Very important, wait stdin of the child process ready
s.stdin.write('uci\r\n')
s.stdin.flush()
tm = time.time()
while time.time() < tm + 2 and getuci == False:
    time.sleep(0.1)
if getuci:
    end = '\r\n'
    f.write('<ending mode is CrLf\r\n')
    f.flush()
else:
    end = '\n'
    s.stdin.write('\n')
    s.stdin.flush()
    s.stdin.write('uci\n')
    s.stdin.flush()
    while time.time() < tm + 5 and getuci == False:
        time.sleep(0.1)
    if getuci:
        f.write('<ending mode is Lf\r\n')
        f.flush()

try:
    ff=open('force.txt')
    fs=ff.read().replace('\r','').replace('\n','').lower()
    ff.close()
    end={'crlf':'\r\n','lf':'\n','cr':'\r'}[fs]
    f.write('<ending mode forced change by file, now %s\r\n'%fs)
    f.flush()
    s.stdin.write(end)
    s.stdin.flush()
except:
    pass


if switch:
    checkStatus = True
    while waiter:
        buf = raw_input('') + end
        if checkStatus:
            try:
                buf3 = buf[:3]
            except:
                pass
            else:
                if buf3 == 'go ':
                    checkStatus = False
                    if not addone()['match']:
                        # Game needs to be skipped
                        stdout.write('bestmove a8a8\n')
                        stdout.flush()
                        f.write('<match will be skipped\r\n')
                        f.flush()
                        s.stdin.write('quit' + end)
                        s.stdin.flush()
                elif buf3 == 'qui':
                    if not quitCheck():
                        f.write('<match will be skipped after opponent pipe close\r\n')
                        f.flush()
        try:
            s.stdin.write(buf)
            s.stdin.flush()
            f.write('>' + buf)
            f.flush()
        except:
            time.sleep(3)
            break
        finally:
            buf4 = buf[:4]
            if buf4 == 'quit':
                safeQuit = True
                time.sleep(0.8)  # If engine exits here successfully we don't need to call killsub
                killsub(s)
                exit(0)
            elif buf4 == 'stop':
                guiSendStop = True
                time.sleep(1)
                if guiSendStop:
                    f.write('<WARN engine seems no response\r\n')
                    f.flush()
                    killsub(s)
                    exit(0)

else:  # Better performance if switch is off
    while waiter:
        buf = raw_input('') + end
        try:
            s.stdin.write(buf)
            s.stdin.flush()
            f.write('>' + buf)
            f.flush()
        except:
            time.sleep(3)
            break
        finally:
            buf4 = buf[:4]
            if buf4 == 'quit':
                safeQuit = True
                time.sleep(0.8)
                killsub(s)
                exit(0)
            elif buf4 == 'stop':
                guiSendStop = True
                time.sleep(1)
                if guiSendStop:
                    f.write('<WARN engine seems no response\r\n')
                    f.flush()
                    killsub(s)
                    exit(0)
