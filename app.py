import random
import time
import streamlit as st

# 페이지 설정 (wide 모드)
st.set_page_config(page_title="사과 게임", page_icon="🍎", layout="wide")

# 초록색 배경 및 UI 스타일링
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 0.3rem !important;
        padding-bottom: 0.3rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
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

    /* 결과 팝업 내 텍스트 색상 처리 */
    .stAlert p, .stAlert span, div[data-testid="stMarkdownContainer"] p {
        color: #000000 !important;
    }

    /* 사과 버튼 스타일 (컴팩트하게 조정하여 하단 잘림 방지) */
    div.stButton > button {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        font-size: 18px !important;
        font-weight: bold !important;
        color: #000000 !important;
        padding: 0px !important;
        height: 32px !important;
        min-height: 32px !important;
        width: 100% !important;
    }
    
    div.stButton > button:hover {
        background-color: rgba(255, 255, 255, 0.25) !important;
        border: none !important;
    }

    /* 시작/재시작 버튼 스타일 */
    .action-btn div.stButton > button {
        background-color: #ffffff !important;
        border: 2px solid #1b5e20 !important;
        border-radius: 10px !important;
        font-size: 20px !important;
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
if "game_id" not in st.session_state:
    st.session_state.game_id = 0  # 버튼 키 잔상 방지를 위한 고유 ID


def init_board():
    st.session_state.board = [
        [random.randint(1, 9) for _ in range(16)] for _ in range(16)
    ]
    st.session_state.score = 0
    st.session_state.cleared_apples = 0
    st.session_state.first_click = None
    st.session_state.game_id += 1  # 게임 시작/재시작마다 키를 완전히 새로 갱신


def start_game():
    init_board()
    st.session_state.game_state = "playing"
    st.session_state.start_time = time.time()


# 1. 시작 화면 (Ready 상태)
if st.session_state.game_state == "ready":
    st.markdown("<div style='height: 120px;'></div>", unsafe_allow_html=True)
    st.markdown(
        "<h1 style='text-align: center; font-size: 48px; margin-bottom: 20px;'>🍎 사과 게임</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; font-size: 18px; margin-bottom: 40px;'>사과 두 개를 클릭해 영역을 지정하고, 네모 안의 숫자 합이 10이 되도록 만드세요!</p>",
        unsafe_allow_html=True,
    )

    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        st.markdown('<div class="action-btn">', unsafe_allow_html=True)
        if st.button("🚀 Start 게임 시작", key="main_start_btn", use_container_width=True):
            start_game()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# 2. 플레이 중 상태 (Playing)
elif st.session_state.game_state == "playing":
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = max(0, int(st.session_state.game_duration - elapsed_time))

    if remaining_time == 0:
        st.session_state.game_state = "game_over"
        st.rerun()

    # 상단 상태바 (컴팩트하게 배치)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("⏱️ 남은 시간", f"{remaining_time}초")
    c2.metric("🏆 점수", f"{st.session_state.score}점")
    c3.metric("🍏 사과", f"{st.session_state.cleared_apples}개")

    if c4.button("🔄 선택 취소", key=f"cancel_btn_{st.session_state.game_id}", use_container_width=True):
        st.session_state.first_click = None
        st.rerun()

    st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)

    # 16x16 보드 출력 (안내 문구를 없애고 간격을 줄여 하단까지 잘림 없이 표시)
    for r in range(16):
        cols = st.columns(16, gap="small")
        for c in range(16):
            val = st.session_state.board[r][c]
            is_first = st.session_state.first_click == (r, c)

            if val == 0:
                cols[c].markdown(
                    "<div style='height: 32px;'></div>", unsafe_allow_html=True
                )
            else:
                if is_first:
                    btn_label = f"🟩{val}"
                else:
                    btn_label = f"🍎{val}"

                if cols[c].button(btn_label, key=f"apple_{st.session_state.game_id}_{r}_{c}"):
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
                                st.session_state.board[tr][tc] = 0

                        st.session_state.first_click = None
                    st.rerun()

    time.sleep(1)
    st.rerun()

# 3. 게임 종료 상태 (Game Over 팝업)
elif st.session_state.game_state == "game_over":
    st.balloons()

    # 결과 오버레이 팝업창
    st.markdown(
        """
        <div style="
            position: fixed;
            top: 30%;
            left: 50%;
            transform: translate(-50%, -30%);
            background-color: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0px 0px 20px rgba(0,0,0,0.5);
            z-index: 9999;
            text-align: center;
            width: 400px;
        ">
            <h2 style="color: #1b5e20 !important; margin-bottom: 15px;">🌿 게임 종료!</h2>
            <p style="color: #000000 !important; font-size: 16px; margin-bottom: 10px;">최종 점수: <b>{score} 점</b></p>
            <p style="color: #000000 !important; font-size: 16px; margin-bottom: 20px;">수확한 사과 개수: <b>{apples} 개</b></p>
        </div>
    """.format(
            score=st.session_state.score,
            apples=st.session_state.cleared_apples,
        ),
        unsafe_allow_html=True,
    )

    # 팝업 내 버튼들 배치 (다시 하기 & 처음으로)
    st.markdown(
        "<div style='position: fixed; top: 52%; left: 50%; transform: translate(-50%, -52%); z-index: 10000; width: 300px;'>",
        unsafe_allow_html=True,
    )
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🔄 다시 하기", key=f"popup_restart_{st.session_state.game_id}", use_container_width=True):
            start_game()
            st.rerun()
    with col_btn2:
        if st.button("🏠 처음으로", key=f"popup_home_{st.session_state.game_id}", use_container_width=True):
            st.session_state.game_state = "ready"
            st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)
