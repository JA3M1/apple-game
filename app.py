import random
import time
import streamlit as st

# 페이지 설정
st.set_page_config(page_title="16x16 사과 게임", page_icon="🍏", layout="wide")

# 초록색 테마를 위한 커스텀 CSS 적용
st.markdown(
    """
    <style>
    .stApp {
        background-color: #e8f5e9;
    }
    h1, h2, h3, p, label {
        color: #1b5e20 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 세션 상태 초기화
if "game_state" not in st.session_state:
    st.session_state.game_state = "ready"  # 'ready', 'playing', 'game_over'
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
    st.session_state.game_duration = 60  # 16x16이므로 제한 시간을 60초로 넉넉하게 설정


def init_board():
    """16x16 크기의 사과(숫자 1~9) 보드를 생성합니다."""
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
    """선택된 사과들의 합이 10인지 확인하고 제거합니다."""
    if sum(st.session_state.selected) == 10:
        count = len(st.session_state.selected)
        st.session_state.score += count * 100
        st.session_state.cleared_apples += count

        # 보드에서 선택된 위치를 빈 칸(0)으로 변경
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
st.title("🍏 16x16 초록빛 사과 게임")

# 1. 시작 화면 (Ready)
if st.session_state.game_state == "ready":
    st.markdown("### 🌲 게임 규칙")
    st.write("1. **Start** 버튼을 누르면 16x16 초록색 사과밭이 펼쳐집니다.")
    st.write("2. 격자판에서 **합이 10이 되는 숫자들**을 여러 개 클릭하여 선택하세요.")
    st.write("3. **[선택 완료]**를 눌러 합이 10인지 확인하고 사과를 없애세요.")
    st.write("4. 제한 시간(60초) 동안 최대한 많은 사과를 없애 고득점을 달성하세요!")

    if st.button("🚀 Start 게임 시작", use_container_width=True):
        start_game()
        st.rerun()

# 2. 플레이 화면 (Playing)
elif st.session_state.game_state == "playing":
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = max(0, int(st.session_state.game_duration - elapsed_time))

    if remaining_time == 0:
        st.session_state.game_state = "game_over"
        st.rerun()

    # 상단 정보 표시
    col1, col2, col3 = st.columns(3)
    col1.metric("⏱️ 남은 시간", f"{remaining_time}초")
    col2.metric("🏆 현재 점수", f"{st.session_state.score}점")
    col3.metric("🍏 없앤 사과", f"{st.session_state.cleared_apples}개")

    st.write("---")

    # 액션 버튼 (상단 배치로 접근성 향상)
    col_a, col_b = st.columns(2)
    if col_a.button("✨ 선택 완료 (합산 확인)", use_container_width=True):
        if st.session_state.selected:
            check_and_clear()
            st.rerun()
        else:
            st.warning("선택된 사과가 없습니다.")

    if col_b.button("🔄 선택 초기화", use_container_width=True):
        st.session_state.selected = []
        st.session_state.selected_coords = []
        st.rerun()

    st.write("")

    # 16x16 보드 그리기
    for r in range(16):
        cols = st.columns(16)
        for c in range(16):
            val = st.session_state.board[r][c]
            is_selected = (r, c) in st.session_state.selected_coords

            if val == 0:
                cols[c].button(
                    "🍃", key=f"btn_{r}_{c}", disabled=True, use_container_width=True
                )
            else:
                label = f"[{val}]" if is_selected else f"{val}"
                if cols[c].button(label, key=f"btn_{r}_{c}", use_container_width=True):
                    if (r, c) not in st.session_state.selected_coords:
                        st.session_state.selected_coords.append((r, c))
                        st.session_state.selected.append(val)
                    st.rerun()

    time.sleep(1)
    st.rerun()

# 3. 결과 화면 (Game Over)
elif st.session_state.game_state == "game_over":
    st.balloons()
    st.markdown("## 🌿 게임 종료!")
    st.write("수고하셨습니다! 16x16 사과밭의 최종 결과입니다.")

    st.info(
        f"""
    - **최종 점수:** {st.session_state.score} 점
    - **제거한 사과 개수:** {st.session_state.cleared_apples} 개
    """
    )

    if st.button("🔄 다시 하기", use_container_width=True):
        st.session_state.game_state = "ready"
        st.rerun()
