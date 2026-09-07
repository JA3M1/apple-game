import random
import time
import streamlit as st

# 페이지 설정 (wide 모드 고정)
st.set_page_config(page_title="16x16 사과 게임", page_icon="🍏", layout="wide")

# 스크롤을 없애고 화면에 딱 맞추기 위한 CSS + 사과 아이콘 스타일링
st.markdown(
    """
    <style>
    /* 상하좌우 여백을 줄여서 한 화면에 꽉 차게 배치 */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }
    
    .stApp {
        background-color: #e8f5e9;
        overflow: hidden !important; /* 스크롤 방지 */
    }
    
    h1, h2, h3, p, label {
        color: #1b5e20 !important;
        margin-bottom: 0px !important;
    }
    
    /* 16x16 버튼 컴포넌트 크기 및 여백 극대화 압축 */
    div.stButton > button {
        background-color: rgba(255, 255, 255, 0.6) !important;
        border: 1px solid #c8e6c9 !important;
        border-radius: 4px !important;
        font-size: 13px !important;
        font-weight: bold !important;
        color: #b71c1c !important;
        padding: 0px !important;
        height: 28px !important;
        min-height: 28px !important;
        width: 100% !important;
    }
    
    div.stButton > button:hover {
        background-color: #a5d6a7 !important;
        border-color: #2e7d32 !important;
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
if "selected" not in st.session_state:
    st.session_state.selected = []
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
    st.session_state.selected = []
    st.session_state.selected_coords = []


def start_game():
    init_board()
    st.session_state.game_state = "playing"
    st.session_state.start_time = time.time()


def check_and_clear():
    if sum(st.session_state.selected) == 10:
        count = len(st.session_state.selected)
        st.session_state.score += count * 100
        st.session_state.cleared_apples += count

        for r, c in st.session_state.selected_coords:
            st.session_state.board[r][c] = 0

        st.session_state.selected = []
        st.session_state.selected_coords = []
        st.success("🎉 합이 10입니다! 사과가 제거되었습니다.")
    else:
        st.error(
            f"❌ 선택한 숫자의 합이 {sum(st.session_state.selected)}입니다. (10이 되어야 합니다)"
        )
        st.session_state.selected = []
        st.session_state.selected_coords = []


# --- UI 레이아웃 ---
st.title("🍏 16x16 원페이지 초록빛 사과 게임")

# 1. 시작 화면
if st.session_state.game_state == "ready":
    st.markdown("### 🌲 게임 규칙")
    st.write("1. **Start** 버튼을 누르면 스크롤 없는 한 화면에 사과 밭이 펼쳐집니다.")
    st.write(
        "2. 사과 아이콘이 있는 자리에 표시된 **숫자들의 합이 10**이 되도록 클릭하세요."
    )
    st.write("3. **[선택 완료]**를 누르면 사과와 숫자가 함께 사라집니다.")

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

    # 상단 정보 및 컨트롤을 한 줄 컴팩트하게 배치
    info_col1, info_col2, info_col3, btn_col1, btn_col2 = st.columns(
        [1.5, 1.5, 1.5, 2, 2]
    )
    info_col1.metric("⏱️ 남은 시간", f"{remaining_time}초")
    info_col2.metric("🏆 점수", f"{st.session_state.score}점")
    info_col3.metric("🍏 사과", f"{st.session_state.cleared_apples}개")

    if btn_col1.button("✨ 선택 완료", use_container_width=True):
        if st.session_state.selected:
            check_and_clear()
            st.rerun()
        else:
            st.warning("선택된 사과가 없습니다.")

    if btn_col2.button("🔄 초기화", use_container_width=True):
        st.session_state.selected = []
        st.session_state.selected_coords = []
        st.rerun()

    st.write("")

    # 16x16 컴팩트 보드 출력 (사과 아이콘과 숫자 매칭)
    for r in range(16):
        cols = st.columns(16, gap="small")
        for c in range(16):
            val = st.session_state.board[r][c]
            is_selected = (r, c) in st.session_state.selected_coords

            if val == 0:
                cols[c].markdown(
                    "<div style='height:28px;'></div>", unsafe_allow_html=True
                )
            else:
                # 사과 배경 위에 숫자가 오도록 라벨 구성
                if is_selected:
                    label = f"🟩{val}"
                else:
                    label = f"🍎{val}"

                if cols[c].button(label, key=f"btn_{r}_{c}"):
                    if (r, c) not in st.session_state.selected_coords:
                        st.session_state.selected_coords.append((r, c))
                        st.session_state.selected.append(val)
                    st.rerun()

    time.sleep(1)
    st.rerun()

# 3. 결과 화면
elif st.session_state.game_state == "game_over":
    st.balloons()
    st.markdown("## 🌿 게임 종료!")
    st.write("수고하셨습니다! 수확 결과입니다.")

    st.info(
        f"""
    - **최종 점수:** {st.session_state.score} 점
    - **수확한 사과 개수:** {st.session_state.cleared_apples} 개
    """
    )

    if st.button("🔄 다시 하기", use_container_width=True):
        st.session_state.game_state = "ready"
        st.rerun()
