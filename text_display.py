import sys
import threading
import time
import tkinter as tk

root = tk.Tk()
root.title("認識結果")
root.geometry("600x600+1200+50")

rootFlag = True


canvas = tk.Canvas(root,width=600,height=600)
canvas.grid()

canvas.create_text(300,300,text='5',font=('',250))

def display(root):
    global rootFlag
    root.mainloop()
    rootFlag = False

def input_text(canvas):
    global rootFlag
    n=0
    while True:

        n = input()
        if n == 'a' or rootFlag == False:
            break
        canvas.delete("all")
        canvas.create_text(300,300,text=n,font=('',350))
        #n+=1
        #canvas.create_text(150,150,text=str(n),font=('',100))
        #time.sleep(1)




#canvas.create_text(150,150,text='5',font=('',100))

#label = tk.Label(root,text="5")
#label.pack(anchor = 'center')
#label.grid()

#root.mainloop()

if __name__ == "__main__":
    #th1 = threading.Thread(target=display,args=(root,))
    th2 = threading.Thread(target=input_text,args=(canvas,))

    #th1.start()
    th2.start()
    display(root)
