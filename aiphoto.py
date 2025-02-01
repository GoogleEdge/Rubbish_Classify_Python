import base64
from zhipuai import ZhipuAI

def classify(img_path):
    with open(img_path, 'rb') as img_file:
        img_base = base64.b64encode(img_file.read()).decode('utf-8')
    global key
    key = input("请输入你的key：")
    print("[*]获取了key")
    if key:
      print("[*]key存在,定义client")
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
      global rubbish_type
      rubbish_type = response.choices[0].message.content
      print(response.choices[0].message.content)
    else:
      print('未输入key')

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
  print(response.choices[0].message.content)
