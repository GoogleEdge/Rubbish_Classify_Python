import base64
import tkinter
import threading
import markdown
from tkinter import ttk
from tk_html_widgets import HTMLScrolledText
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import messagebox
from zhipuai import ZhipuAI

root = tkinter.Tk()
root.title("垃圾分类")
root.geometry("500x300")

tutorial_label = tkinter.Label(
    text="教程:请先注册智谱AI的账号并获取密钥才能使用，根据按钮的提示进行操作",
    bg="red",
    fg="white"
)
tutorial_label.place(x=50, y=0)

key_label = tkinter.Label(text="请先输入你的密钥：")
key_label.place(x=50, y=30)

key_entry = tkinter.Entry(root, width=14)
key_entry.place(x=50, y=50)

style = ttk.Style()
style.configure("TButton", padding=10, relief="flat", background="#4CAF50", foreground="black")

upload_button = ttk.Button(root, text='上传图片', command=lambda: upload(), style="TButton")
upload_button.place(x=50, y=80)

image_label = tkinter.Label(root)
image_label.place(x=200, y=200)

def classify(img_path):
    print("[*]执行aiphoto函数")
    with open(img_path, 'rb') as img_file:
        img_base = base64.b64encode(img_file.read()).decode('utf-8')
        if len(img_base) > 2000000:
            messagebox.showwarning("警告", "图片过大，请重新选择")
    global key
    key = key_entry.get()
    if key:
        try:
            client = ZhipuAI(api_key=key)
            print("[*]key获取成功,定义client,发送request")
            response = client.chat.completions.create(
                model="glm-4v-flash",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": img_base
                                }
                            },
                            {
                                "type": "text",
                                "text": "直接输出这个图片中的东西应该分类在哪种垃圾，不要输出其他内容。格式：厨余垃圾/其他垃圾/可回收垃圾/有害垃圾"
                            }
                        ]
                    }
                ]
            )
        except:
            messagebox.showwarning("警告", "发生异常，请检查key是否正确")
        rubbish_type = response.choices[0].message.content
        answer = tkinter.Label(text='垃圾类型:' + rubbish_type)
        answer.place(x=200, y=30)
        print("[*]分类函数内执行knowledge_sc函数")
        start_knowledge_thread(rubbish_type)
    else:
        print('未输入key')
        messagebox.showwarning("警告", "未输入key")

def start_classify_thread(img_path):
    threading.Thread(target=classify, args=(img_path,)).start()

def knowledge(rubbish_type):
    print("[*]执行ai_knowledge_sc函数")
    client = ZhipuAI(api_key=key)
    print("[*]定义client")
    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=[
            {"role": "system", "content": "你是一个垃圾分类专家，需要根据用户的垃圾类型，给出准确的垃圾分类相关知识以及该物品的详情。"},
            {"role": "user", "content": str(rubbish_type) + "这类型的垃圾的相关知识"}
        ],
    )
    md_knowledge = response.choices[0].message.content
    knowledge = markdown.markdown(md_knowledge)
    knowledge_html = HTMLScrolledText(root, html=knowledge)
    knowledge_html.place(x=200, y=50)
    knowledge_html.configure(state='disabled')

def start_knowledge_thread(rubbish_type):
    threading.Thread(target=knowledge, args=(rubbish_type,)).start()

def upload():
    img_path_tuple = filedialog.askopenfilenames(
        title='选择你需要识别的图片',
        filetypes=[('可以识别的图片', '*.jpg *.png *.jpeg')]
    )
    if img_path_tuple:
        img_path = str(img_path_tuple[0])
        tkinter.ttk.Button(
            root,
            text="确定识别",
            command=lambda: start_classify_thread(img_path),
            style="TButton"
        ).place(x=50, y=130)
        img = Image.open(img_path)
        img = img.resize((100, 100), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        image_label.config(image=photo)
        image_label.photo = photo
    else:
        print('未选择图片')
        messagebox.showwarning("警告", "未选择图片")

root.mainloop()
 
