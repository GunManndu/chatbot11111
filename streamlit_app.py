import streamlit as st
from openai import OpenAI

# =========================
# 페이지 설정
# =========================

st.set_page_config(
    page_title="🎮 게임 추천 챗봇",
    page_icon="🎮",
    layout="wide"
)

# =========================
# CSS 스타일 (다크 테마)
# =========================

st.markdown("""
<style>

/* 전체 앱 */
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

/* 헤더 */
header {
    background-color: #0f1117 !important;
}

[data-testid="stHeader"] {
    background-color: #0f1117 !important;
}

/* 제목 */
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

/* Selectbox */
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #1c2330 !important;
    color: white !important;
    border: 2px solid #4da3ff !important;
    border-radius: 10px;
}

/* MultiSelect */
.stMultiSelect div[data-baseweb="select"] > div {
    background-color: #1c2330 !important;
    color: white !important;
    border: 2px solid #4da3ff !important;
    border-radius: 10px;
}

/* 드롭다운 */
div[role="listbox"] {
    background-color: #1c2330 !important;
}

div[role="option"] {
    background-color: #1c2330 !important;
    color: white !important;
}

div[role="option"]:hover {
    background-color: #263042 !important;
}

/* Chat Input */
[data-testid="stChatInput"] {
    background-color: #0f1117 !important;
    border-top: 1px solid #2c3440;
}

[data-testid="stChatInput"] textarea {
    background-color: #1c2330 !important;
    color: white !important;
}

/* 채팅 메시지 */
[data-testid="chatAvatarIcon-user"] + div {
    background-color: #1d3557 !important;
    color: white !important;
    border-radius: 12px;
    padding: 12px;
}

[data-testid="chatAvatarIcon-assistant"] + div {
    background-color: #1c2330 !important;
    color: white !important;
    border: 1px solid #2c3440;
    border-radius: 12px;
    padding: 12px;
}

/* 버튼 */
.stButton button {
    background-color: #4da3ff !important;
    color: white !important;
    border-radius: 10px;
    border: none;
}

.stButton button:hover {
    background-color: #2d8cff !important;
}

/* 아이콘 */
svg {
    fill: white !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# 제목
# =========================

st.title("🎮 AI 게임 추천 챗봇")

st.write(
    "좋아하는 장르와 플레이 스타일을 설정하고 "
    "나에게 맞는 게임을 추천받아보세요!"
)

# =========================
# 사이드바
# =========================

st.sidebar.title("🎮 게임 취향 설정")

# 장르 선택
genres = st.sidebar.multiselect(
    "좋아하는 장르",
    [
        "RPG",
        "오픈월드",
        "FPS",
        "공포",
        "생존",
        "로그라이크",
        "전략",
        "시뮬레이션",
        "인디",
        "스토리 중심",
        "액션",
        "턴제",
        "퍼즐",
        "리듬",
        "스포츠"
    ]
)

# 평균 플레이 타임
playtime = st.sidebar.slider(
    "평균 플레이 타임 (시간)",
    min_value=1,
    max_value=200,
    value=20
)

# 플랫폼 선택
platforms = st.sidebar.multiselect(
    "사용 플랫폼",
    [
        "PC",
        "모바일",
        "콘솔"
    ]
)

# 선택 내용 표시
st.sidebar.markdown("---")

if genres:
    st.sidebar.write("🎯 선호 장르")
    for genre in genres:
        st.sidebar.write(f"- {genre}")

st.sidebar.write(f"⏰ 평균 플레이 타임: {playtime}시간")

if platforms:
    st.sidebar.write("🕹️ 사용 플랫폼")
    for platform in platforms:
        st.sidebar.write(f"- {platform}")

# =========================
# API 키 입력
# =========================

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

        genre_text = ", ".join(genres) if genres else "미정"
        platform_text = ", ".join(platforms) if platforms else "미정"

        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    f"너는 게임 추천 전문 AI이다. "
                    f"사용자가 좋아하는 장르는 {genre_text} 이고, "
                    f"선호 플레이 타임은 약 {playtime}시간이다. "
                    f"사용 플랫폼은 {platform_text} 이다. "
                    f"이 정보를 바탕으로 게임을 추천하고 "
                    f"게임 특징과 추천 이유를 자세하게 설명해라."
                )
            }
        ]

    # =========================
    # 기존 채팅 출력
    # =========================

    for message in st.session_state.messages:

        if message["role"] != "system":

            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # =========================
    # 사용자 입력
    # =========================

    if prompt := st.chat_input("어떤 게임을 찾고 있나요? 🎮"):

        # 사용자 메시지 저장
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
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
            {
                "role": "assistant",
                "content": response
            }
        )
