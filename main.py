import aiphoto as ai
import tkinter
from tkinter import filedialog

root = tkinter.Tk()

upload_button = tkinter.Button(root, text='上传图片', command=lambda: upload())
upload_button.pack()

def upload():
    img_path_tuple = filedialog.askopenfilenames(title='选择你需要识别的图片')
    if img_path_tuple:
        img_path = str(img_path_tuple[0])
        ai.classify(img_path)
        ai.ai_knowledge_sc(ai.rubbish_type)
    else:
        print('未选择图片')
root.mainloop()