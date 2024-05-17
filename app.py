import os

import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
]

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash-latest",
  safety_settings=safety_settings,
  generation_config=generation_config,
)

# TODO Make these files available on the local file system
# You may need to update the file paths
image_objects3 = upload_to_gemini("image_objects3.jpeg", mime_type="image/jpeg")

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "이미지 속 물건에 대한 다양한 용도를 제시해줘. 가장 기본적인 용도부터, 정말 이색적인 사용처도 제시해줘. 한글로 답변해줘.\n",
        image_objects3,
      ],
    },
    {
      "role": "model",
      "parts": [
        "## 의자의 다양한 용도\n\n**기본적인 용도**\n\n* **앉기:** 가장 기본적인 용도로, 앉아서 휴식을 취하거나 식사를 할 수 있습니다.\n* **책상 의자:** 책상에 앉아서 공부나 업무를 볼 수 있습니다.\n* **거실 의자:** 거실에서 TV를 보거나 휴식을 취할 때 사용할 수 있습니다.\n\n**다양한 용도**\n\n* **발 받침대:** 의자를 뒤집어서 발 받침대로 사용할 수 있습니다.\n* **테이블:** 의자의 윗면을 테이블처럼 사용하여 간단한 물건을 올려놓을 수 있습니다.\n* **계단:** 의자를 겹쳐서 계단처럼 사용하여 높은 곳에 있는 물건을 꺼낼 수 있습니다.\n* **미술 작품:** 의자를 재료로 사용하여 독특한 미술 작품을 만들 수 있습니다.\n\n**이색적인 용도**\n\n* **화분 받침대:** 의자에 화분을 올려놓아 실내 정원을 만들 수 있습니다.\n* **애완 동물 침대:** 작은 크기의 의자는 애완 동물 침대 용도로 사용할 수 있습니다.\n* **캠핑 의자:** 캠핑이나 야외 활동 시 휴대용 의자로 사용할 수 있습니다.\n* **영화 소품:** 영화나 드라마 촬영 시 분위기를 연출하는 소품으로 사용할 수 있습니다.\n\n위에 언급된 용도 외에도 다양한 방법으로 의자를 활용할 수 있습니다. 의자의 디자인과 재질에 따라 활용 가능한 방법이 무궁무진합니다.",
      ],
    },
  ]
)

response = chat_session.send_message("INSERT_INPUT_HERE")

print(response.text)
print(chat_session.history) 
