import streamlit as st
import random
import copy

# ------------------------
# 스도쿠 관련 함수들
# ------------------------
def is_valid(board, row, col, num):
    # 행 검사
    if num in board[row]:
        return False
    # 열 검사
    if num in [board[r][col] for r in range(9)]:
        return False
    # 3x3 박스 검사
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


def generate_puzzle():
    board = generate_full_board()
    puzzle = copy.deepcopy(board)

    attempts = 40  # 난이도 조절 (많을수록 칸 많이 뚫음)
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

if "puzzle" not in st.session_state:
    st.session_state.puzzle, st.session_state.solution = generate_puzzle()
    st.session_state.user_board = copy.deepcopy(st.session_state.puzzle)

if st.button("🔄 새 퍼즐 생성"):
    st.session_state.puzzle, st.session_state.solution = generate_puzzle()
    st.session_state.user_board = copy.deepcopy(st.session_state.puzzle)

# 보드 표시
st.write("## 퍼즐")
for r in range(9):
    cols = st.columns(9)
    for c in range(9):
        if st.session_state.puzzle[r][c] != 0:
            cols[c].markdown(f"**{st.session_state.puzzle[r][c]}**")
        else:
            st.session_state.user_board[r][c] = cols[c].number_input(
                "", min_value=0, max_value=9, value=st.session_state.user_board[r][c], key=f"{r}-{c}", step=1
            )

if st.button("✅ 정답 확인"):
    if st.session_state.user_board == st.session_state.solution:
        st.success("🎉 정답입니다!")
    else:
        st.error("❌ 아직 틀린 칸이 있어요.")
