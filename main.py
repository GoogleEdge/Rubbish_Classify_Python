from aiphoto import aiphoto
import tkinter
from tkinter import filedialog

root = tkinter.Tk()
root.withdraw()

img_path = filedialog.askopenfilename(title='选择你需要识别的图片')
if img_path:
    aiphoto(img_path)
else:
    print('未选择图片')
root.mainloop()