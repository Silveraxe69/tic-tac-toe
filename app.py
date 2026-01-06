import streamlit as st
import time
import json
import os

# Load CSS + JS
st.set_page_config(layout="wide", page_title="Retro Tic Tac Toe")

# Inject CSS
with open("assets/style.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Inject JS
with open("assets/script.js", "r") as f:
    st.markdown(f"<script>{f.read()}</script>", unsafe_allow_html=True)

# ---- STATE INIT ----
if "screen" not in st.session_state:
    st.session_state.screen = "startup"  # startup → names → game

if "board" not in st.session_state:
    st.session_state.board = [""] * 9

if "turn" not in st.session_state:
    st.session_state.turn = "X"

if "winner" not in st.session_state:
    st.session_state.winner = None

if "timer" not in st.session_state:
    st.session_state.timer = 10


# GAME FUNCTIONS
def check_winner(board):
    combos = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for a, b, c in combos:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if "" not in board:
        return "Tie"
    return None


def reset_game():
    st.session_state.board = [""] * 9
    st.session_state.turn = "X"
    st.session_state.winner = None
    st.session_state.timer = 10


# ---- UI SCREENS ----

# 1️⃣ STARTUP SCREEN
if st.session_state.screen == "startup":
    st.markdown("""
    <div id="startup-screen" class="fade-screen">
        <div class="title-glow">TIC - TAC - TOE</div>
        <div class="press-start">Press SPACE to Start</div>
    </div>
    """, unsafe_allow_html=True)

# JS triggers change → Streamlit reruns
    st.session_state.screen = "startup"

# 2️⃣ NAME ENTRY SCREEN
elif st.session_state.screen == "names":

    st.markdown("""
    <div class="fade-screen">
        <h1 class="name-title">Enter Player Names</h1>
    </div>
    """, unsafe_allow_html=True)

    p1 = st.text_input("Player X Name", "Player X")
    p2 = st.text_input("Player O Name", "Player O")

    if st.button("Start Game", key="startgamebtn"):
        st.session_state.player1 = p1
        st.session_state.player2 = p2
        st.session_state.screen = "game"
        st.rerun()


# 3️⃣ GAME BOARD
elif st.session_state.screen == "game":

    # Header
    st.markdown(f"""
    <div class="header-title">🎮 Retro Cyber Tic Tac Toe</div>
    <div class="turn-indicator">Turn: {st.session_state.turn}</div>
    <div id="timer-bar"></div>
    """, unsafe_allow_html=True)

    # Board Grid Layout
    cols = st.columns(3)
    for i in range(9):
        with cols[i % 3]:
            cell_value = st.session_state.board[i] or " "
            if st.button(cell_value, key=f"cell_{i}", use_container_width=True):
                if st.session_state.board[i] == "" and not st.session_state.winner:
                    st.session_state.board[i] = st.session_state.turn

                    st.session_state.winner = check_winner(st.session_state.board)
                    if st.session_state.winner is None:
                        st.session_state.turn = "O" if st.session_state.turn == "X" else "X"
                        st.session_state.timer = 10
                    st.rerun()

    # Winner
    if st.session_state.winner:
        if st.session_state.winner == "Tie":
            st.markdown("<div class='winner'>It's a Draw!</div>", unsafe_allow_html=True)
        else:
            st.markdown(
                f"<div class='winner'>{st.session_state.winner} Wins!</div>",
                unsafe_allow_html=True
            )

    st.button("Restart Game", on_click=reset_game)
