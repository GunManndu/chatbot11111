import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(
    page_title="✈️ 여행 챗봇",
    page_icon="🌍",
    layout="wide"
)

# CSS 스타일 (전체 다크 모드 + 흰색 글씨)
st.markdown("""
<style>

/* ========================= */
/* 전체 앱 */
/* ========================= */

.stApp {
    background-color: #0f1117;
    color: white !important;
}

/* 메인 */
.main {
    background-color: #0f1117;
}

/* 기본 텍스트 */
html, body, p, span, label, div {
    color: white !important;
}

/* ========================= */
/* 헤더 */
/* ========================= */

header {
    background-color: #0f1117 !important;
}

[data-testid="stHeader"] {
    background-color: #0f1117 !important;
}

[data-testid="stToolbar"] {
    background-color: #0f1117 !important;
}

/* ========================= */
/* 제목 */
/* ========================= */

h1 {
    color: #4da3ff !important;
    text-align: center;
}

/* ========================= */
/* 사이드바 */
/* ========================= */

section[data-testid="stSidebar"] {
    background-color: #161a23 !important;
    border-right: 1px solid #2c3440;
}

/* ========================= */
/* 입력창 */
/* ========================= */

.stTextInput input {
    background-color: #1c2330 !important;
    color: white !important;
    border: 2px solid #4da3ff !important;
    border-radius: 10px;
}

/* placeholder */
.stTextInput input::placeholder {
    color: #b0b0b0 !important;
}

/* ========================= */
/* Selectbox */
/* ========================= */

.stSelectbox div[data-baseweb="select"] > div {
    background-color: #1c2330 !important;
    color: white !important;
    border: 2px solid #4da3ff !important;
    border-radius: 10px;
}

/* selectbox 내부 */
.stSelectbox * {
    color: white !important;
}

/* 드롭다운 */
div[role="listbox"] {
    background-color: #1c2330 !important;
    color: white !important;
}

/* 옵션 */
div[role="option"] {
    background-color: #1c2330 !important;
    color: white !important;
}

/* hover */
div[role="option"]:hover {
    background-color: #263042 !important;
    color: white !important;
}

/* ========================= */
/* MultiSelect */
/* ========================= */

.stMultiSelect div[data-baseweb="select"] > div {
    background-color: #1c2330 !important;
    color: white !important;
    border: 2px solid #4da3ff !important;
    border-radius: 10px;
}

.stMultiSelect * {
    color: white !important;
}

/* ========================= */
/* Slider */
/* ========================= */

.stSlider * {
    color: white !important;
}

/* ========================= */
/* Chat Input */
/* ========================= */

[data-testid="stChatInput"] {
    background-color: #0f1117 !important;
    border-top: 1px solid #2c3440;
}

[data-testid="stChatInput"] textarea {
    background-color: #1c2330 !important;
    color: white !important;
}

/* ========================= */
/* 채팅 메시지 */
/* ========================= */

/* 사용자 메시지 */
[data-testid="chatAvatarIcon-user"] + div {
    background-color: #1d3557 !important;
    color: white !important;
    border-radius: 12px;
    padding: 12px;
}

/* AI 메시지 */
[data-testid="chatAvatarIcon-assistant"] + div {
    background-color: #1c2330 !important;
    color: white !important;
    border: 1px solid #2c3440;
    border-radius: 12px;
    padding: 12px;
}

/* ========================= */
/* 버튼 */
/* ========================= */

.stButton button {
    background-color: #4da3ff !important;
    color: white !important;
    border-radius: 10px;
    border: none;
}

.stButton button:hover {
    background-color: #2d8cff !important;
}

/* ========================= */
/* 아이콘 */
/* ========================= */

svg {
    fill: white !important;
}

</style>
""", unsafe_allow_html=True)
# 제목
st.title("✈️ AI 여행 도우미")

# =========================
# 사이드바 (여행 정보 설정)
# =========================
st.sidebar.title("🌍 여행 설정")

# 여행지 선택
destination = st.sidebar.selectbox(
    "여행지 선택",
    [
        "서울",
        "부산",
        "도쿄",
        "오사카",
        "파리",
        "런던",
        "뉴욕",
        "방콕"
    ]
)

# 여행 기간 선택
travel_days = st.sidebar.slider(
    "여행 일자",
    min_value=1,
    max_value=30,
    value=3
)

# 여행 스타일 선택
travel_style = st.sidebar.multiselect(
    "여행 스타일",
    [
        "맛집",
        "관광",
        "쇼핑",
        "휴양",
        "액티비티",
        "사진 명소",
        "야경",
        "카페"
    ]
)

# 선택 내용 표시
st.sidebar.markdown("---")
st.sidebar.write(f"📍 여행지: {destination}")
st.sidebar.write(f"📅 여행 기간: {travel_days}일")

if travel_style:
    st.sidebar.write("🎒 여행 스타일:")
    for style in travel_style:
        st.sidebar.write(f"- {style}")

# 설명
st.write(
    "왼쪽에서 여행 정보를 설정하고 "
    "채팅으로 여행 계획을 물어보세요! 🌍"
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
                    f"너는 여행 전문 AI 챗봇이다. "
                    f"사용자의 여행지는 {destination}이고 "
                    f"여행 기간은 {travel_days}일이다. "
                    f"여행 스타일은 {', '.join(travel_style)} 이다. "
                    f"이 정보를 기반으로 여행 추천과 일정을 제안해라."
                )
            }
        ]

    # 기존 메시지 출력
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 채팅 입력
    if prompt := st.chat_input("여행에 대해 질문해보세요 ✈️"):

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
