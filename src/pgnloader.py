# coding=utf-8
import easygui,sys,os,re,json
def gbkprint(statement):
    try:
        print(str(statement).decode('utf-8').encode('gbk'))
    except:
        print(str(statement))

def takequote(x):
    '''
    :param str x:
    :return:
    '''
    return re.sub(string=x[x.find('"')+1:x.rfind('"')],pattern='[0-9|.].*$',repl='').lower()

def sums(glist):
    '''
    :param list glist:
    :return dict:
    '''
    di={}
    for x in glist:
        if x in di.keys():
            di[x]+=1
        else:
            di[x]=1
    return di

def parfold(clist):
    '''
    :param list clist
    :return:
    '''
    ecdict={}
    gmdict={}
    rtdict={}
    for x in clist:
        if x[0]=='{':
            fs=x.partition('}')
            fs=fs[0]+fs[1]
        else:
            fs=x.partition(' ')[0]
        eng=x.split('\\')[-2].lower()
        if fs[0]=='{':
            ecdict[eng]=json.loads(fs)
        else:
            gmdict[eng]=int(fs)
    for x in ecdict.keys():
        if x not in gmdict.keys():
            gmdict[x]=0
        if ecdict[x]['match']==True:
            rtdict[x]=ecdict[x]['count']+gmdict[x]
        else:
            rtdict[x]=gmdict[x]
    return rtdict

def dictdiff(di1,di2,di1name,di2name):
    '''
    :param dict di1:
    :param dict di2:
    :param str di1name:
    :param str di2name:
    :return None:
    比较两个字典的区别
    '''
    cpr={}
    for x in di1.keys():
        cpr[x]={di1name:di1[x]}
    for x in di2.keys():
        if x in di1.keys():
            cpr[x][di2name]=di2[x]
        else:
            cpr[x]={di2name:di2[x]}
    for x in cpr.keys():
        if len(cpr[x])<2:
            print(x+' '+str(cpr[x]))
        elif cpr[x][di1name]!=cpr[x][di2name]:
            print(x+' '+str(cpr[x]))

p=easygui.fileopenbox(msg='请选择PGN文件',title='导入棋谱',filetypes=['*.pgn'])
if not p:
    sys.exit(0)
f=open(p,'r')
buf=f.readlines()
f.close()
pgn=sums([ takequote(x) for x in buf if '[White' in x or '[Black' in x ])
print('pgn file:')
print(pgn)

gbkprint('0.核对场次')
gbkprint('1.修复场次')
ch=raw_input('请选择：'.decode('utf-8').encode('gbk'))
if ch=='0':
    cm=os.popen('checkgames.bat').readlines()
    txt=parfold(cm)
    print('txt file:')
    print(txt)
    if pgn==txt:
        gbkprint('比较无误！')
    else:
        gbkprint('以下场次有差异，请从棋谱和日志核实原因')
        dictdiff(pgn,txt,'pgn','txt')

elif ch=='1':
    dd='../Engines/'
    h=[ dd+x for x in os.listdir(dd) if os.path.isdir(dd+x) ]
    for x in h:
        buf=x.rpartition('/')[2].lower()
        if buf in pgn.keys():
            f=open('%s/games.txt'%x,'w')
            f.write(json.dumps({'match':False,'count':pgn[buf]}))
            f.flush()
            f.close()
            f=open('%s/totalgames.txt'%x,'w')
            f.write(str(pgn[buf]))
            f.flush()
            f.close()
raw_input('enter to exit')