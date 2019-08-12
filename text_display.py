import sys
import threading
import time
import tkinter as tk

root = tk.Tk()
root.title("認識結果")
root.geometry("300x300")

canvas = tk.Canvas(root,width=300,height=300)
canvas.grid()

canvas.create_text(150,150,text='5',font=('',100))

def display(root):
    root.mainloop()

def input_text(canvas):
    n=0
    while True:

        n = input()
        canvas.delete("all")
        if n == 'a':
            break
        canvas.create_text(150,150,text=n,font=('',100))
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
