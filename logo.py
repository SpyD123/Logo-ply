#----- using ply -----
import lex
import yacc
from graphics import *
import math
import time

#------ lex part -----
#tokens
tokens=(
    'REPEAT','NUMBER',
    'RIGHT','LEFT','FORW','BACK',
    'LPAREN','RPAREN','PLUS',
    'PENU','PEND',
    'CLR',
    'NAME','FUNS','FUNE'
    )

#regular expressions for each token
t_RIGHT		= r'(rt)|(right)'
t_LEFT		= r'(lt)|(left)'
t_BACK		= r'(bk)|(back)'
t_FORW		= r'(fd)|(forward)'
t_LPAREN	= r'\['
t_RPAREN	= r'\]'
t_PLUS		= r'\+'
t_REPEAT	= r'(repeat)'
t_PENU		= r'(penup)|(pu)'
t_PEND		= r'(pendown)|(pd)'
t_CLR		= r'(clear)|(clr)'
t_NAME 		= r'\-[a-zA-Z_][a-zA-Z0-9_]*'
t_FUNS		= r'(to)'
t_FUNE		= r'(end)'

def t_NUMBER(t):
    r'\d+'
    t.value=int(t.value)
    return t

t_ignore=" \t\n"

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

#lexer build
lex.lex()

#----- yacc part -----
heading=90	#starting heading
win=GraphWin('Logo',500,500)	#intializing display window
#------ graphics -----
msg=Text(Point(250, 100),"LET'S LEARN LOGO")
cur=Point(250,250)
tur=Circle(cur,5)
cur_x=250
cur_y=250
pen_flag=1
st=""
val=(math.pi)/180	#degree to radians
names={}	#function dictionary

def p_statement_comm(p):	#statement -> expr
    'statement : expr'
    global heading,cur,cur_x,cur_y,val,win,pen_flag,tur,msg
    commands=p[1].split("\n")	#creating commands dictionary
    if commands[-1]=='':
	commands=commands[:-1]
    for i in commands:
	i=i.split("-")	#part1 : command & part2 : numerical value
	if i[0]=='r':	#right turn
	    heading=(360+heading+(int)(i[1]))%360
	elif i[0]=='l':	#left turn
	    heading=(360+heading-(int)(i[1]))%360
	elif i[0]=='f' or i[0]=='b':	#forward or backward
	    dx=(int)((int)(i[1])*(math.cos(heading*val)))	#change in x direction
	    dy=(int)((int)(i[1])*(math.sin(heading*val)))	#change in y direction
	    if i[0]=='b':	#backward command -> reverse direction
		dx=dx*(-1)
		dy=dy*(-1)
	    #updating x and y
	    cur_x=cur_x-dx
	    cur_y=cur_y-dy
	    temp=Point(cur_x,cur_y)
	    #draw line if pen is down
	    if pen_flag==1:
	    	line=Line(cur,temp)
	    	line.draw(win)
		line.setOutline('yellow')
	    #update current
	    cur=temp
	    #move turtle
	    tur.move((-1)*dx,(-1)*dy)
	elif i[0]=='u':	#pen up
	    pen_flag=0
	elif i[0]=='d':	#pen down
	    pen_flag=1
	elif i[0]=='c':	#clear
	    #remove everything
	    for item in win.items[:]:
		item.undraw()
	    win.update()
	    #reset everything to default
	    win.setBackground('black')
	    msg=Text(Point(250, 10),"LET'S LEARN LOGO")
	    msg.draw(win)
	    msg.setOutline('red')
	    cur=Point(250,250)
	    tur=Circle(cur,5)
	    tur.draw(win)
	    tur.setFill('green')
	    tur.setOutline('green')
	    cur_x=250
	    cur_y=250
	    pen_flag=1
	    heading=90
	    st=""

def p_expr_def(p): #expr -> command | command + expr
    '''expr : command
            | command PLUS expr'''   
    #command 
    if len(p)>2:
	s=(str)(p[1])+"\n"+(str)(p[3])
	p[0]=s
    #command + expression
    else:
	p[0]=p[1]

def p_command_typ(p):	#command -> optionm number | repeat number [ expr ] | optionp
    '''command : optionm NUMBER
               | REPEAT NUMBER LPAREN expr RPAREN
	       | optionp'''
    #optionp
    if len(p)<=2:
	p[0]=p[1]
    #repeat number [ expression ]
    elif p[1]=='repeat':
	i=0
	s=""
	while i<p[2]:
		s=s+p[4]+"\n"
		i=i+1
	p[0]=s
    #optionm number
    else:
	s=p[1]+"-"+(str)(p[2])
	p[0]=s

def p_optionm_choice(p):	#optionm -> right | left | forward | backward
    '''optionm : RIGHT
               | LEFT
               | FORW
               | BACK'''
    p[0]=p[1][0]

def p_func_def(p):	#func -> to name expr end | name
    '''func : FUNS NAME expr FUNE
	    | NAME'''
    #name
    if p[1][0]=='-':
	p[0]=names.get(p[1],"\n")	#creating dictionary
    #to name expr end
    else:
	names[p[2]]=p[3]	#searching dictionary
	p[0]="\n"

def p_optionp_choice(p):	#optionp -> pen up | pen down | clear | func 
    '''optionp : PENU
	       | PEND
	       | CLR
	       | func'''
    #pen up | pen down
    if p[1][0]=='p':
	if len(p[1])>2:    
	    p[0]=p[1][3]
	else:
	    p[0]=p[1][1]
    #clear
    elif p[1][0]=='c':    
	p[0]='c'
    #func
    else:
	p[0]=p[1]

def p_error(p):
    print("Syntax error at '%s'" % p.value)

#yacc build (LALR)
yacc.yacc()

def inside(A,B,C):	#find button press
    if (C.getX() > A.getX() and C.getX() < B.getX())and(C.getY() > A.getY() and C.getY() < B.getY()):
	return 1	#button press true
    return 0	#button press false

def clr():	#clear screen
    global win
    for item in win.items[:]:
	item.undraw()
    win.update()

def setup():	#first screen
    global win
    clr()
    win.setBackground('yellow')
    msg1=Text(Point(250, 150),"LET'S LEARN")
    msg1.draw(win)
    msg1.setSize(20)
    msg1.setFace("courier")
    msg2=Text(Point(250, 200),"LOGO")
    msg2.draw(win)
    msg2.setStyle("bold italic")
    msg2.setFill('green')
    msg2.setSize(30)
    rec0=Rectangle(Point(50,50),Point(450,450))
    rec0.setOutline("black")
    rec0.draw(win)
    rec0.setWidth(5)
    #start new button
    P1=Point(175,250)
    P2=Point(325,290)
    rec1=Rectangle(P1,P2)
    rec1.setFill("black")
    rec1.setOutline("red")
    rec1.setWidth(3)
    rec1.draw(win)
    msg3=Text(Point(250, 270),"START NEW")
    msg3.draw(win)
    msg3.setFill('red')
    #open button
    P3=Point(175,300)
    P4=Point(325,340)
    rec2=Rectangle(P3,P4)
    rec2.setFill("black")
    rec2.setOutline("red")
    rec2.setWidth(3)
    rec2.draw(win)
    msg4=Text(Point(250, 320),"OPEN")
    msg4.draw(win)
    msg4.setFill('red')
    #quit button
    P5=Point(175,350)
    P6=Point(325,390)
    rec3=Rectangle(P5,P6)
    rec3.setFill("black")
    rec3.setOutline("red")
    rec3.setWidth(3)
    rec3.draw(win)
    msg5=Text(Point(250, 370),"QUIT")
    msg5.draw(win)
    msg5.setFill('red')
    #button press
    while True:
    	click=win.getMouse()
    	if inside(P1,P2,click)==1:
	    return 's'
    	elif inside(P3,P4,click)==1:
	    return 'o'
	elif inside(P5,P6,click)==1:
	    return 'q'

def choice(s1,s2,s3):	#choice selection from 2 options
    global win
    clr()
    win.setBackground('yellow')
    #question
    msg1=Text(Point(250, 200),s1)
    msg1.draw(win)
    msg1.setSize(20)
    msg1.setFace("courier")
    rec0=Rectangle(Point(50,50),Point(450,450))
    rec0.setOutline("black")
    rec0.draw(win)
    rec0.setWidth(5)
    #option 1
    P1=Point(90,250)
    P2=Point(240,290)
    rec1=Rectangle(P1,P2)
    rec1.setFill("black")
    rec1.setOutline("red")
    rec1.setWidth(3)
    rec1.draw(win)
    msg3=Text(Point(165, 270),s2)
    msg3.draw(win)
    msg3.setFill('red')
    #option 2
    P3=Point(260,250)
    P4=Point(410,290)
    rec2=Rectangle(P3,P4)
    rec2.setFill("black")
    rec2.setOutline("red")
    rec2.setWidth(3)
    rec2.draw(win)
    msg4=Text(Point(335, 270),s3)
    msg4.draw(win)
    msg4.setFill('red')
    #button press
    while True:
    	click=win.getMouse()
    	if inside(P1,P2,click)==1:
	    return 1
    	elif inside(P3,P4,click)==1:
	    return 2

def input_screen(s1,size):	#input screen
    global win
    clr()
    win.setBackground('yellow')
    #question
    msg1=Text(Point(250, 200),s1)
    msg1.draw(win)
    msg1.setSize(20)
    msg1.setFace("courier")
    rec0=Rectangle(Point(50,50),Point(450,450))
    rec0.setOutline("black")
    rec0.draw(win)
    rec0.setWidth(5)
    #input
    input_b=Entry(Point(250,270),size)
    input_b.draw(win)
    input_b.setFill('white')
    input_b.setTextColor('black')
    #wait
    win.getMouse()
    s=input_b.getText()
    return s

def save():	#save option
    global st
    c=choice("Do you want to save ?","YES","NO") 
    if c==1:
	f=input_screen("Enter file name : ",10)
	fobj=open(f,'w')
	fobj.write(st)
	fobj.close()

def quit():	#quit button press
    global win
    clr()
    win.setBackground('yellow')
    msg=Text(Point(250, 250),"BYE AND THANK YOU")
    msg.draw(win)
    msg.setSize(20)
    msg.setFace("courier")
    msg.setStyle("bold")
    rec0=Rectangle(Point(50,50),Point(450,450))
    rec0.setOutline("black")
    rec0.draw(win)
    rec0.setWidth(5)
    win.getMouse()

def animate(s,ch,t):	#animate after option
    global st,win
    cs=s.split("\n")
    yacc.parse("clear")
    for c in cs:
	if c<>"":
	    print c
	    yacc.parse(c)
	    if ch=="man":
		win.getMouse()
	    else:
	    	time.sleep(t)
    st=s

def start():	#start the command screen
    global st
    while True:
    	try:
            s=raw_input('logo > ')
    	except EOFError:
            break
    	if s=="quit":	#quit command
	    save()
	    return
	elif s=="save":	#save command
	    save()
	    c=choice("Do you want to continue ?","YES","NO")	#continue ?
    	    if c==1:
		print "Command history : "
		animate(st,"auto",0)
	    else:
		st=""
		first()
    	elif s=="": #ignore command
	    continue
    	else:	#parse command
	    st=st+s+"\n"
    	    yacc.parse(s)

def first():	#first function
    global st
    sx=setup()	#setup
    if sx=='s':	#save button
	yacc.parse("clear")
	start()
	first()
    elif sx=='q':	#quit button
	quit()
	win.close()
	return
    elif sx=='o':	#open button
	f=input_screen("Enter file name : ",10)
	fobj=open(f)
	st=fobj.read()
	fobj.close()
	c=choice("Select mode : ","MANUAL","AUTO")	#animation option
    	if c==1:
	    animate(st,"man",1)
	else:
	    t=input_screen("Speed : ",10)
	    animate(st,"auto",(int)(t))
	start()
	first()

def main():
    first()	#start

main()
