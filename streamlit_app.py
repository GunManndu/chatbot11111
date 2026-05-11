import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(
    page_title="✈️ 여행 챗봇",
    page_icon="🌍",
    layout="centered"
)

# CSS 스타일 적용 (하얀색 + 푸른색 테마)
st.markdown("""
<style>

/* 전체 배경 */
.stApp {
    background-color: #f4f9ff;
}

/* 제목 스타일 */
h1 {
    color: #1e88e5;
    text-align: center;
}

/* 설명 문구 */
p {
    color: #333333;
}

/* 입력창 */
.stTextInput input {
    border: 2px solid #64b5f6;
    border-radius: 10px;
}

/* 채팅 입력창 */
[data-testid="stChatInput"] {
    border-top: 2px solid #90caf9;
    background-color: white;
}

/* 사용자 메시지 */
[data-testid="chatAvatarIcon-user"] + div {
    background-color: #bbdefb;
    border-radius: 12px;
    padding: 10px;
}

/* AI 메시지 */
[data-testid="chatAvatarIcon-assistant"] + div {
    background-color: white;
    border-radius: 12px;
    padding: 10px;
    border: 1px solid #90caf9;
}

/* 버튼 */
.stButton button {
    background-color: #1e88e5;
    color: white;
    border-radius: 10px;
    border: none;
}

.stButton button:hover {
    background-color: #1565c0;
}

</style>
""", unsafe_allow_html=True)

# 제목 및 설명
st.title("✈️ 여행 도우미 챗봇")

st.write(
    "여행지 추천, 맛집, 일정 계획, 교통 정보까지! 🌍\n"
    "여행과 관련된 질문을 자유롭게 물어보세요."
)

# API 키 입력
openai_api_key = st.text_input(
    "OpenAI API 키를 입력하세요",
    type="password"
)

if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해주세요.", icon="🗝️")

else:

    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 세션 상태 생성
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "너는 친절한 여행 전문 AI 챗봇이다. "
                    "사용자의 여행 스타일, 예산, 기간 등을 고려해 "
                    "여행 추천과 여행 계획을 도와준다."
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
