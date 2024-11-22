# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import font
import os
import RetrievalModel as RM


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root = tk.Tk()







    root.title("Search Engine")
    root.geometry("1024x480")
    root.configure(bg='#000000')



    back_frame = tk.Frame(root,bg='#2c2e30')
    back_frame.pack(fill="both", expand=True)
    back_frame.grid_rowconfigure(0)  # Allow row 0 to expand
    back_frame.grid_rowconfigure(1, weight=1)  # Allow row 1 to expand
    back_frame.grid_columnconfigure(0, weight=1)



    img = Image.open(r"C:\Users\skydo\Pictures\Screenshot 2024-11-18 201722.png")
    img_tk = ImageTk.PhotoImage(img)
    label = tk.Label(back_frame,bg="#2c2e30", text="Loading image...")
    label.grid(row=0,column=0,sticky="nsew",pady=(10,0))
    # Display the image in a Label
    label.config(image=img_tk)
    label.image = img_tk

    bottom_frame = tk.Frame(back_frame,bg='#2c2e30')
    bottom_frame.grid(row=1,column=0,sticky="nsew",pady=(0,10),padx=80)






    customFont = font.Font(family="Arial", size=20, weight="bold")
    search_frame = tk.Frame(bottom_frame)
    search_box = tk.Text(search_frame,width=50,font=customFont,height=1,wrap='none')
    search_box.grid(row=0,column=0,sticky="nsew")
    search_btn = tk.Button(search_frame,width=5,text='⌕',font=('Bold'), bg='#76808a',bd=0,activebackground='#2c2e30', command=lambda :(startSearch(bottom_frame)))
    search_btn.grid(row=0,column=1,sticky="nsew")
    search_frame.pack()

    resultFrame = tk.Frame(bottom_frame)
    resultFrame.pack(fill="both", expand=True,pady=10)
    resultList = tk.Listbox(resultFrame, justify="center")
    resultList.pack(fill="both", expand=True)

    def startSearch(bottom_frame):
        itemList = RM.process_query(str(search_box.get("1.0",tk.END)))
        print(itemList)

        for i in range(5):
            resultList.delete(0)

        for i in range(len(itemList)):
            if i < 5:
                resultList.insert(tk.END,itemList[i])
        resultList.config(height=50)





    root.mainloop()
