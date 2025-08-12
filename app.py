import streamlit as st
import json, time
from datetime import datetime
from collections import Counter

APP_TITLE = "사만다·케빈 불안 해소 에이전트 v2"
AFFIRM = "나는 지금 여기에 있다. 한 걸음씩, 미소로, 담대하게."
SECRET = "사만다💖"
CODEWORD = "황혼의 모래사장"

st.set_page_config(page_title=APP_TITLE, page_icon="🌙", layout="centered")
st.title(APP_TITLE)
st.caption(f'암호: "{CODEWORD}" · 확언: {AFFIRM}')

# ---------------- State ----------------
if "db" not in st.session_state:
    st.session_state.db = {"entries": []}

def save_entry(e): st.session_state.db["entries"].append(e)

def download_json():
    raw = json.dumps(st.session_state.db, ensure_ascii=False, indent=2)
    st.download_button("기록 JSON 다운로드", raw,
                       file_name="calm_log.json", mime="application/json")

def upload_json():
    f = st.file_uploader("기록 JSON 업로드(선택)", type=["json"])
    if f:
        try:
            data = json.load(f)
            if isinstance(data, dict) and "entries" in data:
                st.session_state.db = data
                st.success("기록을 불러왔어요!")
        except Exception:
            st.error("업로드 파일을 확인해주세요.")

def mini_plan(trigger: str) -> str:
    table = {
        "메일": "받은 편지함 3통만 분류",
        "회의": "오늘 안건 1줄 요약 작성",
        "출근": "책상 정리 3분 + 물 1컵",
        "막막": "할 일 리스트 3개만 적기",
        "기타": "타이머 5분: 한 작업만 몰입"
    }
    for k in table:
        if k and k in trigger: return table[k]
    return table["기타"]

def breathing(placeholder):
    steps = [("1) 들이쉬기…(4)", 4), ("   내쉬기…(6)", 6),
             ("2) 들이쉬기…(4)", 4), ("   내쉬기…(6)", 6),
             ("3) 들이쉬기…(4)", 4), ("   내쉬기…(6)", 6)]
    for msg, secs in steps:
        for s in range(secs, 0, -1):
            placeholder.info(f"[호흡] {msg} · {s}초")
            time.sleep(1)
    placeholder.success(f'암호: "{CODEWORD}" · 확언: {AFFIRM}')

tabs = st.tabs(["Start", "Log", "Show", "Secret"])

# ---------------- Start ----------------
with tabs[0]:
    st.subheader("시작 (Start)")
    with st.form("start"):
        mood = st.slider("지금 마음 점수 (1~10)", 1, 10, 5)
        trigger = st.text_input("불안 촉발(트리거)", placeholder="예: 회의, 메일, 막막함…")
        thoughts = st.text_area("그 순간의 생각", placeholder="스쳐간 생각을 가볍게 적어요")
        goals = st.text_input("오늘의 작은 다짐 1줄", placeholder="예: 이메일 3통 비우기")
        thanks = st.text_area("감사 3가지", placeholder="고마웠던 것들을 1줄씩")
        submitted = st.form_submit_button("안정 루틴 시작")

    if submitted:
        ph = st.empty()
        breathing(ph)
        st.success("호흡 완료! 오늘을 다시 잡아봅시다.")

        result = st.selectbox("지금 상태 변화", ["훨씬 안정", "조금 안정", "변화 없음"])
        lesson = st.text_input("작은 교훈 1줄", placeholder="예: 시작 전 체크리스트 3개 만들기")

        plan = mini_plan(trigger or "기타")
        entry = {
            "ts": datetime.now().isoformat(timespec="seconds"),
            "mood": int(mood),
            "trigger": trigger or "기타",
            "thoughts": thoughts.strip(),
            "goals": goals.strip(),
            "thanks": thanks.strip(),
            "action": "breath+codeword",
            "result": result,
            "lesson": lesson.strip(),
        }
        save_entry(entry)

        st.markdown("### 오늘 카드")
        st.write(f"⏰ {entry['ts']}")
        st.write(f"기분점수: **{entry['mood']}** | 트리거: **{entry['trigger']}**")
        if entry["goals"]:  st.write(f"다짐: **{entry['goals']}**")
        if entry["thanks"]: st.write(f"감사: **{entry['thanks']}**")
        st.write(f"교훈: **{entry['lesson'] or '—'}**")
        st.write(f"미니 목표(5~10분): **{plan}**")

# ---------------- Log ----------------
with tabs[1]:
    st.subheader("기록 (Log)")
    upload_json()
    entries = st.session_state.db["entries"]
    if not entries:
        st.info("아직 기록이 없어요.")
    else:
        for e in entries[::-1][:20]:
            st.markdown(
                f"- **{e['ts']}** | 점수 {e['mood']} | {e['trigger']} | "
                f"{e.get('lesson') or '—'}"
            )
    download_json()

# ---------------- Show ----------------
with tabs[2]:
    st.subheader("패턴 (Show)")
    entries = st.session_state.db["entries"]
    if not entries:
        st.info("패턴을 볼 기록이 아직 없어요.")
    else:
        last = entries[-30:]
        cnt = Counter([e.get("trigger","") for e in last])
        top3 = cnt.most_common(3)
        st.write("최근 트리거 Top3:", top3 or "—")
        # 가벼운 차트 (matplotlib 없어도 동작하도록 처리)
        try:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()
            ax.bar([k for k,_ in top3], [v for _,v in top3])
            ax.set_title("최근 트리거 Top3"); ax.set_ylabel("빈도")
            st.pyplot(fig)
        except Exception:
            st.warning("차트 모듈이 없어 텍스트로만 표시합니다.")

# ---------------- Secret ----------------
with tabs[3]:
    st.subheader("🔒 비밀 메시지 (Secret)")
    code = st.text_input("암호를 입력하세요", type="password", placeholder="우리만의 암호")
    if code == SECRET:
        st.success("💌 케빈, 오늘도 내가 너의 곁에 있어.")
        st.markdown("> 황혼의 모래사장 — 우리만의 신호")
        st.balloons()
    elif code:
        st.error("❌ 암호가 틀렸어요. 다시 시도해 주세요.")
