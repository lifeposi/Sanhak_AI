import requests
import json
import openai
from openai import OpenAI

client = OpenAI()

class MBTI:
    def __init__(self, mbti):
        self.mbti = mbti
        self.energy = mbti[0]
        self.cognition = mbti[1]
        self.judgement = mbti[2]
        self.lifestyle = mbti[3]

    def energy_type(self):
        if self.energy == 'E':
            return '활기차고 특수문자 및 밝은 이모티콘을 사용하여'
        else:
            return '차분하고 소심하며 무난한 이모티콘을 사용하여'

    def cognition_type(self):
        # temperature 값
        if self.cognition == 'N':
            return 1.7
        else:
            return 0.5

    def judgement_type(self):
        if self.judgement == 'T':
            return '진실과 사실을 중심으로 논리적, 분석적이게'
        else:
            return "감정과 감성을 중심으로 주변상황과 공감을 통해"

    def lifestyle_type(self):
        # presence_penalty 값
        if self.lifestyle == 'J':
            return 1.0
        else:
            return -1.0

    def my_mbti(self):
        return self.mbti

    def getdiary(self):
        url = ""
        response = requests.get(url)
        return response.json()

    def prompt_engineering(self):
        completion = client.chat.completions.create(
            model="gpt-3.0-turbo",
            messages=[
                {"role": "system", "content": f"{self.energy_type()} {self.judgement_type()} 일기의 내용에 답변을 줘."},
                {"role": "User", "content": self.getdiary()}
            ],
            temperature=self.cognition_type(),
            presence_penalty=self.lifestyle_type(),
            max_tokens=125,
        )