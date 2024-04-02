import requests
import json
import pymysql
import pymysql.cursors
import datetime
from openai import OpenAI
from flask import Flask, request, jsonify

app = Flask(__name__)

client = OpenAI(api_key="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")

mysql_params = {
    'host': '',
    'port': 3306,
    'user': '',
    'password': '',
    'database': '',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor
}

conn = pymysql.connect(**mysql_params)

def current_user(request):
    ## 여기에 현재 로그인된 사용자 id를 반환하는 코드 작성
    ## api로 받아올 것
    return 1

'''
def get_writedAt():
    ## 여기에 api가 요청된 시각을 반환하는 코드 작성
    return datetime.datetime.now().strftime('%Y-%m-%d')'''

@app.route('/diary', methods=['GET'])
def get_info():
    current_time = datetime.datetime.now().isoformat()
    user_id = current_user(request)
    return jsonify({
        'user_id': user_id,
        'current_time': current_time
    })

def to_dict(data):
    info_dict = json.loads(data)
    return info_dict

def get_keywords_from_db():
    try:
        with conn.cursor() as cursor:
            info_dict = to_dict(get_info())
            query = "SELECT * FROM diary WHERE member_id = %s AND date = %s"
            cursor.execute(query, (info_dict['user_id'], info_dict['current_time']))
            result = cursor.fetchall()
        return result
    finally:
        conn.close()

def insert_diary_to_db():
    try:
        with conn.cursor() as cursor:
            query = "INSERT INTO diary (diary) VALUES (%s)"
            cursor.execute(query, get_diary_completion())
        conn.commit()
    except Exception as e:
        print(e)

def get_diary_completion():

    diary_info = get_keywords_from_db()

    prompt = """
    유저가 제공한 정보:
- 언제: %s
- 어디서: %s
- 누구와: %s
- 무엇을: %s
- 느낀점: %s

다이어리 작성 지시:
유저가 제공한 '언제', '어디서', '누구와', '무엇을', '느낀점'에 바탕을 둔 일기를 작성하되, 
유저가 제공한 사실에 대한 추가 정보만을 포함하여 일기를 작성해 주세요.
유저의 느낀점을 중심으로, 그 경험이 유저에게 어떤 의미가 있었는지에 초점을 맞추어 진솔하게 작성해 주세요.
유저가 직접 언급하지 않은 새로운 사실이나 가정은 추가하지 마세요.

좋은 예시는 다음과 같습니다.
{
    - 언제: 2024년 4월 1일
    - 어디서: 제주도 한라산
    - 누구와: 친구들과
    - 무엇을: 한라산 등반
    - 느낀점: 산 정상에서 보는 풍경이 매우 인상적이었고, 함께 등반한 친구들과의 우정도 더 깊어진 기분이었다.

    - 완성된 다이어리의 예시 : 2024년 4월 1일, 친구들과 함께 제주도의 한라산을 등반했다.
    한라산은 한국에서 가장 높은 산으로, 그 정상에서 바라보는 제주도의 풍경은 정말로 인상적이였다.
    제주도의 파란 바다와 울창한 숲이 한눈에 들어왔고, 그 아름다움에 모두가 말을 잃었다.
    
    우리는 등반하면서 서로를 의지하며 많은 얘기를 나누었고, 함께 등반한 친구들과 나는 더욱 가까워진 것을 느꼈다.
    우리는 서로에 대해 더 많이 알게 되었고, 이 여행이 우리 사이의 우정을 더욱 깊게 만들었다는 것을 깨달았다.

    한라산 등반은 단순한 여행 이상의 의미가 있었다.
    이 경험은 나에게 자연의 아름다움을 다시 한번 일깨워 주었고, 친구들과의 관계를 더욱 소중히 여기게 만들었다.
    이번 등반을 통해 얻은 추억과 교훈은 앞으로도 오랫동안 내 마음속에 남아있을 것이다.
    }
    
    위의 예시처럼, 유저가 제공한 정보를 바탕으로 일기를 작성해주세요.
    추가로, 다른 추가적인 말은 덧붙여 제공하지 말고 완성된 다이어리 내용만 답변으로 제공해주세요.

    """ % (diary_info['When'], diary_info['Where'], diary_info['with_whom'], diary_info['what'], diary_info['feelings'])

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "User", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=300,
    )
    return completion.choices[0].message.content

