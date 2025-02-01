import base64
import tkinter.messagebox
from zhipuai import ZhipuAI
import tkinter
from tkinter import filedialog
import time

root = tkinter.Tk()
root.title("垃圾分类")
root.geometry("300x300")

key_label = tkinter.Label(text="请先输入你的密钥：")
key_label.pack()

key_entry=tkinter.Entry(root)
key_entry.pack()

upload_button = tkinter.Button(root, text='上传图片', command=lambda: upload(),bg="green")
upload_button.pack()
 
def aiphoto(img_path): 
    print("[*]执行aiphoto函数")
    with open(img_path, 'rb') as img_file:
        img_base = base64.b64encode(img_file.read()).decode('utf-8')
    global key
    key = key_entry.get()
    if key:
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
      rubbish_type = response.choices[0].message.content
      answer = tkinter.Label(text=rubbish_type)
      answer.pack()
      print("[*]分类函数内执行knowledge_sc函数")
      ai_knowledge_sc(rubbish_type)
    else:
      print('未输入key')
      tkinter.messagebox.showwarning("警告","未输入key")
      

def ai_knowledge_sc(rubbish_type):
  print("[*]执行ai_knowledge_sc函数")
  client = client = ZhipuAI(api_key=key)
  print("[*]定义client")
  response = client.chat.completions.create(  
    model="glm-4-flash",  
    messages=[
        {"role": "system", "content": "你是一个垃圾分类专家，需要根据用户的垃圾类型，给出准确的垃圾分类相关知识以及该物品的详情。"},
        {"role": "user", "content": str(rubbish_type) + "这类型的垃圾的相关知识"}
    ],
)
  knowledge = response.choices[0].message.content
  knowledge_label = tkinter.Label(text=knowledge)
  knowledge_label.pack()
  

def upload():
    img_path_tuple = filedialog.askopenfilenames(title='选择你需要识别的图片')
    img_path = str(img_path_tuple[0])
    if img_path:
        tkinter.Button(root,text="确定识别",command=lambda:aiphoto(img_path)).pack()
    else:
       print('未选择图片')
       tkinter.messagebox.showwarning("警告","未选择图片")

root.mainloop()