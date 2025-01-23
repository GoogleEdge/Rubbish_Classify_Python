import base64
from zhipuai import ZhipuAI

def aiphoto(img_path):
    with open(img_path, 'rb') as img_file:
        img_base = base64.b64encode(img_file.read()).decode('utf-8')

    client = ZhipuAI(api_key="api key")
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
            "text": "直接告诉这个图片中的东西垃圾分类在哪里，不要输出其他内容"
          }
        ]
      }
    ]
)
    print(response.choices[0].message)
