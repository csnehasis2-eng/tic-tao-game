
import streamlit as st
import numpy as np

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Tic Tac Toe",
    page_icon="🎮",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>
.stApp {
    background: #0B1120;
    color: white;
}

.block-container {
    max-width: 650px;
    padding-top: 2rem;
}

h1, h2, h3, p {
    color: white;
}

.game-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    letter-spacing: 3px;
    margin-bottom: 0;
}

.subtitle {
    text-align: center;
    color: #94A3B8;
    margin-bottom: 30px;
}

.turn-card {
    background: #172033;
    padding: 18px;
    border-radius: 15px;
    text-align: center;
    border: 1px solid #26344D;
    margin-bottom: 20px;
}

.cell {
    font-size: 38px;
    font-weight: 800;
}

div.stButton > button {
    width: 100%;
    height: 100px;
    border-radius: 16px;
    background: #172033;
    border: 1px solid #334155;
    color: white;
    font-size: 38px;
    font-weight: bold;
    transition: 0.2s;
}

div.stButton > button:hover {
    background: #25334D;
    border-color: #60A5FA;
    color: white;
}

div.stButton > button:disabled {
    opacity: 1;
    background: #1E293B;
    color: #60A5FA;
    border-color: #334155;
}

div.stButton > button:focus:not(:active) {
    border-color: #60A5FA;
    color: white;
}

div.stButton > button:active {
    background: #334155;
}

div.stButton > button[kind="primary"] {
    background: #2563EB;
    border: none;
}

</style>
""", unsafe_allow_html=True)


# ---------------- GAME LOGIC ----------------

def check_winner(b):
    for i in range(3):
        if abs(np.sum(b[i, :])) == 3:
            return "X" if np.sum(b[i, :]) == 3 else "O"

        if abs(np.sum(b[:, i])) == 3:
            return "X" if np.sum(b[:, i]) == 3 else "O"

    if np.trace(b) == 3:
        return "X"
    if np.trace(b) == -3:
        return "O"

    diagonal = np.trace(np.fliplr(b))

    if diagonal == 3:
        return "X"
    if diagonal == -3:
        return "O"

    if not np.any(b == 0):
        return "DRAW"

    return None


# ---------------- SESSION STATE ----------------

if "board" not in st.session_state:
    st.session_state.board = np.zeros((3, 3), dtype=int)

if "current" not in st.session_state:
    st.session_state.current = 1

if "result" not in st.session_state:
    st.session_state.result = None


def reset_game():
    st.session_state.board = np.zeros((3, 3), dtype=int)
    st.session_state.current = 1
    st.session_state.result = None


def make_move(row, col):
    if st.session_state.result is not None:
        return

    board = st.session_state.board

    if board[row, col] != 0:
        return

    board[row, col] = st.session_state.current

    st.session_state.result = check_winner(board)

    if st.session_state.result is None:
        st.session_state.current *= -1


# ---------------- HEADER ----------------

st.markdown(
    '<div class="game-title">TIC TAC TOE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Challenge your friend. Make your move.</div>',
    unsafe_allow_html=True
)


# ---------------- TURN STATUS ----------------

result = st.session_state.result
current = st.session_state.current

if result is None:
    player = "X" if current == 1 else "O"

    st.markdown(
        f"""
        <div class="turn-card">
            <h3 style="margin:0;">Player {player}'s Turn</h3>
            <p style="margin:5px 0 0;color:#94A3B8;">
                {'Blue' if player == 'X' else 'Orange'} is playing
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

elif result == "DRAW":
    st.markdown("""
    <div class="turn-card">
        <h2>🤝 It's a Draw!</h2>
        <p style="color:#94A3B8;">Nobody wins this round.</p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown(f"""
    <div class="turn-card">
        <h2>🏆 Player {result} Wins!</h2>
        <p style="color:#94A3B8;">Congratulations!</p>
    </div>
    """, unsafe_allow_html=True)


# ---------------- GAME BOARD ----------------

board = st.session_state.board

for row in range(3):
    cols = st.columns(3, gap="small")

    for col in range(3):
        value = board[row, col]

        if value == 1:
            symbol = "X"
        elif value == -1:
            symbol = "O"
        else:
            symbol = " "

        with cols[col]:
            st.button(
                symbol,
                key=f"cell_{row}_{col}",
                disabled=(value != 0 or result is not None),
                on_click=make_move,
                args=(row, col),
                use_container_width=True
            )


# ---------------- SCORE / CONTROLS ----------------

st.markdown("<br>", unsafe_allow_html=True)

x_count = np.count_nonzero(board == 1)
o_count = np.count_nonzero(board == -1)

score1, score2 = st.columns(2)

with score1:
    st.metric("PLAYER X", x_count)

with score2:
    st.metric("PLAYER O", o_count)

st.markdown("<br>", unsafe_allow_html=True)

st.button(
    "🔄  NEW GAME",
    on_click=reset_game,
    type="primary",
    use_container_width=True
)

st.markdown("""
<p style="text-align:center;color:#64748B;font-size:12px;margin-top:25px;">
    BUILT WITH PYTHON • NUMPY • STREAMLIT
</p>
""", unsafe_allow_html=True)
