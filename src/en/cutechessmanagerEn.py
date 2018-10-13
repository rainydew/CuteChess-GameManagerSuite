# coding: utf-8
import json,os
from sys import exit
from goto import with_goto

flocate=os.popen('echo %APPDATA%').read().replace('\n','').replace('\\','/').decode('gbk')+'/cutechess/'
ftmp=''

def gbkprint(x):
    print x

def jiebao(anyiter):
    buf=[]
    [ buf.extend(x) for x in anyiter ]
    return buf


try:
    f=open(ftmp+'engines.json','r')
except:
    try:
        ftmp=flocate
        f = open(ftmp+'engines.json', 'r')
    except:
        print("Cannot find engines'configure file. Rerun cutechess.exe can solve it.")
        exit(1)

j=f.read()
f.close()
jdict=json.loads(j)


def takeval(val):
    try:
        val = int(val)
    except:
        if val.lower() == 'true':
            val = True
        elif val.lower() == 'false':
            val = False
        else:
            val = unicode(val)
    return val


def savefile(r):
    '''
    :param str r:
    :return:
    '''
    r=r.replace('\n','\r\n')
    i=0
    while os.path.exists(ftmp+'engines(%i).json'%i):
        i=i+1
    os.rename(ftmp+'engines.json',ftmp+'engines(%i).json'%i)
    f=open(ftmp+'engines.json','w')
    f.write(r)
    f.write('\r\n')
    f.flush()
    f.close()
    print('Files saved and backuped successfully.')
    if ftmp!='':
        print('The directory is:')
        print(ftmp)


def queryPro(elist):
    '''    :param list elist:
    :return:
    '''
    odict={0:'command',1:'protocol',2:'workingDirectory'}
    [ gbkprint(str(x)+'.'+odict[x]) for x in odict.keys() ]
    print('3.All engine properties')
    print('4.Back to main menu')
    cg = int(raw_input('Choose an option:'))

    if cg==4:
        return
    elif cg==3:
        [ gbkprint(x['name'] + ':\n' + '\n'.join([ '\t'+y+' '+x[y] for y in x.keys() if y!='name' and y!='options' and y!='stderrFile' ]) ) for x in elist ]
    else:
        [ gbkprint(x['name']+' '+odict[cg]+' '+x[odict[cg]]) for x in elist ]

@with_goto
def queryOpt(elist):
    '''    :param list elist:
    :return:
    '''
    edict={ x['name']:x['options'] for x in elist }
    oset=tuple({ x['name'] for x in jiebao(edict.values()) }) # inner is set while outer is dict
    otup={oset.index(x):x for x in oset}
    [ gbkprint(str(x) + '.' + otup[x]) for x in otup.keys() ]
    print( str(len(otup))+'.All engine settings' )
    print( str(len(otup)+1)+'.Back to main menu' )
    print( str(len(otup)+2) + '.Search setting number by name')

    label .cg2
    cg = int(raw_input('Choose an option:'))
    if cg==len(otup)+1:
        return
    elif cg==len(otup)+2:
        sc=raw_input('Full or part of the setting name (case is not sensitive):')
        print('Searching result:')
        [ gbkprint(str(x) + '.' + otup[x]) for x in otup.keys() if sc.lower() in otup[x].lower() ]
        goto .cg2
    elif cg==len(otup):
        [ gbkprint(x['name'] + ':\n' + '\n'.join([ '\t'+y['name']+' '+unicode(y['value']) for y in x['options'] if y.has_key('value') ]) ) for x in elist ]
    else:
        try:
            [ gbkprint(x['name']+'\t'+ (lambda z: 'Unsupported' if z=='' else z)(''.join([ y['name']+'\t'+unicode(y['value']) for y in x['options'] if y['name']==otup[cg] ])) ) for x in elist ]
        except:
            print('Nothing to display')

def setPro(engcho,fread):
    '''
    :param list elist:
    :return:
    '''
    odict={0:'command',1:'protocol',2:'workingDirectory'}
    [ gbkprint(str(x)+'.'+odict[x]) for x in odict.keys() ]
    print('3.Back to main menu')
    cg = int(raw_input('Choose an option:'))

    if cg==3:
        return
    else:
        val=takeval(raw_input('Input a value for this parameter:'))
        if type(val)==type('a'):
            try:
                val=unicode(val)
            except:
                pass

        if len(engcho)==1:
            engcho=engcho[0]
            fread[engcho][odict[cg]]=val
        else:
            for i in engcho:
                fread[i][odict[cg]]=val

        r = json.dumps(fread, indent=4, ensure_ascii=False)
        print(r)
        savefile(r)

@with_goto
def setOpt(engcho,fread):
    if len(engcho)==1:
        elist=[fread[engcho[0]]]
    else:
        elist=fread
    edict={ x['name']:x['options'] for x in elist }
    oset=tuple({ x['name'] for x in jiebao(edict.values()) }) # inner is set while outer is dict
    otup={oset.index(x):x for x in oset}
    [ gbkprint(str(x) + '.' + otup[x]) for x in otup.keys() ]
    print( str(len(otup))+'.Back to main menu' )
    print( str(len(otup)+1)+'.Search setting number by name' )
    label .cg1
    cg = int(raw_input('Choose an option:'))

    if cg==len(otup):
        return
    elif cg==len(otup)+1:
        sc=raw_input('Full or part of the setting name (case is not sensitive):')
        print('Searching result:')
        [ gbkprint(str(x) + '.' + otup[x]) for x in otup.keys() if sc.lower() in otup[x].lower() ]
        goto .cg1
    else:
        cgs=[ x for x in range(len(otup)) if otup[x].lower()==otup[cg].lower() ]  # 这样可以忽略大小写
        print('Auto merge these same items with different cases：'+str(cgs))
        val = takeval(raw_input('Input a value for this parameter:'))
        if type(val)==type('a'):
            try:
                val=unicode(val)
            except:
                pass

        for cg in cgs:
            for i in engcho:
                opt={ x['name']:[ x['value'] , (lambda y: (y['min'],y['max']) if y.has_key('min') and y.has_key('max') else None)(x) ] for x in fread[i]['options'] if x.has_key('value') }
                try:
                    opt=opt[otup[cg]]
                except:
                    print('warning setting not found in engine %d'%i)
                    continue
                rk = [x['name'] for x in fread[i]['options']].index(otup[cg])
                if opt[1] is not None:
                    if val<opt[1][0]:
                        print('warning engine %d adjust from %d to %d because of minvalue'%(i,val,opt[1][0]))
                        sval=opt[1][0]
                    elif val>opt[1][1]:
                        print('warning engine %d adjust from %d to %d because of maxvalue'%(i,val,opt[1][1]))
                        sval=opt[1][1]
                    else:
                        sval=val
                else:
                    sval=val
                fread[i]['options'][rk]['value']=sval

        r = json.dumps(fread, indent=4, ensure_ascii=False)
        print(r)
        savefile(r)


@with_goto
def main(ch):
    ch=int(ch)

    if ch==1:
        # queries
        label .ch1
        print('\n'.join([str(jdict.index(en))+'.\t'+en['name'] for en in jdict]))
        print(str(len(jdict))+'.\tAll engines')
        print(str(len(jdict)+1)+'.\tGo back')
        cg=int(raw_input('Choose an engine or all:'))
        if cg==len(jdict)+1:
            return
        elif cg==len(jdict):
            englist=jdict
        else:
            englist=[jdict[cg]]
        print('0.Engine UCI settings')
        print('1.Engine properties')
        print('2.Go back')
        cf=int(raw_input('Choose an item:'))
        if cf==2:
            goto .ch1
        elif cf==1:
            queryPro(englist)
        elif cf==0:
            queryOpt(englist)

    elif ch==2:
        # 修改
        label .ch2
        print('\n'.join([str(jdict.index(en))+'.\t'+en['name'] for en in jdict]))
        print(str(len(jdict))+'.\tMerging modify (recommanded)')
        print(str(len(jdict)+1)+'.\tGo back')
        cg=int(raw_input('Choose an engine or all engines that have this option to modify:'))
        if cg==len(jdict)+1:
            return
        elif cg==len(jdict):
            engcho=list(range(cg))
        else:
            engcho=[cg]
        print('0.Engine UCI settings')
        print('1.Engine properties')
        print('2.Go back')
        cf=int(raw_input('Choose an item:'))
        if cf==2:
            goto .ch2
        elif cf==1:
            setPro(engcho,jdict)
        elif cf==0:
            setOpt(engcho,jdict)

    elif ch==3:
        print('0.Go back')
        print('1.All Hash to 512MB')
        print('2.All Hash to 1024MB')
        print('3.All Threads/CPUs/Cores to 2')
        print('4.All Threads/CPUs/Cores to 4')
        print('5.All Threads/CPUs/Cores to 8')
        print('6.Set syzygy path for all engines support this')
        print('Function developing, not available now')
    elif ch==0:
        exit(0)
    else:
        print('Invalid input')

while True:
    print('cuteChess engine configuring tool 1.1')
    print('Author Rainy, thanks to Kinloo/Vara')
    print('0.Exit')
    print('1.Query engine settings')
    print('2.Modify engine settings')
    print('3.Fast channel (not available now)')
    ch=raw_input('Choose an item:')
    try:
        main(ch)
    except Exception,e:
        print('Opps, an error occurred, coding here:')
        print(e.message)
        raw_input('press enter to exit')
        raise
