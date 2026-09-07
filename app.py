import random
import time
import streamlit as st

# 페이지 설정 (wide 모드)
st.set_page_config(page_title="사과 게임", page_icon="🍎", layout="wide")

# 흰색 네모 배경을 완전히 없애고 사과 아이콘 위에 검은색 숫자가 딱 겹쳐 보이도록 하는 CSS
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
        height: 100vh !important;
        overflow: hidden !important;
    }
    
    .stApp {
        background-color: #2e7d32 !important;
        overflow: hidden !important;
    }
    
    h1, h2, h3, p, label {
        color: #ffffff !important;
        margin: 0px !important;
    }

    /* 버튼의 흰색 네모 배경과 테두리를 완전히 투명하게 제거 */
    div.stButton > button {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        font-size: 16px !important;
        font-weight: bold !important;
        color: #000000 !important; /* 숫자를 검정색으로 설정 */
        padding: 0px !important;
        height: 32px !important;
        min-height: 32px !important;
        width: 100% !important;
    }
    
    /* 마우스 올렸을 때 은은한 효과 */
    div.stButton > button:hover {
        background-color: rgba(255, 255, 255, 0.2) !important;
        border: none !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 세션 상태 초기화
if "game_state" not in st.session_state:
    st.session_state.game_state = "ready"
if "score" not in st.session_state:
    st.session_state.score = 0
if "cleared_apples" not in st.session_state:
    st.session_state.cleared_apples = 0
if "board" not in st.session_state:
    st.session_state.board = []
if "selected_coords" not in st.session_state:
    st.session_state.selected_coords = []
if "start_time" not in st.session_state:
    st.session_state.start_time = 0
if "game_duration" not in st.session_state:
    st.session_state.game_duration = 60


def init_board():
    st.session_state.board = [
        [random.randint(1, 9) for _ in range(16)] for _ in range(16)
    ]
    st.session_state.score = 0
    st.session_state.cleared_apples = 0
    st.session_state.selected_coords = []


def start_game():
    init_board()
    st.session_state.game_state = "playing"
    st.session_state.start_time = time.time()


# --- UI 레이아웃 ---
st.markdown(
    "<h3 style='text-align: center;'>🍎 사과 게임 (16 x 16)</h3>",
    unsafe_allow_html=True,
)

# 1. 시작 화면
if st.session_state.game_state == "ready":
    st.markdown(
        "<div style='text-align: center; margin-top: 50px;'>", unsafe_allow_html=True
    )
    st.write(
        "사과 아이콘 자리에 적힌 **검은색 숫자들의 합이 10**이 되도록 클릭하세요."
    )
    st.write("합이 10이 되면 사과와 숫자가 함께 사라집니다!")

    if st.button("🚀 Start 게임 시작", use_container_width=True):
        start_game()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# 2. 플레이 화면
elif st.session_state.game_state == "playing":
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = max(0, int(st.session_state.game_duration - elapsed_time))

    if remaining_time == 0:
        st.session_state.game_state = "game_over"
        st.rerun()

    # 상단 상태바
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("⏱️ 남은 시간", f"{remaining_time}초")
    c2.metric("🏆 점수", f"{st.session_state.score}점")
    c3.metric("🍎 사과", f"{st.session_state.cleared_apples}개")

    if c4.button("🔄 선택 초기화", use_container_width=True):
        st.session_state.selected_coords = []
        st.rerun()

    st.write("")

    # 16x16 보드 출력 (네모 배경 없이 사과 아이콘 자리에 검은색 숫자가 위치)
    for r in range(16):
        cols = st.columns(16, gap="small")
        for c in range(16):
            val = st.session_state.board[r][c]
            is_selected = (r, c) in st.session_state.selected_coords

            if val == 0:
                cols[c].markdown(
                    "<div style='height: 32px;'></div>", unsafe_allow_html=True
                )
            else:
                # 선택된 경우 초록색 배경/테두리 느낌의 이모지, 아닐 경우 사과 아이콘과 검은색 숫자 결합
                if is_selected:
                    btn_label = f"🟩 {val}"
                else:
                    btn_label = f"🍎 {val}"

                if cols[c].button(btn_label, key=f"apple_{r}_{c}"):
                    if (r, c) in st.session_state.selected_coords:
                        st.session_state.selected_coords.remove((r, c))
                    else:
                        st.session_state.selected_coords.append((r, c))

                        # 선택된 사과들의 합 검사
                        current_sum = sum(
                            st.session_state.board[coord[0]][coord[1]]
                            for coord in st.session_state.selected_coords
                        )
                        if current_sum == 10:
                            count = len(st.session_state.selected_coords)
                            st.session_state.score += count * 100
                            st.session_state.cleared_apples += count
                            for cr, cc in st.session_state.selected_coords:
                                st.session_state.board[cr][cc] = 0
                            st.session_state.selected_coords = []
                        elif current_sum > 10:
                            st.session_state.selected_coords = []
                    st.rerun()

    time.sleep(1)
    st.rerun()

# 3. 결과 화면
elif st.session_state.game_state == "game_over":
    st.balloons()
    st.markdown(
        "<h2 style='text-align: center; color: white;'>🌿 게임 종료!</h2>",
        unsafe_allow_html=True,
    )
    st.info(
        f"""
    - **최종 점수:** {st.session_state.score} 점
    - **수확한 사과 개수:** {st.session_state.cleared_apples} 개
    """
    )

    if st.button("🔄 다시 하기", use_container_width=True):
        st.session_state.game_state = "ready"
        st.rerun()
