# coding=utf-8
import easygui,sys,os,re,json


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
    Compare two dictionaries
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

p=easygui.fileopenbox(msg='Choose a PGN file',title='Import games',filetypes=['*.pgn'])
if not p:
    sys.exit(0)
f=open(p,'r')
buf=f.readlines()
f.close()
pgn=sums([ takequote(x) for x in buf if '[White' in x or '[Black' in x ])
print('pgn file:')
print(pgn)

print('0.Check games count')
print('1.Repair games count (rewrite counting file based on PGN)')
ch=raw_input('Choose an option:')
if ch=='0':
    cm=os.popen('checkgames.bat').readlines()
    txt=parfold(cm)
    print('txt file:')
    print(txt)
    if pgn==txt:
        print('Compare done! All OK')
    else:
        print('The following count(s) are different, please check logfile to find out why')
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