import json

# 텍스트 파일 읽기
with open('text_file.txt', 'r') as file:
    lines = file.readlines()

# 각 줄을 JSON 객체로 변환
data = []
for line in lines:
    prompt, completion = line.split('\t')
    data.append({
        'prompt': prompt.strip(),
        'completion': completion.strip()
    })

# JSON 파일 쓰기
with open('output.json', 'w') as file:
    json.dump(data, file, indent=4)