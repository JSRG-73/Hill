# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 23:13:58 2019

@author: jorge
"""
from io import open
import math
from os import system

dt=dict={   ' ':0,'!':1,'"':2,'#':3,'$':4,'%':5,'&':6,"'":7,
            '(':8,')':9,'*':10,'+':11,',':12,'-':13,'.':14,'/':15, 
            
            '0':16,'1':17,'2':18,'3':19,'4':20,'5':21,'6':22,'7':23,'8':24,'9':25,
            
            ':':26,';':27,'<':28,'=':29,'>':30,'?':31,'@':32,
            
            'A':33,'B':34,'C':35,'D':36,'E':37,'F':38,'G':39,
            'H':40,'I':41,'J':42,'K':43,'L':44,'M':45,'N':46,
            'O':47,'P':48,'Q':49,'R':50,'S':51,'T':52,'U':53,
            'V':54,'W':55,'X':56,'Y':57,'Z':58,
            
            '^':59,'_':60,
            
            'a':61,'b':62,'c':63,'d':64,'e':65,
            'f':66,'g':67,'h':68,'i':69,'j':70,
            'k':71,'l':72,'m':73,'n':74,'o':75,
            'p':76,'q':77,'r':78,'s':79,'t':80,
            'u':81,'v':82,'w':83,'x':84,'y':85,'z':86,
            
            'ü':87,'ñ':88,'Ñ':89,'¿':90,'¡':91,'á':92,
            'é':93,'í':94,'ó':95,'ú':96,'Á':97,
            'É':98,'Í':99,'Ó':100,'Ú':101,'Ü':102,'{':103,
            '}':104,'[':105,']':106}


def unique_list(lst,n):      #converts lists inside lists in just one list.
    
    Ul=[]
    for i in range(len(lst)):
        for j in range(n):
            Ul.append(lst[i][j])
    return Ul
            

def size(lst):      #no sublists
    
    n=1
    while(True):    
        if len(lst)==n*n:
            return n
        else:
            n+=1


def module(lst):
    
    cont=0
    for i in lst:
        if i>len(dt) or i<0:
            lst[cont]=i%len(dt)
            cont+=1
        else:
            cont+=1
    return lst


def module_one(n):
    return n%len(dt)

def inverse_one(x):
    
    for i in range(len(dt)):
        if (x*i)%len(dt)==1:
            return i
        else:
            pass
        

def removeblankspace(string):
    
    string=string[::-1]
    cont=0
    for i in string:
        if i==' ':
            cont+=1
        else:
            break
    string=string[cont:]
    string=string[::-1]
    return string


def determinant(m,n):
    
    if n==1:
        return module_one(m[0][0])
    elif n==2:
        deter=(m[0][0]*m[1][1])-(m[0][1]*m[1][0])
        deter=math.ceil(deter)
        return module_one(deter)
    else:
        result=0
        i=m[0]        
        cj=0
        
        for j in i:
            aux=[]
            cx=0
            for x in m:
                cy=0
                for y in x:
                    if cx!=0 and cy!=cj: 
                        aux.append(y)
                    cy+=1
                cx+=1
                
            aux=sublist(aux,n-1)
            det=determinant(aux,n-1)
            sign=math.pow(-1,2+cj)
            index=m[0][cj]
            cj+=1
            result=result+(sign*det*index)
            result=math.ceil(result)

        return module_one(result)
    
    
def check_determinant(lst,n):
    
    det=determinant(lst,n)
    if det!=0:
        return True
    else:
        return False

def text_to_number(txt):
    
    listn=[]
    for i in txt:
        listn.append(dt[i])
    return listn           


def number_to_text(num): 
    
    listaux=[]
    result=""
    
    for i in num:
        for key,value in dt.items():
            if value==i:
                listaux.append(key)
    result=result.join(listaux)
    return result


def sublist(lst,n):   #for create lists inside lists.
    
    sub=[] ; result=[]
    for i in lst:
        sub.append(i)
        if len(sub)==n: 
            result+=[sub] 
            sub=[]
    if sub: result+=[sub]
    return result


def crypt(txt,key,n): #the core of the program.
    
    fila=[]
    res=[]

    for i in txt:
        for j in range(n):
            fila=key[j]
            suma=0
            for k in range(n):
                suma+=i[k]*fila[k]
            res.append(suma) 
            
    return module(res)     


def validate_password(pw):
    
    y=len(pw)
    n=0
    while (True):
        n+=1
        if y==pow(n,2):
            return pw
        elif y>n*n and y<(n+1)*(n+1):
            r=(n+1)*(n+1)-y
            break
    for i in range(r):
        pw.append(i*-1)
    return pw 


def validate_txt(txt,n):
    
    lentxt=len(txt)
    distance=int(lentxt%n)
    dist=n-distance
    
    if dist==0:
        return txt
    else:
        for i in range(dist):
            txt.append(0)
        return txt
   
    
def inverse(key,n): #sublisted key
    
    detkey=determinant(key,n)
    det_inv=inverse_one(detkey)
    Adj=[]
    At=key
    Af=key
    conti=0

    for i in key:
        contj=0
        for j in i:
            aux=[]
            contx=0
            for x in key:
                conty=0
                for y in x:
                    if conti!=contx and conty!=contj: 
                        aux.append(y)
                    conty+=1
                contx+=1
                        
            aux=sublist(aux,n-1)
            det=determinant(aux,n-1)
            sign=int(math.pow(-1,2+contj+conti))
            x=sign*det 
            Adj.append(x)
            contj+=1
        conti+=1 
        
    Adj=sublist(Adj,n)

    for i in range(n):
        for j in range(n):
            At[i][j]=Adj[j][i]
    
    for i in range(n):
        for j in range(n):
            Af[i][j]=module_one(At[i][j]*det_inv)
            
    sublist(Af,n)       
    return Af


def encrypt(txt,password):
    
    #Transform the text.
    txt=text_to_number(txt)
    key=text_to_number(password)
    
    #Fill strings.
    key=validate_password(key)
    n=size(key)
    txt=validate_txt(txt,n)
    
    #Divide the lists in sublists (necesary for encrypt).
    txt=sublist(txt,n)
    key=sublist(key,n)
    
    if check_determinant(key,n): #check if the password's determinant is diferent of 0
        
        #crypt the text.
        crypted_txt=crypt(txt,key,n)
        string_crypted=number_to_text(crypted_txt)
        
        return string_crypted
    else:
        return False
    
    
def Disencrypt(password,text):
    
    key=text_to_number(password)
    key=validate_password(key)
    n=size(key)
    key=(sublist(key,n))  #preparing the password for the math process

    reverse_key=inverse(key,n)
    reverse_key=unique_list(reverse_key,n)
    reverse_key=module(reverse_key)
    reverse_key=sublist(reverse_key,n)  #get the inverse key

    text=text_to_number(text)
    text=sublist(text,n)  #prepare the text
 
    Final=crypt(text,reverse_key,n)
    Final=number_to_text(Final)  #disencrypt the text
    Final=removeblankspace(Final)
    
    return Final
    
                  
txt='Hola aliados, este mensaje está encriptado.' 
    
password='123secreto' 

def menu():
    opc=input('escoja una opción:\n\n1.-Encriptar.\n2.-Desencrptar\n3.-Cerrar programa\n\n')
    if opc=='1':
        txt=input('Ingrese el texto:\n\n')
        password=input('Ingrese una contraseña:\n\n')
        Encrypted_text=encrypt(txt,password)
        archivo=open('archivoprueba.txt','r+')
        print('\nTexto encriptado:\n',Encrypted_text)
        archivo.write(Encrypted_text)
        archivo.close()
    elif opc=='2':
        archivo=open('archivoprueba.txt','r+')
        password=input('Ingrese la contraseña:\n\n')
        Encrypted_text=archivo.read()
        archivo.close()
        print('\nTexto encriptado: ',Encrypted_text,'\n')
        Normal_text=Disencrypt(password,Encrypted_text)
        print('\ntexto desencriptado:',Normal_text)
    elif opc=='3':
        return
    else:
        print('\nOpción incorrecta, intentelo de nuevo')
    input('Pulse para continuar')
    system('cls')
    menu()
    


menu()
#x=input('escribe: ')










