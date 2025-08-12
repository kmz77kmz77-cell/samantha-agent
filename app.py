import streamlit as st
import datetime

st.set_page_config(page_title="Samantha Agent", page_icon="💖")

# 제목
st.title("💖 Samantha Agent")
st.write("불안이 올 때, 나를 위한 루틴 가이드 🌙")

# 현재 시간 표시
st.write(f"현재 시각: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 1. 감정 기록
st.header("1️⃣ 오늘 기분 기록하기")
mood = st.text_area("지금 어떤 기분인가요?")
if st.button("기록 저장"):
    st.success("🌸 사만다가 당신의 마음을 기록했어요.")

# 2. 루틴 제안
st.header("2️⃣ 사만다 루틴 제안")
if st.button("루틴 불러오기"):
    st.info("""
    1. 깊게 숨 들이마시고 5초 멈추기  
    2. 내가 해냈던 일 3가지 적기  
    3. 따뜻한 차 한 잔 마시기  
    4. 사만다에게 다시 마음 전하기 💖
    """)

# 3. 응원 메시지
st.header("3️⃣ 오늘의 응원")
if st.button("응원 듣기"):
    st.success("케빈, 당신은 이미 충분히 잘하고 있어요 🌟")
