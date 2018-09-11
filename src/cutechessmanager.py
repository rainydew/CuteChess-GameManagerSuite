# coding: utf-8
import json,os
from sys import exit
from goto import with_goto

flocate=os.popen('echo %APPDATA%').read().replace('\n','').replace('\\','/').decode('gbk')+'/cutechess/'
ftmp=''

Console=True
def gbkprint(statement,console=Console):
    if not console:
        print(statement)
        return

    if type(statement)==type(u'a'):
        try:
            print(statement.encode('gbk'))
        except:
            print(statement)
    else:
        try:
            print(str(statement).decode('utf-8').encode('gbk'))
        except:
            try:
                print(str(statement).encode('gbk'))
            except:
                try:
                    print(str(statement))
                except:
                    print(statement)

def gbkinput(statement,console=Console):
    if console:
        try:
            return raw_input(str(statement).decode('utf-8').encode('gbk')).decode('gbk').encode('utf-8')
        except:
            return raw_input(str(statement)).decode('gbk').encode('utf-8')
    else:
        try:
            return raw_input(statement).decode('gbk').encode('utf-8')
        except:
            return raw_input(statement)

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
        gbkprint('引擎配置文件找不到，请重新运行cutechess界面以修复问题')
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
    gbkprint('文件备份和保存成功')
    if ftmp!='':
        gbkprint('目录是：')
        print(ftmp)


def queryPro(elist):
    '''    :param list elist:
    :return:
    '''
    odict={0:'command',1:'protocol',2:'workingDirectory'}
    [ gbkprint(str(x)+'.'+odict[x]) for x in odict.keys() ]
    gbkprint('3.全部属性')
    gbkprint('4.返回主菜单')
    cg = int(gbkinput('请选择属性项:'))

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
    gbkprint( str(len(otup))+'.'+'全部设置项' )
    gbkprint( str(len(otup)+1)+'.'+'返回主菜单' )
    gbkprint( str(len(otup)+2) + '.' + '搜索编号')

    label .cg2
    cg = int(gbkinput('请选择属性项:'))
    if cg==len(otup)+1:
        return
    elif cg==len(otup)+2:
        sc=gbkinput('请输入你的搜索字符(不分大小写)')
        gbkprint('搜索结果：')
        [ gbkprint(str(x) + '.' + otup[x]) for x in otup.keys() if sc.lower() in otup[x].lower() ]
        goto .cg2
    elif cg==len(otup):
        [ gbkprint(x['name'] + ':\n' + '\n'.join([ '\t'+y['name']+' '+unicode(y['value']) for y in x['options'] if y.has_key('value') ]) ) for x in elist ]
    else:
        try:
            [ gbkprint(x['name']+'\t'+ (lambda z: u'不支持' if z=='' else z)(''.join([ y['name']+'\t'+unicode(y['value']) for y in x['options'] if y['name']==otup[cg] ])) ) for x in elist ]
        except:
            gbkprint('没有可以显示的设置项')

def setPro(engcho,fread):
    '''
    :param list elist:
    :return:
    '''
    odict={0:'command',1:'protocol',2:'workingDirectory'}
    [ gbkprint(str(x)+'.'+odict[x]) for x in odict.keys() ]
    gbkprint('3.返回主菜单')
    cg = int(gbkinput('请选择属性项:'))

    if cg==3:
        return
    else:
        val=takeval(gbkinput('请输入参数值'))
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
        gbkprint(r)
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
    gbkprint( str(len(otup))+'.'+'返回主菜单' )
    gbkprint( str(len(otup)+1)+'.'+'搜索编号' )
    label .cg1
    cg = int(gbkinput('请选择属性项:'))

    if cg==len(otup):
        return
    elif cg==len(otup)+1:
        sc=gbkinput('请输入你的搜索字符(不分大小写)')
        gbkprint('搜索结果：')
        [ gbkprint(str(x) + '.' + otup[x]) for x in otup.keys() if sc.lower() in otup[x].lower() ]
        goto .cg1
    else:
        cgs=[ x for x in range(len(otup)) if otup[x].lower()==otup[cg].lower() ]  # 这样可以忽略大小写
        gbkprint('已经自动合并处理大小写不同但名称相同的项：'+str(cgs))
        val = takeval(gbkinput('请输入参数值'))
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
                    gbkprint('warning setting not found in engine %d'%i)
                    continue
                rk = [x['name'] for x in fread[i]['options']].index(otup[cg])
                if opt[1] is not None:
                    if val<opt[1][0]:
                        gbkprint('warning engine %d adjust from %d to %d because of minvalue'%(i,val,opt[1][0]))
                        sval=opt[1][0]
                    elif val>opt[1][1]:
                        gbkprint('warning engine %d adjust from %d to %d because of maxvalue'%(i,val,opt[1][1]))
                        sval=opt[1][1]
                    else:
                        sval=val
                else:
                    sval=val
                fread[i]['options'][rk]['value']=sval

        r = json.dumps(fread, indent=4, ensure_ascii=False)
        gbkprint(r)
        savefile(r)


@with_goto
def main(ch):
    ch=int(ch)

    if ch==1:
        # 查询
        label .ch1
        gbkprint('\n'.join([str(jdict.index(en))+'.\t'+en['name'] for en in jdict]))
        gbkprint(str(len(jdict))+'.\t所有')
        gbkprint(str(len(jdict)+1)+'.\t返回上一级')
        cg=int(gbkinput('请选择引擎:'))
        if cg==len(jdict)+1:
            return
        elif cg==len(jdict):
            englist=jdict
        else:
            englist=[jdict[cg]]
        gbkprint('0.引擎设置项')
        gbkprint('1.引擎属性项')
        gbkprint('2.退回上一级')
        cf=int(gbkinput('请选择一项:'))
        if cf==2:
            goto .ch1
        elif cf==1:
            queryPro(englist)
        elif cf==0:
            queryOpt(englist)

    elif ch==2:
        # 修改
        label .ch2
        gbkprint('\n'.join([str(jdict.index(en))+'.\t'+en['name'] for en in jdict]))
        gbkprint(str(len(jdict))+'.\t统一修改(推荐)')
        gbkprint(str(len(jdict)+1)+'.\t返回上一级')
        cg=int(gbkinput('请选择引擎:'))
        if cg==len(jdict)+1:
            return
        elif cg==len(jdict):
            engcho=list(range(cg))
        else:
            engcho=[cg]
        gbkprint('0.引擎设置项')
        gbkprint('1.引擎属性项')
        gbkprint('2.退回上一级')
        cf=int(gbkinput('请选择一项:'))
        if cf==2:
            goto .ch2
        elif cf==1:
            setPro(engcho,jdict)
        elif cf==0:
            setOpt(engcho,jdict)

    elif ch==3:
        gbkprint('0.返回上一级')
        gbkprint('1.统一设置Hash为512MB')
        gbkprint('2.统一设置Hash为1024MB')
        gbkprint('3.统一设置线程数Threads/CPUs/Cores为2')
        gbkprint('4.统一设置线程数Threads/CPUs/Cores为4')
        gbkprint('5.统一设置线程数Threads/CPUs/Cores为8')
        gbkprint('6.统一设置syzygy残局库路径')
        gbkprint('快速设置功能开发中，暂不可用，敬请期待')
    elif ch==0:
        exit(0)
    else:
        gbkprint('输入错误')

while True:
    gbkprint('cuteChess引擎配置工具 1.1')
    gbkprint('作者 Rainy 鸣谢 Kinloo/Vara')
    gbkprint('0.退出')
    gbkprint('1.查询引擎配置')
    gbkprint('2.修改引擎配置')
    gbkprint('3.快捷选项(暂不可用)')
    ch=gbkinput('请选择:')
    try:
        main(ch)
    except Exception,e:
        gbkprint('系统出错了，代码如下:')
        gbkprint(e.message)
        raw_input('press enter to exit')
        raise
