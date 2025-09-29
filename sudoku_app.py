import streamlit as st
import random
import copy
import time

# ------------------------
# 스도쿠 관련 함수들
# ------------------------
def is_valid(board, row, col, num):
    if num in board[row]:
        return False
    if num in [board[r][col] for r in range(9)]:
        return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r][c] == num:
                return False
    return True


def solve(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve(board):
                            return True
                        board[row][col] = 0
                return False
    return True


def count_solutions(board):
    solutions = []

    def backtrack(bd):
        for r in range(9):
            for c in range(9):
                if bd[r][c] == 0:
                    for num in range(1, 10):
                        if is_valid(bd, r, c, num):
                            bd[r][c] = num
                            backtrack(bd)
                            bd[r][c] = 0
                    return
        solutions.append(copy.deepcopy(bd))

    backtrack(copy.deepcopy(board))
    return len(solutions)


def generate_full_board():
    board = [[0 for _ in range(9)] for _ in range(9)]
    numbers = list(range(1, 10))

    def fill(bd):
        for r in range(9):
            for c in range(9):
                if bd[r][c] == 0:
                    random.shuffle(numbers)
                    for num in numbers:
                        if is_valid(bd, r, c, num):
                            bd[r][c] = num
                            if fill(bd):
                                return True
                            bd[r][c] = 0
                    return False
        return True

    fill(board)
    return board


def generate_puzzle(hole_attempts=40):
    board = generate_full_board()
    puzzle = copy.deepcopy(board)

    attempts = hole_attempts
    while attempts > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)
        while puzzle[row][col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)

        backup = puzzle[row][col]
        puzzle[row][col] = 0

        board_copy = copy.deepcopy(puzzle)
        if count_solutions(board_copy) != 1:
            puzzle[row][col] = backup
            attempts -= 1
    return puzzle, board


# ------------------------
# Streamlit 앱
# ------------------------
st.title("🧩 스도쿠 게임 (Streamlit)")

# 난이도 선택
level = st.sidebar.selectbox("난이도 선택", ["쉬움", "보통", "어려움"])
if level == "쉬움":
    holes = 30
elif level == "보통":
    holes = 40
else:
    holes = 50

# 세션 상태 초기화
if "puzzle" not in st.session_state:
    st.session_state.puzzle, st.session_state.solution = generate_puzzle(holes)
    st.session_state.user_board = copy.deepcopy(st.session_state.puzzle)
    st.session_state.start_time = time.time()

if st.button("🔄 새 퍼즐 생성"):
    st.session_state.puzzle, st.session_state.solution = generate_puzzle(holes)
    st.session_state.user_board = copy.deepcopy(st.session_state.puzzle)
    st.session_state.start_time = time.time()

# 타이머 표시
elapsed = int(time.time() - st.session_state.start_time)
st.write(f"⏱️ 경과 시간: {elapsed//60}분 {elapsed%60}초")

# 보드 표시
st.write("## 퍼즐")
for r in range(9):
    cols = st.columns(9)
    for c in range(9):
        style = "border:1px solid black; text-align:center;"
        if (c+1) % 3 == 0 and c != 8:
            style = "border-right:3px solid black; border:1px solid gray; text-align:center;"
        if (r+1) % 3 == 0 and r != 8:
            style = style.replace("border:1px", "border-bottom:3px")

        if st.session_state.puzzle[r][c] != 0:
            cols[c].markdown(f"<div style='{style}'><b>{st.session_state.puzzle[r][c]}</b></div>", unsafe_allow_html=True)
        else:
            st.session_state.user_board[r][c] = cols[c].number_input(
                "", min_value=0, max_value=9, value=st.session_state.user_board[r][c], key=f"{r}-{c}", step=1
            )

if st.button("✅ 정답 확인"):
    if st.session_state.user_board == st.session_state.solution:
        st.success("🎉 정답입니다!")
    else:
        st.error("❌ 아직 틀린 칸이 있어요.")
