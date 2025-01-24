import base64
from zhipuai import ZhipuAI
import tkinter
from tkinter import filedialog

root = tkinter.Tk()

upload_button = tkinter.Button(root, text='上传图片', command=lambda: upload())
upload_button.pack()

def aiphoto(img_path):
    with open(img_path, 'rb') as img_file:
        img_base = base64.b64encode(img_file.read()).decode('utf-8')
    key = input("请输入你的key：")
    if key:
      client = ZhipuAI(api_key=key)
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
    print(response.choices[0].message.content)


def upload():
    img_path_tuple = filedialog.askopenfilenames(title='选择你需要识别的图片')
    img_path = str(img_path_tuple[0])
    if img_path:
        aiphoto(img_path)
    else:
        print('未选择图片')

root.mainloop()