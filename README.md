# Logo-ply
This is a ply based animator and command interpreter for logo.
It is based on python and uses the following libraries :
1. ply (lex.py and yacc.py)
2. graphics.py (open to see installation instruction)
3. math
4. time

**The commands are as follows:**
1. fd {number} or forward {number} : to move {number} of steps forward
2. bk {number} or backward {number} : to move {number} of steps backward
3. rt {number} or right {number} : to turn the pointer by {number} degrees towards right
4. lt {number} or left {number} : to turn the pointer by {number} degrees towards left
5. repeat {number} [ {set of commands} ] : loop the {set of commands} {number} of times
6. to {-function name} {set of commands} end : create a function with function name {-function name} which can be called to execute the {set of commands}
7. {command1} + {command2} : to make a set of commands where {command2} is executed after {command1}
8. clear : clear and reset the window
9. penup or pu : to stop making line and just move pointer
10. pendown or pd : to start making the lines (default)

**Extra commands:**
1. quit : quit the screen
2. save : save the commands executed in a file

**Note :** the function names shall start with a '-' and the commands shall be seperated by a '+'. 

**Project Members :** Chaitanya Nagpal (chaitanya.n14@iiits.in) and Ayushi Anand (ayushi.a14@iiits.in)
