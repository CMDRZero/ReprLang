import random
import pickle
import os

def tobin(tree,path=""):
    if type(tree)!=tuple:
        return({tree:path})
    d={}
    d.update(tobin(tree[0],path+"0"))
    d.update(tobin(tree[1],path+"1"))
    return(d)
def decode(val,tree):
    ctree=tree
    o=""
    for v in val:
        ctree=ctree[int(v)]
        if type(ctree)!=tuple:
            o+=ctree
            ctree=tree
    return(o)
def rlencode(val,tree):
    o=''
    while val!="":
        for key in tree.keys():
            if len(key)<=len(val):
                if val[:len(key)]==key:
                    o+=tree[key]
                    val=val[len(key):]
                    break
        else:
            raise IndexError(f"Character {repr(val[0])} does not have an encoding")
    return(o)
def rrlencode(val,treeo):
    tree=dict(sorted([(key,treeo[key]) for key in treeo],key=lambda e:-len(e[0]),reverse=True))
    o=''
    while val!="":
        for key in tree.keys():
            if len(key)<=len(val):
                if val[:len(key)]==key:
                    o+=tree[key]
                    val=val[len(key):]
                    break
        else:
            raise IndexError(f"Character {repr(val[0])} does not have an encoding")
    return(o)
def annotcode(val,tree):
    o=[]
    while val!="":
        for key in tree.keys():
            if len(key)<=len(val):
                if val[:len(key)]==key:
                    o.append([tree[key],repr(key)])
                    val=val[len(key):]
                    break
        else:
            raise IndexError(f"Character {repr(val[0])} does not have an encoding")
    r1=""
    r2=""
    for e,k in o:
        ml=max(len(e),len(k))+1
        r1+=e+" "*(ml-len(e))
        r2+=k+" "*(ml-len(k))
    print(r1)
    print(r2)

def fullcode(token):
    print("-"*100)
    ov=0
    for i in range(0,len(token)):
        v=int(100*(i/len(token)))
        if v>ov:
            ov=v
            print("-",end="")
##        if i%10==0:
##            print()
        m=""
        for j in range(len(token)-i):
            if token[j]==token[j+i]:
                m+="x"
            else:
                m+='-'
        buf=""
        for i in range(len(token)-i):
            if m[i]=='x':
                buf+=token[i]
            else:
                tkss[buf]=token.count(buf)
                buf=""
        tkss[buf]=token.count(buf)
    print("-")
    for j in range(len(token)-1):
        ss=token[j]
        tkss[ss]=token.count(ss)
    del tkss['']

    tks=tkss.copy()
    while len(tks)>1:
        key=list(tks.keys())[list(tks.values()).index(min(tks.values()))]
        n1,v1=(key,tks.pop(key))
        key=list(tks.keys())[list(tks.values()).index(min(tks.values()))]
        n2,v2=(key,tks.pop(key))
        tks[(n1,n2)]=v1+v2
    tree=list(tks.keys())[0]
    bintree=tobin(tree)
    bintree=dict(sorted([(key,bintree[key]) for key in bintree],key=lambda e:-len(e[0])))#Sort dict by length of key longest being first
    return(tkss,tree,bintree)

def tmark(txt,tks):
    o={}
    for tk in tks:
        for i in range(len(txt)-len(tk)):
            if txt[i:i+len(tk)]==tk:
                d=o.get(tk,{})
                ttks=ftk(txt[i+len(tk):],tks)
                for ttk in ttks:
                    d[ttk]=1+0*len(ttk)+d.get(ttk,0)
                o[tk]=d
    return(o)
def gen(d,s=100,seed=None):
    o=''
    if seed==None:
        seed=list(d.keys())[0]
    for i in range(s):
        o+=seed
        ops=d[seed]
        seed=random.choices(list(ops.keys()),map(lambda e:e,list(ops.values())))[0]
    return(o)
def ftk(txt,tks):
    o=set()
    l=0
    for tk in tks:
        if txt[:len(tk)]==tk:
##            o.add(tk)
            if len(tk)>l:
                o=set([tk])
                l=len(tk)
    return(list(o))
def tmark2(txt,tks):
    o={}
    for tk1 in tks:
        for i in range(len(txt)-len(tk1)):
            if txt[i:i+len(tk1)]==tk1:
                d1=o.get(tk1,{})
                for tk2 in tks:
                    if tk1 != tk2:
                        for j in range(i+len(tk1), len(txt)-len(tk2)):
                            if txt[j:j+len(tk2)]==tk2:
                                d2=d1.get(tk2,{})
                                ttks=ftk(txt[j+len(tk2):],tks)
                                for ttk in ttks:
                                    d2[ttk]=1+0*len(ttk)+d2.get(ttk,0)
                                d1[tk2] = d2
                o[tk1]=d1
    return(o)
def analyze():
    for key,v in sorted([(key,tkss[key]) for key in tkss],key=lambda e:e[1])[::-1]:
        print(repr(key),v,bintree[key])
def ana2():
    for key,v in sorted([(key,tkss[key]) for key in tkss],key=lambda e:e[1])[::-1]:
        ll=len(rrlencode(key,bintree))
        l2=len(bintree[key])
        if l2>ll:
            print(repr(key),v,l2,ll)
def irgen(s=100):
    return(decode(bin(random.randint(0,2**s-1))[2:],tree))
def test(v,tree,n):
    cc=rlencode(v,tree)
    print(f"Original length: {len(v)} chars")
    print(f"New length: {len(cc)} chars")
    print(f"Bits per sym: {round(len(cc)/len(v),3)}")
    print(f"{round(100*len(cc)/len(v)/n,1)}% of Nieve Size")

def funky(txt,x):
    global tkn,reps
    reps=[]
    tkn=txt
    rx=0
    for i in range(x):
        fin=b[i][1]
        rfin=fin
        rep=findfree(tkn)
        for r in reps:
            fin=fin.replace(r[0],r[1])
        if fin in tkn and len(rep)<len(fin):
            reps.append([fin,rep])
            tkn=tkn.replace(fin,rep)
            rx+=1
    return rx
def apfun(txt,verb=True):
    c=txt
    for r in reps:
        txt=txt.replace(r[0],r[1])
        if txt!=c:
            c=txt
            if verb:
                print(f"{repr(r[0])} -> {repr(r[1])} :: {repr(txt)}")

def findfree(txt):
    stk=[0]
    x=None
    while x==None:
        x="".join([sym[i] for i in stk])
        if x in txt:
            x=None
        i=0
        stk[i]+=1
        while stk[i]==len(sym):
            stk[i]=0
            i+=1
            if i==len(stk):
                stk.append(-1)
            stk[i]+=1
    return x

def defunky(x,verb=True):
    tkn2=x
    c=tkn2
    for r in reps[::-1]:
        tkn2=tkn2.replace(r[1],r[0])
        if tkn2!=c:
            c=tkn2
            if verb:
                print(f"{repr(r[1])} -> {repr(r[0])} :: {repr(tkn2)}")
    return tkn2

filename='egfile4'

if os.path.exists('replang_'+filename+'.pkl'):
    with open('replang_'+filename+'.pkl',"rb") as f:
        token,tkss,tree,bintree,dd=pickle.load(f)
    a=[((len(x)-1)*tkss[x],x) for x in list(tkss.keys())[1:]]
    b=sorted(a,key=lambda x:x[0])[::-1]
    sym=sorted('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM,./<>?;\':"[]\\{}|`1234567890-=~!@#$%^&*()_+')
else:
    with open(filename+'.txt',"r",encoding='utf-8') as f:
        token=f.read()

    tkss={}
    tkss,tree,bintree = fullcode(token)
    dd=tmark(token,tkss)

    with open('replang_'+filename+'.pkl',"wb") as f:
        pickle.dump((token,tkss,tree,bintree,dd),f)

##tkss={}
##
##with open("replang.pkl","rb") as f:
##    token,tkss,tree,bintree,dd=pickle.load(f)
##
##a=[((len(x)-1)*tkss[x],x) for x in list(tkss.keys())[1:]]
##b=sorted(a,key=lambda x:x[0])[::-1]
##sym=sorted('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM,./<>?;\':"[]\\{}|`1234567890-=~!@#$%^&*()_+')
##
##with open("egfile4.txt","r",encoding='utf-8') as f:
##    token=f.read()
##
##tkss,tree,bintree = fullcode(token)
##dd=tmark(token,tkss)
##
##with open("replang.pkl","wb") as f:
##    pickle.dump((token,tkss,tree,bintree,dd),f)


