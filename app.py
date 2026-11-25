
import streamlit as st
import numpy as np
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Tic Tac Toe | Neon Arena",
    page_icon="🎮",
    layout="centered"
)

# ---------------- SESSION STATE ----------------

if "board" not in st.session_state:
    st.session_state.board = np.zeros((3, 3), dtype=int)
if "current" not in st.session_state:
    st.session_state.current = 1
if "result" not in st.session_state:
    st.session_state.result = None
if "winning_cells" not in st.session_state:
    st.session_state.winning_cells = []
if "scores" not in st.session_state:
    st.session_state.scores = {"X": 0, "O": 0, "DRAW": 0}
if "celebrated" not in st.session_state:
    st.session_state.celebrated = False


# ---------------- GAME LOGIC ----------------

def check_winner(b):
    # Rows
    for r in range(3):
        if abs(np.sum(b[r, :])) == 3:
            return ("X" if b[r, 0] == 1 else "O",
                    [(r, c) for c in range(3)])

    # Columns
    for c in range(3):
        if abs(np.sum(b[:, c])) == 3:
            return ("X" if b[0, c] == 1 else "O",
                    [(r, c) for r in range(3)])

    # Main diagonal
    if np.trace(b) == 3:
        return "X", [(i, i) for i in range(3)]

    if np.trace(b) == -3:
        return "O", [(i, i) for i in range(3)]

    # Opposite diagonal
    diagonal = np.trace(np.fliplr(b))

    if diagonal == 3:
        return "X", [(i, 2-i) for i in range(3)]

    if diagonal == -3:
        return "O", [(i, 2-i) for i in range(3)]

    # Draw
    if not np.any(b == 0):
        return "DRAW", []

    return None, []


# ---------------- GAME ACTIONS ----------------

def make_move(r, c):
    if st.session_state.result is not None:
        return

    board = st.session_state.board

    if board[r, c] != 0:
        return

    board[r, c] = st.session_state.current

    winner, cells = check_winner(board)

    if winner is not None:
        st.session_state.result = winner
        st.session_state.winning_cells = cells
        st.session_state.scores[winner] += 1
        st.session_state.celebrated = False
    else:
        st.session_state.current *= -1


def reset_game():
    st.session_state.board = np.zeros((3, 3), dtype=int)
    st.session_state.current = 1
    st.session_state.result = None
    st.session_state.winning_cells = []
    st.session_state.celebrated = False


def reset_all():
    reset_game()
    st.session_state.scores = {"X": 0, "O": 0, "DRAW": 0}


# ---------------- WINNING LINE SVG ----------------

def get_winning_line(cells):
    if not cells:
        return ""

    # SVG viewBox: 300 x 330
    positions = {
        (0, 0): (50, 50),   (0, 1): (150, 50),  (0, 2): (250, 50),
        (1, 0): (50, 165),  (1, 1): (150, 165), (1, 2): (250, 165),
        (2, 0): (50, 280),  (2, 1): (150, 280), (2, 2): (250, 280)
    }

    x1, y1 = positions[cells[0]]
    x2, y2 = positions[cells[2]]

    return f"""
    <svg class="win-overlay"
         viewBox="0 0 300 330"
         preserveAspectRatio="none">
        <defs>
            <filter id="glow">
                <feGaussianBlur stdDeviation="5" result="blur"/>
                <feMerge>
                    <feMergeNode in="blur"/>
                    <feMergeNode in="SourceGraphic"/>
                </feMerge>
            </filter>
        </defs>
        <line
            x1="{x1}" y1="{y1}"
            x2="{x2}" y2="{y2}"
            stroke="#38bdf8"
            stroke-width="7"
            stroke-linecap="round"
            filter="url(#glow)"
            class="draw-line"
        />
    </svg>
    """


# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

* {
    font-family: Inter, sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 10% 10%, rgba(37,99,235,.20), transparent 40%),
        radial-gradient(ellipse at 90% 85%, rgba(124,58,237,.20), transparent 40%),
        #070b16;
    color: white;
}

header, footer, #MainMenu {
    visibility: hidden;
}

.block-container {
    max-width: 650px;
    padding: 35px 18px 45px;
}

/* Ambient gaming background */

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(96,165,250,.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(96,165,250,.025) 1px, transparent 1px);
    background-size: 45px 45px;
    pointer-events: none;
    z-index: 0;
}

/* Header */

.hero {
    text-align: center;
    margin-bottom: 30px;
}

.tag {
    display: inline-block;
    border: 1px solid #36517e;
    background: rgba(30,64,120,.25);
    color: #7dd3fc;
    padding: 7px 17px;
    border-radius: 30px;
    font-size: 10px;
    letter-spacing: 3px;
    font-weight: 800;
}

.hero h1 {
    font-size: clamp(38px, 8vw, 55px);
    font-weight: 900;
    letter-spacing: -3px;
    margin: 12px 0 0;
    background: linear-gradient(90deg,#fff,#60a5fa,#c4b5fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #8493ad;
    font-size: 12px;
    letter-spacing: 2px;
}

/* Player cards */

.players {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-bottom: 18px;
}

.player {
    padding: 17px;
    border-radius: 17px;
    background: rgba(19,31,53,.85);
    border: 1px solid #293b59;
    text-align: center;
    transition: .3s;
}

.player-x.active {
    border-color: #38bdf8;
    box-shadow: 0 0 24px rgba(56,189,248,.2);
}

.player-o.active {
    border-color: #c084fc;
    box-shadow: 0 0 24px rgba(192,132,252,.2);
}

.symbol {
    font-size: 30px;
    font-weight: 900;
}

.blue { color: #38bdf8; }
.purple { color: #c084fc; }

.player-name {
    font-size: 12px;
    font-weight: 800;
    margin-top: 6px;
}

.player-status {
    font-size: 9px;
    color: #94a3b8;
    letter-spacing: 1px;
    margin-top: 5px;
}

/* Status */

.status {
    padding: 15px;
    background: rgba(18,31,53,.9);
    border: 1px solid #293d5d;
    border-radius: 14px;
    text-align: center;
    color: #dbeafe;
    font-weight: 700;
    font-size: 13px;
    margin-bottom: 20px;
}

.winner-status {
    color: #fde68a;
    border-color: #a78bfa;
    background: linear-gradient(90deg,rgba(30,41,80,.9),rgba(76,29,149,.25));
    animation: pulse 1.5s infinite alternate;
}

@keyframes pulse {
    from { box-shadow: 0 0 8px rgba(167,139,250,.15); }
    to { box-shadow: 0 0 25px rgba(167,139,250,.4); }
}

/* Board */

.st-key-game_board {
    position: relative;
    background: linear-gradient(145deg,#15243d,#0d1729);
    border: 1px solid #354b6c;
    border-radius: 22px;
    padding: 13px;
    box-shadow: 0 20px 60px rgba(0,0,0,.45),
                inset 0 1px 1px rgba(255,255,255,.05);
}

.st-key-game_board button {
    height: clamp(88px, 19vw, 115px) !important;
    border-radius: 16px !important;
    background: linear-gradient(145deg,#1d304e,#142139) !important;
    border: 1px solid #344a69 !important;
    color: #38bdf8 !important;
    font-size: clamp(34px,8vw,48px) !important;
    font-weight: 900 !important;
    box-shadow: 0 5px 15px rgba(0,0,0,.25);
    transition: all .2s ease !important;
}

.st-key-game_board button:hover:not(:disabled) {
    transform: scale(1.035);
    background: #263e60 !important;
    border-color: #60a5fa !important;
    box-shadow: 0 0 22px rgba(56,189,248,.18);
}

.st-key-game_board button:disabled {
    opacity: 1 !important;
    cursor: default !important;
}

.st-key-game_board button:focus {
    box-shadow: none !important;
}

/* Winning cells */

.st-key-game_board .st-key-cell_0_0 button,
.st-key-game_board .st-key-cell_0_1 button,
.st-key-game_board .st-key-cell_0_2 button,
.st-key-game_board .st-key-cell_1_0 button,
.st-key-game_board .st-key-cell_1_1 button,
.st-key-game_board .st-key-cell_1_2 button,
.st-key-game_board .st-key-cell_2_0 button,
.st-key-game_board .st-key-cell_2_1 button,
.st-key-game_board .st-key-cell_2_2 button {
    transition: all .3s ease;
}

/* SVG overlay */

.win-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    overflow: visible;
    z-index: 50;
}

.draw-line {
    stroke-dasharray: 400;
    stroke-dashoffset: 400;
    animation: draw 0.7s ease-out forwards;
}

@keyframes draw {
    to { stroke-dashoffset: 0; }
}

/* Scoreboard */

div[data-testid="stMetric"] {
    background: rgba(19,31,53,.85);
    border: 1px solid #293d5b;
    padding: 13px;
    border-radius: 14px;
}

div[data-testid="stMetricValue"] {
    color: white;
    font-weight: 900;
}

div[data-testid="stMetricLabel"] {
    color: #9aabc4;
}

/* Buttons */

div.stButton > button[kind="primary"] {
    height: 53px;
    border-radius: 13px;
    background: linear-gradient(90deg,#2563eb,#7c3aed);
    border: none;
    color: white;
    font-weight: 800;
    letter-spacing: 1px;
}

div.stButton > button:not([kind="primary"]) {
    border-radius: 12px;
}

.footer {
    text-align: center;
    font-size: 10px;
    color: #64748b;
    letter-spacing: 2px;
    margin-top: 28px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">
    <div class="tag">✦ NEON GAME ARENA ✦</div>
    <h1>TIC TAC TOE</h1>
    <p>THINK FAST. MAKE YOUR MOVE.</p>
</div>
""", unsafe_allow_html=True)


# ---------------- PLAYER DISPLAY ----------------

current = st.session_state.current
result = st.session_state.result

st.markdown(f"""
<div class="players">
    <div class="player player-x {'active' if current == 1 and result is None else ''}">
        <div class="symbol blue">X</div>
        <div class="player-name">PLAYER ONE</div>
        <div class="player-status">
            {'● PLAYING NOW' if current == 1 and result is None else 'READY'}
        </div>
    </div>
    <div class="player player-o {'active' if current == -1 and result is None else ''}">
        <div class="symbol purple">O</div>
        <div class="player-name">PLAYER TWO</div>
        <div class="player-status">
            {'● PLAYING NOW' if current == -1 and result is None else 'READY'}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------- GAME STATUS ----------------

if result is None:
    player = "X" if current == 1 else "O"
    message = f"⚡ PLAYER {player} — YOUR TURN"
    status_class = "status"
elif result == "DRAW":
    message = "🤝 IT'S A DRAW! WELL PLAYED"
    status_class = "status winner-status"
else:
    message = f"🏆 PLAYER {result} WINS!"
    status_class = "status winner-status"

st.markdown(
    f'<div class="{status_class}">{message}</div>',
    unsafe_allow_html=True
)


# ---------------- BOARD ----------------

with st.container(key="game_board"):
    board = st.session_state.board

    for r in range(3):
        cols = st.columns(3, gap="small")

        for c in range(3):
            value = board[r, c]

            symbol = " " if value == 0 else (
                "X" if value == 1 else "O"
            )

            with cols[c]:
                st.button(
                    symbol,
                    key=f"cell_{r}_{c}",
                    use_container_width=True,
                    disabled=(value != 0 or result is not None),
                    on_click=make_move,
                    args=(r, c)
                )

    if result in ("X", "O"):
        st.markdown(
            get_winning_line(st.session_state.winning_cells),
            unsafe_allow_html=True
        )


# ---------------- CELEBRATION ----------------

if result in ("X", "O") and not st.session_state.celebrated:
    st.session_state.celebrated = True
    st.balloons()

elif result == "DRAW" and not st.session_state.celebrated:
    st.session_state.celebrated = True
    st.snow()


# ---------------- SCOREBOARD ----------------

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 🏆 MATCH STATISTICS")

a, b, c = st.columns(3)

with a:
    st.metric("X WINS", st.session_state.scores["X"])

with b:
    st.metric("DRAWS", st.session_state.scores["DRAW"])

with c:
    st.metric("O WINS", st.session_state.scores["O"])


# ---------------- CONTROLS ----------------

st.markdown("<br>", unsafe_allow_html=True)

st.button(
    "↻   PLAY AGAIN",
    type="primary",
    use_container_width=True,
    on_click=reset_game
)

if st.button("RESET MATCH & SCORES", use_container_width=True):
    reset_all()

st.markdown("""
<div class="footer">
    NEON ARENA · POWERED BY PYTHON & NUMPY
</div>
""", unsafe_allow_html=True)
