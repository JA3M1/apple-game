import random
import time
import streamlit as st

# 페이지 설정 (wide 모드)
st.set_page_config(page_title="사과 게임", page_icon="🍎", layout="wide")

# 흰색 네모 박스(버튼 배경/테두리)를 완전히 지우고, 사과 아이콘 자리에 검은색 숫자가 딱 겹치게 하는 CSS
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

    /* 버튼의 흰색 네모 배경, 테두리, 그림자를 완전히 투명하게 제거 */
    div.stButton > button {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        font-size: 15px !important;
        font-weight: bold !important;
        color: #000000 !important; /* 숫자를 검은색으로 고정 */
        padding: 0px !important;
        height: 30px !important;
        min-height: 30px !important;
        width: 100% !important;
    }
    
    /* 마우스 올렸을 때 살짝 초록빛이 감돌도록 설정 */
    div.stButton > button:hover {
        background-color: rgba(255, 255, 255, 0.15) !important;
        border: none !important;
    }

    /* 시작 버튼은 예외적으로 눈에 띄게 스타일링 */
    div.stCol > div > div > div > button {
        background-color: #ffffff !important;
        border: 2px solid #1b5e20 !important;
        border-radius: 10px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        color: #1b5e20 !important;
        height: auto !important;
        padding: 12px 24px !important;
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
if "first_click" not in st.session_state:
    st.session_state.first_click = None
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
    st.session_state.first_click = None


def start_game():
    init_board()
    st.session_state.game_state = "playing"
    st.session_state.start_time = time.time()


# 1. 시작 화면
if st.session_state.game_state == "ready":
    st.markdown("<div style='height: 120px;'></div>", unsafe_allow_html=True)
    st.markdown(
        "<h1 style='text-align: center; font-size: 48px; margin-bottom: 20px;'>🍎 사과 게임</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; font-size: 18px; margin-bottom: 40px;'>사과를 두 개 클릭하여 영역을 지정하고, 네모 안의 숫자 합이 10이 되면 사과와 숫자가 사라집니다!</p>",
        unsafe_allow_html=True,
    )

    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        if st.button("🚀 Start 게임 시작", use_container_width=True):
            start_game()
            st.rerun()

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

    if c4.button("🔄 선택 취소", use_container_width=True):
        st.session_state.first_click = None
        st.rerun()

    if st.session_state.first_click:
        r_f, c_f = st.session_state.first_click
        st.info(
            f"📍 첫 번째 사과 선택됨 ({r_f+1}행, {c_f+1}열). 대각선 위치의 두 번째 사과를 클릭하여 영역을 지정하세요."
        )
    else:
        st.write("사과 영역의 시작점을 클릭하세요.")

    # 16x16 보드 출력 (투명 배경 + 사과 이모지 중앙에 검은색 숫자 결합)
    for r in range(16):
        cols = st.columns(16, gap="small")
        for c in range(16):
            val = st.session_state.board[r][c]
            is_first = st.session_state.first_click == (r, c)

            if val == 0:
                cols[c].markdown(
                    "<div style='height: 30px;'></div>", unsafe_allow_html=True
                )
            else:
                # 선택된 첫 번째 지점은 초록색 테두리 느낌, 나머지는 사과 아이콘 + 검은색 숫자
                if is_first:
                    btn_label = f"🟩{val}"
                else:
                    btn_label = f"🍎{val}"

                if cols[c].button(btn_label, key=f"apple_{r}_{c}"):
                    if st.session_state.first_click is None:
                        st.session_state.first_click = (r, c)
                    else:
                        r1, c1 = st.session_state.first_click
                        r2, c2 = (r, c)

                        min_r, max_r = min(r1, r2), max(r1, r2)
                        min_c, max_c = min(c1, c2), max(c1, c2)

                        total_sum = 0
                        target_coords = []
                        for row in range(min_r, max_r + 1):
                            for col in range(min_c, max_c + 1):
                                current_val = st.session_state.board[row][col]
                                if current_val > 0:
                                    total_sum += current_val
                                    target_coords.append((row, col))

                        if total_sum == 10:
                            count = len(target_coords)
                            st.session_state.score += count * 100
                            st.session_state.cleared_apples += count
                            for tr, tc in target_coords:
                                st.session_state.board[tr][tc] = (
                                    0  # 영역 안의 사과와 숫자 모두 제거 (공백 처리)
                                )
                            st.success("🎉 합이 10입니다! 사과가 제거되었습니다.")
                        else:
                            st.error(
                                f"❌ 선택한 영역의 합이 {total_sum}입니다. (10이 되어야 합니다)"
                            )

                        st.session_state.first_click = None
                    st.rerun()

    time.sleep(1)
    st.rerun()

# 3. 결과 화면
elif st.session_state.game_state == "game_over":
    st.balloons()
    st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)
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

    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        if st.button("🔄 다시 하기", use_container_width=True):
            st.session_state.game_state = "ready"
            st.rerun()
