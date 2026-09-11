import streamlit as st
import pandas as pd
import random

# 스마트폰 화면에 맞춘 모바일 최적화 레이아웃 설정
st.set_page_config(page_title="노무사 판례 암기장", page_icon="🧠", layout="centered")

st.title("🎓 노무사 합격 판례 인출기")
st.caption("구글 스프레드시트 실시간 연동 버전")
st.write("---")

# 🔗 회원님의 구글 시트 주소와 'upload' 탭을 가리키는 전용 연동 링크입니다.
GOOGLE_SHEET_URL = "https://google.com"

@st.cache_data(ttl=5) # 5초마다 구글 시트의 최신 데이터를 자동으로 확인하여 새로고침합니다.
def load_data_from_google():
    try:
        df = pd.read_csv(GOOGLE_SHEET_URL)
        # 빈 행이나 데이터가 없는 행 제거
        df = df.dropna(subset=['title', 'quiz', 'answer'])
        return df.to_dict(orient="records")
    except Exception as e:
        st.error("⚠️ 구글 스프레드시트 주소를 확인해 주세요. 오른쪽 위 [공유] 버튼을 눌러 '링크가 있는 모든 사용자'로 설정되어 있어야 합니다.")
        return []

db = load_data_from_google()

if db:
    # 세션 상태 관리 (구글 시트 행 개수가 바뀌면 문항 순서 리스트도 자동 리셋)
    if 'order' not in st.session_state or len(st.session_state.order) != len(db):
        st.session_state.order = list(range(len(db)))
        random.shuffle(st.session_state.order)
    if 'index' not in st.session_state:
        st.session_state.index = 0

    # 안전하게 인덱스 범위 체크
    if st.session_state.index >= len(db):
        st.session_state.index = 0

    idx = st.session_state.order[st.session_state.index]
    current_item = db[idx]

    # 상단 문항 정보 바 (구글 시트 전체 행 개수만큼 자동 확장)
    st.subheader(f"🔥 문항 [{st.session_state.index + 1} / {len(db)}]")
    st.info(f"**쟁점: {current_item['title']}**")

    st.warning(current_item['quiz'])

    if st.button("👁️ 모범답안 필수 현출 키워드 확인", use_container_width=True):
        st.success(f"**🟢 필수 현출 문구:**\n\n{current_item['answer']}")

    st.write("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⏭️ 다음 판례로 넘어가기", use_container_width=True):
            if st.session_state.index < len(db) - 1:
                st.session_state.index += 1
                st.rerun()
            else:
                st.balloons()
                st.success(f"🎉 구글 시트에 있는 총 {len(db)}개 판례를 모두 정복하셨습니다!")
    with col2:
        if st.button("🔄 처음부터 다시 섞기", use_container_width=True):
            st.session_state.index = 0
            random.shuffle(st.session_state.order)
            st.rerun()
else:
    st.info("💡 구글 스프레드시트의 'upload' 탭 1행에 title, quiz, answer를 적고 아래에 데이터를 입력해 주세요.")
