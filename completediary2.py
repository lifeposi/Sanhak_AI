import requests
from openai import OpenAI
def getdiaryMap():
    diaryMap = {}
    url = ""
    response = requests.get(url)
    for diary in response.json():
        diaryMap[diary['emotion']] = diary['content']
    return diaryMap

def complete_diary():
    completediary = ""
    for emotion, content in getdiaryMap().items():
        if content is None:
            continue
        else:
            completion = client.chat.completions.create(
                model="gpt-3.0-turbo",
                messages=[
                    {"role": "system", "content": "{comnpletediary}와 입력되는 문장을 결합하여 완성된 문장을 작성해줘. "
                                                  "단, 같은 이벤트가 있다고 판단되면 둘의 이벤트를 연결 혹은 하나로 대체 하되 "
                                                  "두 문장에 있던 감정들은 유지하여 모두 작성해줘"},
                    {"role": "User", "content": "새로운문장: " + content}
                ],
                top_p=0.9,
                logprobs=True,
                top_logprobs=7
            )
            completediary += completion.choices[0].message.content
    return completediary