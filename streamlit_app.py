# =========================
# 사이드바
# =========================

st.sidebar.title("🎮 게임 취향 설정")

# =========================
# 장르 선택 (체크박스)
# =========================

st.sidebar.subheader("🎯 좋아하는 장르")

genre_list = [
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

selected_genres = []

for genre in genre_list:
    if st.sidebar.checkbox(genre):
        selected_genres.append(genre)

# =========================
# 평균 플레이 타임
# =========================

playtime = st.sidebar.slider(
    "⏰ 평균 플레이 타임 (시간)",
    min_value=1,
    max_value=200,
    value=20
)

# =========================
# 플랫폼 선택
# =========================

platforms = st.sidebar.multiselect(
    "🕹️ 사용 플랫폼",
    [
        "PC",
        "모바일",
        "콘솔"
    ]
)

# =========================
# 선택 결과 출력
# =========================

st.sidebar.markdown("---")

if selected_genres:
    st.sidebar.write("🎮 선택한 장르")
    for genre in selected_genres:
        st.sidebar.write(f"- {genre}")

st.sidebar.write(f"⏰ 플레이 타임: {playtime}시간")

if platforms:
    st.sidebar.write("🖥️ 플랫폼")
    for platform in platforms:
        st.sidebar.write(f"- {platform}")

# =========================
# system prompt에 사용
# =========================

genre_text = ", ".join(selected_genres) if selected_genres else "미정"
platform_text = ", ".join(platforms) if platforms else "미정"
