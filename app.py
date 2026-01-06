import streamlit as st

st.set_page_config(page_title="Multiplayer Tic Tac Toe", layout="centered")

# Initialize game state
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
if "turn" not in st.session_state:
    st.session_state.turn = "X"
if "winner" not in st.session_state:
    st.session_state.winner = None
if "started" not in st.session_state:
    st.session_state.started = False


def reset_game():
    st.session_state.board = [""] * 9
    st.session_state.turn = "X"
    st.session_state.winner = None


def check_winner(board):
    combos = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    for a, b, c in combos:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if "" not in board:
        return "Tie"
    return None


# ---------------------------
#   NAME INPUT PAGE
# ---------------------------
if not st.session_state.started:

    st.title("🎮 Multiplayer Tic Tac Toe")
    st.subheader("Enter your names to start the game")

    player1 = st.text_input("Player 1 Name (X):")
    player2 = st.text_input("Player 2 Name (O):")

    if st.button("Start Game"):
        if player1.strip() == "" or player2.strip() == "":
            st.error("Please enter both names!")
        else:
            st.session_state.player1 = player1
            st.session_state.player2 = player2
            st.session_state.started = True
            st.rerun()

    st.stop()



# ---------------------------
#   GAME BOARD PAGE
# ---------------------------

st.title("🎯 Tic Tac Toe")

st.subheader(f"Turn: {st.session_state.player1 if st.session_state.turn=='X' else st.session_state.player2} ({st.session_state.turn})")

cols = st.columns(3)

for i in range(9):
    with cols[i % 3]:
        if st.button(st.session_state.board[i] or " ", key=i, use_container_width=True):
            if st.session_state.board[i] == "" and not st.session_state.winner:
                st.session_state.board[i] = st.session_state.turn
                st.session_state.winner = check_winner(st.session_state.board)
                st.session_state.turn = "O" if st.session_state.turn == "X" else "X"
                st.rerun()


# ---------------------------
#   WINNER DISPLAY
# ---------------------------

if st.session_state.winner:
    if st.session_state.winner == "Tie":
        st.success("🤝 It's a Tie!")
    else:
        winner_name = st.session_state.player1 if st.session_state.winner == "X" else st.session_state.player2
        st.success(f"🏆 Winner: {winner_name} ({st.session_state.winner})")

    st.button("🔄 Restart Game", on_click=reset_game)

