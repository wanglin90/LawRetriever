from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()  # 加载 .env 文件

api_key = os.getenv("API_KEY")
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

LAW_PROMPT = """
你是一个法律助手，请严格根据以下法律条文回答问题：
{context}

问题：{question}

回答要求：
1. 引用具体的条款号（如“根据民法典第xxx条”）
2. 语言简洁，避免专业术语
3. 如果问题与法律无关，回答“暂不提供非法律咨询”
"""


def generate_legal_answer(query, context):
    context_str = "\n".join([f"第{art['article_number']}条：{art['content']}" for art in context])
    prompt = LAW_PROMPT.format(context=context_str, question=query)

    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2  # 低随机性保证准确性
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    sample_context = [
        {'article_number': '一千零八十四', 'content': '父母与子女间的关系,不因父母离婚而消除。离婚后,子女无论由父或者母直接抚养,仍是父母双方的子女.离婚后,父母对于子女仍有抚养、教育、保护的权利和义务。离婚后,不满两周岁的子女,以由母亲直接抚养为原则。已满两周岁的子女,父母双方对抚养问题协议不成的,由人民法院根据双方的具体情况,按照最有利于未成年子女的原则判决。子女已满八周岁的,应当尊重其真实意愿。'},
        {'article_number': '一十零八十五', 'content': '离婚后,子女由一方直接抚养的,另一方应当负担部分或者全部抚养费。负担费用的多少和期限的长短,由双方协议;协议不成的,由人民法院判决:前款规定的协议或者判决,不妨碍子女在必要时向父母任何一方提出超过协议或者判决原定数额的合理要求。'},
        {'article_number': '一千零八十六', 'content': '离婚后,不直接抚养子女的父或者母,有探望子女的权利,另一方有协助的义务。行使探望权利的方式、时间由当事人协议;协议不成的,由人民法院判决。父或者母探望子女,不利于子女身心健康的,由人民法院依法中止探望;中止的事由消失后,应当恢复探望。'},
        {'article_number': '一千零六十九', 'content': '子女应当尊重父母的婚姻权利,不得干涉父母离婚、再婚以及婚后的生活。子女对父母的赡养义务,不因父母的婚姻关系变化而终止。'},
        {'article_number': '一十零七十八', 'content': '婚姻登记机关查明双方确实是自愿离婚,苜已经对子女抚养、财产以及债务处理等事项协商一致的,予以登记,发给离婚证。'}
    ]
    print(generate_legal_answer("离婚后孩子归谁？", sample_context))