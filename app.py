
import streamlit as st
import numpy as np

st.set_page_config(
    page_title="Tic Tac Toe | Arena",
    page_icon="🎮",
    layout="centered"
)

# ---------------- CSS ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 15% 10%, #182b50 0%, transparent 38%),
        radial-gradient(ellipse at 85% 80%, #241b49 0%, transparent 38%),
        #080d19;
    color: #f8fafc;
}

header, footer, #MainMenu {
    visibility: hidden;
}

.block-container {
    max-width: 680px;
    padding: 35px 20px 40px;
}

.hero {
    text-align: center;
    margin-bottom: 32px;
}

.logo {
    display: inline-block;
    padding: 8px 16px;
    border: 1px solid #334c72;
    border-radius: 30px;
    background: #14213a;
    color: #93c5fd;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 3px;
    margin-bottom: 17px;
}

.hero h1 {
    font-size: clamp(38px, 8vw, 55px);
    font-weight: 900;
    letter-spacing: -3px;
    margin: 0;
    background: linear-gradient(90deg, #ffffff, #93c5fd, #c4b5fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #8190a9;
    font-size: 13px;
    margin-top: 10px;
}

.players {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 13px;
    margin-bottom: 22px;
}

.player {
    padding: 17px;
    background: rgba(22, 34, 57, 0.8);
    border: 1px solid #293a57;
    border-radius: 18px;
    text-align: center;
    transition: 0.2s;
}

.player.active-x {
    border-color: #38bdf8;
    box-shadow: 0 0 22px rgba(56,189,248,.12);
}

.player.active-o {
    border-color: #c084fc;
    box-shadow: 0 0 22px rgba(192,132,252,.12);
}

.player-icon {
    font-size: 28px;
    font-weight: 900;
}

.x-color { color: #38bdf8; }
.o-color { color: #c084fc; }

.player-name {
    font-size: 13px;
    font-weight: 700;
    color: #f1f5f9;
    margin-top: 7px;
}

.player-status {
    color: #8291aa;
    font-size: 10px;
    margin-top: 5px;
    letter-spacing: 1px;
}

.status {
    background: rgba(20, 32, 53, .9);
    border: 1px solid #293a57;
    padding: 15px;
    text-align: center;
    border-radius: 14px;
    margin-bottom: 19px;
    color: #cbd5e1;
    font-size: 14px;
}

.game-wrapper {
    background: linear-gradient(145deg, #17243b, #10192b);
    padding: 15px;
    border: 1px solid #33445f;
    border-radius: 24px;
    box-shadow: 0 20px 65px rgba(0,0,0,.4);
}

div[data-testid="stHorizontalBlock"] {
    gap: 10px;
}

div.stButton > button {
    height: clamp(85px, 19vw, 125px);
    width: 100%;
    border-radius: 17px;
    background: linear-gradient(145deg, #1b2b46, #142139);
    border: 1px solid #354765;
    color: #f8fafc;
    font-size: clamp(35px, 8vw, 49px);
    font-weight: 900;
    box-shadow: 0 5px 12px rgba(0,0,0,.22);
    transition: all .2s ease;
}

div.stButton > button:hover:not(:disabled) {
    background: linear-gradient(145deg, #263d60, #1c3050);
    border: 1px solid #60a5fa;
    transform: translateY(-3px);
    box-shadow: 0 8px 22px rgba(56,189,248,.15);
    color: white;
}

div.stButton > button:disabled {
    opacity: 1;
    cursor: default;
    background: #18263e;
    border-color: #30435e;
}

div.stButton > button:focus {
    box-shadow: none;
    outline: none;
}

div[data-testid="stButton"]:has(button:disabled) {
    cursor: default;
}

div[data-testid="stMetric"] {
    background: rgba(22,34,57,.8);
    border: 1px solid #293a57;
    padding: 13px 16px;
    border-radius: 15px;
}

div[data-testid="stMetricLabel"] {
    color: #94a3b8;
}

div[data-testid="stMetricValue"] {
    color: white;
    font-weight: 800;
}

div.stButton > button[kind="primary"] {
    height: 53px;
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    border: none;
    color: white;
    font-size: 14px;
    font-weight: 800;
    letter-spacing: 1px;
    border-radius: 13px;
    box-shadow: 0 7px 25px rgba(79,70,229,.25);
}

.footer {
    text-align: center;
    color: #53627c;
    font-size: 10px;
    letter-spacing: 2px;
    margin-top: 30px;
}

@media(max-width: 480px) {
    .block-container {
        padding: 25px 12px;
    }
    .game-wrapper {
        padding: 10px;
    }
}
</style>
""", unsafe_allow_html=True)


# ---------------- GAME LOGIC ----------------

def check_winner(b):
    for i in range(3):
        row_sum = np.sum(b[i, :])
        col_sum = np.sum(b[:, i])

        if row_sum == 3 or col_sum == 3:
            return "X"

        if row_sum == -3 or col_sum == -3:
            return "O"

    d1 = np.trace(b)
    d2 = np.trace(np.fliplr(b))

    if d1 == 3 or d2 == 3:
        return "X"

    if d1 == -3 or d2 == -3:
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

if "scores" not in st.session_state:
    st.session_state.scores = {"X": 0, "O": 0, "DRAW": 0}


def reset_game():
    st.session_state.board = np.zeros((3, 3), dtype=int)
    st.session_state.current = 1
    st.session_state.result = None


def make_move(r, c):
    if st.session_state.result is not None:
        return

    if st.session_state.board[r, c] != 0:
        return

    st.session_state.board[r, c] = st.session_state.current

    result = check_winner(st.session_state.board)
    st.session_state.result = result

    if result:
        st.session_state.scores[result] += 1
    else:
        st.session_state.current *= -1


# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">
    <div class="logo">✦ GAME ARENA</div>
    <h1>TIC TAC TOE</h1>
    <p>THINK SMART. PLAY BOLD. OWN THE GRID.</p>
</div>
""", unsafe_allow_html=True)


# ---------------- PLAYER CARDS ----------------

current = st.session_state.current
result = st.session_state.result

x_active = current == 1 and result is None
o_active = current == -1 and result is None

st.markdown(f"""
<div class="players">
    <div class="player {'active-x' if x_active else ''}">
        <div class="player-icon x-color">X</div>
        <div class="player-name">PLAYER ONE</div>
        <div class="player-status">
            {'● YOUR TURN' if x_active else 'PLAYER 01'}
        </div>
    </div>
    <div class="player {'active-o' if o_active else ''}">
        <div class="player-icon o-color">O</div>
        <div class="player-name">PLAYER TWO</div>
        <div class="player-status">
            {'● YOUR TURN' if o_active else 'PLAYER 02'}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------- GAME STATUS ----------------

if result is None:
    player = "X" if current == 1 else "O"
    status_text = f"⚡ PLAYER {player} — IT'S YOUR TURN"
elif result == "DRAW":
    status_text = "🤝 MATCH DRAW — WELL PLAYED!"
else:
    status_text = f"🏆 PLAYER {result} WINS THE MATCH!"

st.markdown(
    f'<div class="status">{status_text}</div>',
    unsafe_allow_html=True
)


# ---------------- BOARD ----------------

st.markdown('<div class="game-wrapper">', unsafe_allow_html=True)

board = st.session_state.board

for r in range(3):
    cols = st.columns(3, gap="small")

    for c in range(3):
        value = board[r, c]

        symbol = " " if value == 0 else ("X" if value == 1 else "O")

        with cols[c]:
            st.button(
                symbol,
                key=f"cell_{r}_{c}",
                use_container_width=True,
                disabled=(value != 0 or result is not None),
                on_click=make_move,
                args=(r, c)
            )

st.markdown('</div>', unsafe_allow_html=True)


# ---------------- SCOREBOARD ----------------

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 🏅 MATCH SCOREBOARD")

s1, s2, s3 = st.columns(3)

with s1:
    st.metric("PLAYER X", st.session_state.scores["X"])

with s2:
    st.metric("DRAWS", st.session_state.scores["DRAW"])

with s3:
    st.metric("PLAYER O", st.session_state.scores["O"])


# ---------------- CONTROLS ----------------

st.markdown("<br>", unsafe_allow_html=True)

st.button(
    "↻   PLAY AGAIN",
    type="primary",
    use_container_width=True,
    on_click=reset_game
)

if st.button("RESET ALL SCORES", use_container_width=True):
    st.session_state.scores = {"X": 0, "O": 0, "DRAW": 0}
    reset_game()

# ---------------- FOOTER ----------------

st.markdown("""
<div class="footer">
    BUILT WITH PYTHON & NUMPY<br><br>
    GAME ARENA © 2026
</div>
""", unsafe_allow_html=True)
