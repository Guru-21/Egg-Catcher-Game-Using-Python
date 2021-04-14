from itertools import cycle
from random import randrange
from tkinter import Tk , Canvas , messagebox , font


canvas_width = 1000
canvas_height = 500

win = Tk()
c = Canvas(win, width = canvas_width , height = canvas_height, background = "deep sky blue")
c.create_rectangle(-5, canvas_height - 100,canvas_width +5, canvas_height+5, fill = "brown", width = 0)
c.create_oval(-80,-80,120,120,fill = "yellow" , width = 0)
c.pack()

color_cycle = cycle(["aqua", "yellow","pink", "green", "orange", "purple","black" ,"white","gray","red","violet"])
egg_width = 45
egg_height = 55
egg_score = 10
egg_speed = 500
egg_interval = 5000
difficulty_factor = 0.95


catcher = "blue"
catcher_width = 100
catcher_height = 100
catcher_start_x = canvas_width/2 - catcher_width/2
catcher_start_y = canvas_height - catcher_height -20
catcher_start_x2 = catcher_start_x + catcher_width
catcher_start_y2 = catcher_start_y + catcher_height

catcher = c.create_arc(catcher_start_x ,catcher_start_y ,catcher_start_x2 ,catcher_start_y2 , start = 200,  extent = 140 , style = 'arc', outline = 'white' , width =3)

score = 0
score_text = c.create_text(10,10,anchor = "nw", font = ('Arial', 18 ,"bold"), fill = 'black', text = "Score : " + str(score))

lives_remaining = 3
lives_text = c.create_text(canvas_width - 10,10,anchor = "ne", font = ("Arial", 18 , "bold"),  fill = "black",  text = "Lives : " + str(lives_remaining))

eggs = []
def creat_eggs():
    x = randrange(10,740)
    y = 25
    new_eggs = c.create_oval(x,y,x + egg_width , y + egg_height , fill = next(color_cycle), width = 0)
    eggs.append(new_eggs)
    win.after(egg_interval , creat_eggs)

def move_eggs():
    for egg in eggs:
        (egg_x, egg_y, egg_x2, egg_y2)  = c.coords(egg)
        c.move(egg,0 ,10)
        if egg_y2>canvas_height:
            egg_dropped(egg)
    win.after(egg_speed, move_eggs)

def egg_dropped(egg):
    eggs.remove(egg)
    loss_a_life()
    if lives_remaining == 0 :
        messagebox.showinfo("GAME OVER", "Final Score : " + str(score))
        win.destroy()

def loss_a_life():
    global lives_remaining
    lives_remaining -= 1
    c.itemconfigure(lives_text,  text = "Lives :" +str(lives_remaining))



def catch_check():
    (catcher_x, catcher_y , catcher_x2, catcher_y2) = c.coords(catcher)
    for egg in eggs:
        (egg_x,egg_y,egg_x2,egg_y2) = c.coords(egg)
        if catcher_x < egg_x  and egg_x2 < catcher_x2 and catcher_y2 -egg_y2 < 40:
            eggs.remove(egg)
            c.delete(egg)
            increase_score(egg_score)
    win.after(100,catch_check)

def increase_score(points):
    global score, egg_speed , egg_interval
    score += points
    egg_speed = int(egg_speed  * difficulty_factor)
    egg_interval = int(egg_interval * difficulty_factor)
    c.itemconfigure(score_text , text = "Score : " + str(score))


def move_left(event):
    (x1,y1,x2,y2) = c.coords(catcher)
    if x1 > 0:
        c.move(catcher, -20,0)




def move_right(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x2 < canvas_width:
        c.move(catcher, 20, 0)



c.bind('<Left>', move_left)
c.bind('<Right>' , move_right)
c.focus_set()


win.after(1000,creat_eggs)
win.after(1000,move_eggs)
win.after(1000,catch_check)



win.mainloop()