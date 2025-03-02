import base64
import tkinter
import threading
import markdown
import os
from tkinter import ttk,filedialog,messagebox
from tk_html_widgets import HTMLScrolledText
from zhipuai import ZhipuAI

def classify(img_path):
    with open(img_path, 'rb') as img_file:
      file_size = os.path.getsize(img_path)
      if file_size > 5 * 1024 * 1024:
        messagebox.showwarning("警告", "图片大小超过5MB")
      img_base = base64.b64encode(img_file.read()).decode('utf-8')
    global key
    key = key_entry.get()
    if key:
        try:
            root.after(0, lambda: statu_label.configure(text="状态：正在识别垃圾类型..."))
            client = ZhipuAI(api_key=key)
            response = client.chat.completions.create(model="glm-4v-flash",messages=[{"role": "user","content": [{"type": "image_url","image_url": {"url": img_base}},{"type": "text","text": "直接输出这个图片中的东西应该分类在哪种垃圾，不要输出其他内容。格式：厨余垃圾/其他垃圾/可回收垃圾/有害垃圾"}]}])
        except Exception as e:
            root.after(0, lambda: messagebox.showerror("错误", str(e)))
        rubbish_type = response.choices[0].message.content
        answer.configure(text="垃圾类型："+rubbish_type)
        start_knowledge_thread(rubbish_type)
        statu_label.configure(text="状态：等待")
    else:
        messagebox.showwarning("警告", "未输入key")

def start_classify_thread(img_path):
    upload_button.configure(state="disabled")
    okbutton.configure(state="disabled") 
    threading.Thread(target=classify, args=(img_path,)).start()

def knowledge(rubbish_type):
    statu_label.configure(text="状态：正在生成垃圾类型知识...")
    client = ZhipuAI(api_key=key)
    response = client.chat.completions.create(model="glm-4-flash",messages=[{"role": "system", "content": "你是一个垃圾分类专家，需要根据用户的垃圾类型，给出准确的垃圾分类相关知识以及该物品的详情。"},{"role": "user", "content": str(rubbish_type) + "这类型的垃圾的相关知识"}],)
    md_knowledge = response.choices[0].message.content
    knowledge = markdown.markdown(md_knowledge)
    knowledge_html = HTMLScrolledText(root,html=knowledge)
    knowledge_html.place(x=200, y=50)
    knowledge_html.configure(state='disabled')
    statu_label.configure(text="状态：等待")
    root.after(0, lambda: upload_button.configure(state="normal"))

def start_knowledge_thread(rubbish_type):
    threading.Thread(target=knowledge, args=(rubbish_type,)).start()

def upload():
    img_path = filedialog.askopenfilename(title='选择你需要识别的图片',filetypes=[('可以识别的图片', '*.jpg *.png *.jpeg')])
    if img_path:
        global okbutton
        okbutton = ttk.Button(root,text="确定识别",command=lambda: start_classify_thread(img_path),style="TButton")
        okbutton.place(x=50, y=130)
    else:
        print('未选择图片')
        messagebox.showwarning("警告", "未选择图片")

if __name__ == '__main__':
  rubbish_type = ""

  root = tkinter.Tk()
  root.title("垃圾分类")
  root.geometry("820x430")

  key_label = tkinter.Label(text="请先输入你的密钥：")
  key_label.place(x=50, y=30)

  key_entry = tkinter.Entry(root, width=14)
  key_entry.place(x=50, y=50)

  style = ttk.Style()
  style.configure("TButton", padding=10, relief="flat", foreground="black")

  upload_button = ttk.Button(root, text='上传图片', command=lambda: upload(), style="TButton")
  upload_button.place(x=50, y=80)

  statu_label = tkinter.Label(root,text="状态：等待")
  statu_label.place(x=30, y=400)

  version_label = tkinter.Label(root,text="V2.2.0")
  version_label.place(x=750, y=400)

  answer = tkinter.Label(text='垃圾类型:' + rubbish_type)
  answer.place(x=200, y=30)

  root.mainloop()