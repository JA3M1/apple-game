import random
import time
import streamlit as st

# 페이지 설정 (wide 모드)
st.set_page_config(page_title="진짜 사과 게임", page_icon="🍎", layout="wide")

# 스크롤을 완전히 없애고 16x16 그리드를 한 화면에 맞추는 CSS 스타일
st.markdown(
    """
    <style>
    /* 상하좌우 여백 제거 및 스크롤 원천 차단 */
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

    /* 16x16 사과밭 그리드 컨테이너 */
    .apple-grid {
        display: grid;
        grid-template-columns: repeat(16, minmax(0, 1fr));
        gap: 3px;
        width: 100%;
        max-width: 750px;
        margin: 0 auto;
    }

    /* 개별 사과 아이템 스타일 (네모 박스 느낌 제거, 사과와 숫자가 한몸처럼) */
    .apple-item {
        position: relative;
        aspect-ratio: 1;
        background-color: #d32f2f;
        border-radius: 50% 50% 45% 45%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        font-weight: bold;
        color: white;
        cursor: pointer;
        box-shadow: inset -2px -2px 4px rgba(0,0,0,0.3), 1px 1px 3px rgba(0,0,0,0.2);
        user-select: none;
        transition: transform 0.1s;
    }

    .apple-item:hover {
        transform: scale(1.08);
    }

    /* 선택된 사과 스타일 (초록색 테두리 또는 색상 변환) */
    .apple-item.selected {
        background-color: #388e3c !important;
        box-shadow: 0 0 8px #a5d6a7, inset -2px -2px 4px rgba(0,0,0,0.3);
    }

    /* 빈 자리 (사과가 사라진 곳) */
    .apple-empty {
        aspect-ratio: 1;
        visibility: hidden;
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
    "<h3 style='text-align: center;'>🍎 실시간 사과 밭 (16 x 16)</h3>",
    unsafe_allow_html=True,
)

# 1. 시작 화면
if st.session_state.game_state == "ready":
    st.markdown(
        "<div style='text-align: center; margin-top: 50px;'>", unsafe_allow_html=True
    )
    st.write("나무에 달린 숫자의 합이 **10**이 되도록 드래그하거나 선택하세요.")
    st.write("스크롤 없이 한 화면에 모든 사과가 표시됩니다!")

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

    if c4.button("🔄 초기화", use_container_width=True):
        st.session_state.selected_coords = []
        st.rerun()

    st.write("")

    # 쿼리 파라미터나 상태를 활용한 클릭 이벤트 처리 구조 구성
    # 스트림릿에서 그리드 내 개별 클릭을 받기 위해 스트림릿 고유 버튼 방식을 병행하되,
    # CSS를 통해 완전히 사과 모양으로 렌더링되도록 처리합니다.

    for r in range(16):
        cols = st.columns(16, gap="small")
        for c in range(16):
            val = st.session_state.board[r][c]
            is_selected = (r, c) in st.session_state.selected_coords

            if val == 0:
                cols[c].markdown(
                    "<div style='height: 24px;'></div>", unsafe_allow_html=True
                )
            else:
                # 선택 여부에 따른 스타일 분기
                btn_label = f"{val}"
                if cols[c].button(btn_label, key=f"apple_{r}_{c}"):
                    if (r, c) in st.session_state.selected_coords:
                        st.session_state.selected_coords.remove((r, c))
                    else:
                        st.session_state.selected_coords.append((r, c))

                        # 선택된 사과들의 합이 10인지 검사
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
                            # 합이 10을 넘으면 초기화
                            st.session_state.selected_coords = []
                    st.rerun()

    time.sleep(1)
    st.rerun()

# 3. 결과 화면
elif st.session_state.game_state == "game_over":
    st.balloons()
    st.markdown(
        "<h2 style='text-align: center;'>🌿 게임 종료!</h2>",
        unsafe_allow_html=True,
    )
    st.success(
        f"최종 점수: **{st.session_state.score}점** | 수확한 사과: **{st.session_state.cleared_apples}개**"
    )

    if st.button("🔄 다시 하기", use_container_width=True):
        st.session_state.game_state = "ready"
        st.rerun()
