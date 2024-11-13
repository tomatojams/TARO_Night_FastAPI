# !pip install -U langchain openai
# !pip install -U langchain-openai


class ai_init:

    from ai.pt_components.prompt_template import template_pt
    from ai.pt_components.extract_chain import (
        create_custom_extraction_chain,
    )

    from typing import Dict
    from langchain.prompts import PromptTemplate
    from langchain.chains import SequentialChain
    from langchain.chains import create_tagging_chain
    from langchain_core.pydantic_v1 import BaseModel
    from langchain.chains import ConversationChain
    from .pt_components.setting_llm import (
        llm,
        memory,
        memory_key,
        input_key,
        output_key,
    )

    prompt = PromptTemplate(
        input_variables=[memory_key, input_key], template=template_pt
    )

    # Initialize and return conversation chain
    con_chain = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=prompt,
        verbose=True,
        input_key=input_key,
        output_key=output_key,
    )

    # 분기 + 추출 테스트 + 시퀀셜

    extract_schema = {
        "properties": {
            "cutomer_name": {"type": "string"},
            "cutomer_feeling": {"type": "string"},
            "cutomer_age": {"type": "string"},
            "cutomer_extra_info": {"type": "string"},
        },
        "required": ["이름"],
    }

    tag_schema = {
        "properties": {
            "sentiment": {
                "type": "string",
                "enum": [
                    "행복",
                    "중립",
                    "우울",
                    "고통",
                    "슬픔",
                    "분노",
                    "불안",
                    "기쁨",
                    "놀람",
                    "기대",
                    "기타",
                ],
                "description": "사용자의 감정을 나타내는 태그입니다.",
            },
            "problem": {
                "type": "string",
                "enum": ["가족", "애인", "직장", "학교", "기타"],
                "description": "사용자가 직면한 문제의 종류를 나타내는 태그입니다.",
            },
            "conNumber": {
                "type": "integer",
                "default": 1,
                "description": "llm이 말한 대화의 횟수입니다.",
            },
        }
    }

    tag_chain = create_tagging_chain(tag_schema, llm)
    extract_chain = create_custom_extraction_chain(extract_schema, llm)



    overall = SequentialChain(
        chains=[
            con_chain,
            # multi_prompt_chain,
            extract_chain,
            tag_chain,
        ],
        input_variables=["input"],
        output_variables=["out_text", "extracted_data", "text"],
    )

    class UserRequest(BaseModel):
        user_message: str

    def gernerate_answer(self, req: UserRequest) -> Dict[str, str]:
        context = req.dict()
        context["input"] = context["user_message"]
        print(context)
        answer = ai_init.overall.invoke(context)
        # answer = multi_prompt_chain.run(context)
        # answer = ai_init.con_chain.invoke(context)
        # print(answer)
        return {"answer": answer}

    # 문제가 발생하면 상담사 추천하는 로직을 구현
    import requests

    # 현재 날씨 크롤링 self 인자 필요없음.
    def get_location_by_ip():
        import requests

        try:
            response = requests.get("https://ipinfo.io")
            data = response.json()
            location = data.get("loc")
            return location.split(",")
        except Exception as e:
            print(f"Error: {e}")
            return None

    current_location = get_location_by_ip()
    # print(f"Current location (latitude, longitude): {current_location}")

    lag = current_location[0]
    lon = current_location[1]
    API_KEY = "70884f237363a4b09ec8fed86b4877f1"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lag}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    # data에서 눈또는 비가 오는지 확인
    weather = data["weather"][0]["description"]
    from datetime import datetime

    # 현재 날짜와 시간 가져오기
    current_date_time = datetime.now()

    # 날짜만 가져오기
    current_date = current_date_time.date()
    current_time = current_date_time.time()
