import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(page_title="✈️ 여행 챗봇", page_icon="🌍")

# 제목 및 설명
st.title("✈️ 여행 도우미 챗봇")
st.write(
    "여행지 추천, 맛집, 일정 짜기, 준비물, 교통 정보 등 "
    "여행과 관련된 질문을 자유롭게 물어보세요! 🌍"
)

# API 키 입력
openai_api_key = st.text_input("OpenAI API 키를 입력하세요", type="password")

if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해주세요.", icon="🗝️")
else:

    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 대화 기록 저장
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "너는 친절한 여행 전문 AI 챗봇이다. "
                    "사용자의 여행 스타일, 예산, 기간 등을 고려해 "
                    "여행지 추천, 일정 계획, 맛집 추천, 교통 안내를 제공한다. "
                    "답변은 보기 쉽게 정리하고, 필요하면 리스트와 이모지를 사용한다."
                )
            }
        ]

    # 기존 메시지 출력
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 사용자 입력
    if prompt := st.chat_input("어디로 여행 가고 싶나요? ✈️"):

        # 사용자 메시지 저장
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        # 사용자 메시지 출력
        with st.chat_message("user"):
            st.markdown(prompt)

        # GPT 응답 생성
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            stream=True,
        )

        # 응답 출력
        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        # 응답 저장
        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )
