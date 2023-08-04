import tkinter as tk


window = tk.Tk()
window.title("Text Widget with Scrollbar")

text = tk.Text(window, height=30, width=60)
scroll = tk.Scrollbar(window)
text.configure(yscrollcommand=scroll.set)
text.pack(side=tk.LEFT)

scroll.config(command=text.yview)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
while(True):
	insert_text = input("enter:: ")

	text.insert(tk.END, insert_text)
tk.mainloop()