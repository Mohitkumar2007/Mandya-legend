import random
import time

import streamlit as st


st.set_page_config(
    page_title="Likhith M: Mandya Legend Challenge",
    page_icon="🌾",
    layout="centered",
)


st.markdown(
    """
    <style>
    .stApp {
        background:
          radial-gradient(circle at top right, rgba(255,193,7,.20), transparent 34%),
          linear-gradient(145deg, #fffdf5 0%, #f4ffe8 55%, #e8fff2 100%);
    }
    .block-container {max-width: 780px; padding-top: 1.6rem; padding-bottom: 3rem;}
    .hero {
        padding: 1.65rem 1.25rem;
        border-radius: 24px;
        background: linear-gradient(135deg, #173f2b, #287348);
        color: white;
        box-shadow: 0 16px 35px rgba(23,63,43,.22);
        text-align: center;
        margin-bottom: 1rem;
    }
    .hero h1 {font-size: clamp(1.8rem, 6vw, 2.7rem); margin: 0;}
    .hero p {font-size: 1.03rem; opacity: .9; margin: .55rem 0 0;}
    .score-card {
        background: rgba(255,255,255,.85);
        border: 1px solid rgba(40,115,72,.15);
        border-radius: 18px;
        padding: .9rem 1rem;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,.05);
    }
    .score-number {font-size: 2rem; font-weight: 800; color: #1f6b42;}
    .round-title {font-size: 1.35rem; font-weight: 800; color: #173f2b; margin-top: .3rem;}
    .fun-card {
        background: white;
        padding: 1rem 1.1rem;
        border-radius: 18px;
        border-left: 6px solid #f4b400;
        margin: .75rem 0;
        box-shadow: 0 8px 18px rgba(0,0,0,.045);
    }
    div.stButton > button {
        border-radius: 14px;
        min-height: 3rem;
        font-weight: 750;
        border: 1px solid rgba(31,107,66,.22);
    }
    .tiny {font-size: .82rem; color: #587065; text-align:center;}
    </style>
    """,
    unsafe_allow_html=True,
)


QUESTIONS = [
    {
        "question": "Mandya is especially famous for which crop?",
        "options": ["Coffee", "Sugarcane", "Tea", "Apples"],
        "answer": "Sugarcane",
        "fact": "Mandya is often called Karnataka's sugar bowl. Sweet place, sweeter people!",
    },
    {
        "question": "Which river is closely connected with Mandya's agriculture?",
        "options": ["Kaveri", "Yamuna", "Narmada", "Ganga"],
        "answer": "Kaveri",
        "fact": "The Kaveri and its canals support much of the district's farming.",
    },
    {
        "question": "Which famous bird sanctuary is in Mandya district?",
        "options": ["Ranganathittu", "Gudavi", "Kokkare Bellur", "Both A and C"],
        "answer": "Both A and C",
        "fact": "Mandya gets double bird points: Ranganathittu and Kokkare Bellur are both well known.",
    },
    {
        "question": "What is the safest fuel for Likhith's legendary confidence?",
        "options": ["One compliment", "Mysore Pak", "Full phone battery", "All of these"],
        "answer": "All of these",
        "fact": "Scientific proof: unavailable. Friendship proof: 100% confirmed.",
    },
    {
        "question": "If Likhith says 'five minutes', what does it usually mean?",
        "options": ["Exactly 5 minutes", "Already there", "Somewhere between 5 and 50", "Tomorrow"],
        "answer": "Somewhere between 5 and 50",
        "fact": "This is a friendly-joke question—the game accepts Mandya Standard Time!",
    },
]


def reset_game():
    keep_player = st.session_state.get("player_name", "")
    keep_target = st.session_state.get("target_name", "Likhith M")
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state.player_name = keep_player
    st.session_state.target_name = keep_target
    initialize()


def initialize():
    defaults = {
        "screen": "welcome",
        "score": 0,
        "question_index": 0,
        "quiz_questions": random.sample(QUESTIONS, 3),
        "answered": False,
        "reaction_started": False,
        "reaction_ready_at": None,
        "reaction_done": False,
        "reaction_result": None,
        "lucky_done": False,
        "lucky_winner": random.randint(0, 2),
        "player_name": "",
        "target_name": "Likhith M",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def header():
    st.markdown(
        f"""
        <div class="hero">
          <div style="font-size:2.2rem">🌾 👑 🎮</div>
          <h1>{st.session_state.target_name}: Mandya Legend Challenge</h1>
          <p>Three rounds. One legend. Unlimited friendly chaos.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def score_bar(round_name):
    left, middle, right = st.columns(3)
    with left:
        st.markdown(
            f'<div class="score-card"><div>Player</div><b>{st.session_state.player_name or "Guest"}</b></div>',
            unsafe_allow_html=True,
        )
    with middle:
        st.markdown(
            f'<div class="score-card"><div>Score</div><div class="score-number">{st.session_state.score}</div></div>',
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            f'<div class="score-card"><div>Now playing</div><b>{round_name}</b></div>',
            unsafe_allow_html=True,
        )


def welcome_screen():
    st.markdown(
        """
        <div class="fun-card">
        <b>Your mission:</b> prove that you can survive Mandya trivia, harvest
        sugarcane at lightning speed, and discover the lucky treasure box.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.session_state.player_name = st.text_input(
        "Your name",
        value=st.session_state.player_name,
        placeholder="Enter challenger name",
        max_chars=24,
    )
    with st.expander("Personalize the legend"):
        st.session_state.target_name = st.text_input(
            "Friend's name",
            value=st.session_state.target_name,
            max_chars=24,
        )
    if st.button("🚀 Start the challenge", type="primary", use_container_width=True):
        if not st.session_state.player_name.strip():
            st.warning("Enter your name before challenging the Mandya legend!")
        else:
            st.session_state.screen = "quiz"
            st.rerun()


def quiz_screen():
    score_bar("1 / 3 · Trivia")
    st.progress(st.session_state.question_index / 3)
    idx = st.session_state.question_index
    question = st.session_state.quiz_questions[idx]
    st.markdown('<p class="round-title">🧠 Mandya Brain Battle</p>', unsafe_allow_html=True)
    st.subheader(f"Question {idx + 1} of 3")

    choice = st.radio(
        question["question"],
        question["options"],
        key=f"q_{idx}",
        disabled=st.session_state.answered,
        index=None,
    )

    if not st.session_state.answered:
        if st.button("Lock answer 🔒", type="primary", use_container_width=True):
            if choice is None:
                st.warning("Pick an answer first!")
            else:
                st.session_state.answered = True
                st.session_state.last_correct = choice == question["answer"]
                if st.session_state.last_correct:
                    st.session_state.score += 10
                st.rerun()
    else:
        if st.session_state.last_correct:
            st.success(f"Correct! +10 points. {question['fact']}")
        else:
            st.error(f"Nice try! The answer is **{question['answer']}**. {question['fact']}")
        label = "Next question ➡️" if idx < 2 else "Enter the sugarcane field 🌾"
        if st.button(label, type="primary", use_container_width=True):
            st.session_state.answered = False
            if idx < 2:
                st.session_state.question_index += 1
            else:
                st.session_state.screen = "reaction"
            st.rerun()


def reaction_screen():
    score_bar("2 / 3 · Reaction")
    st.markdown('<p class="round-title">⚡ Sugarcane Speed Challenge</p>', unsafe_allow_html=True)
    st.info("Start the round. When the green HARVEST button appears, tap it as fast as you can!")

    if not st.session_state.reaction_started:
        if st.button("Start the tractor 🚜", type="primary", use_container_width=True):
            st.session_state.reaction_started = True
            st.session_state.reaction_ready_at = time.time() + random.uniform(1.8, 4.0)
            st.rerun()
        return

    if st.session_state.reaction_done:
        reaction = st.session_state.reaction_result
        if reaction < 0.35:
            points, comment = 20, "Lightning harvest! Even the tractor is impressed."
        elif reaction < 0.7:
            points, comment = 15, "Super quick—proper Mandya reflexes!"
        elif reaction < 1.3:
            points, comment = 10, "Good harvest. The sugarcane is safe."
        else:
            points, comment = 5, "A relaxed harvest is still a harvest!"
        if not st.session_state.get("reaction_scored", False):
            st.session_state.score += points
            st.session_state.reaction_scored = True
        st.success(f"Your reaction time: **{reaction:.3f} seconds** · +{points} points")
        st.write(comment)
        if st.button("Open the final lucky boxes 🎁", type="primary", use_container_width=True):
            st.session_state.screen = "lucky"
            st.rerun()
        return

    remaining = st.session_state.reaction_ready_at - time.time()
    if remaining > 0:
        st.warning("🟡 Tractor warming up… wait for green!")
        time.sleep(min(remaining, 0.35))
        st.rerun()
    else:
        st.success("🟢 GO! GO! GO!")
        if "go_shown_at" not in st.session_state:
            st.session_state.go_shown_at = time.time()
        if st.button("🌾 HARVEST NOW!", type="primary", use_container_width=True):
            st.session_state.reaction_result = max(0.001, time.time() - st.session_state.go_shown_at)
            st.session_state.reaction_done = True
            st.rerun()


def lucky_screen():
    score_bar("3 / 3 · Lucky Box")
    st.markdown('<p class="round-title">🎁 The Mandya Mystery Boxes</p>', unsafe_allow_html=True)
    st.write(f"One box contains the **Golden Mysore Pak**. Choose wisely, {st.session_state.player_name}!")

    labels = ["📦 Box A", "📦 Box B", "📦 Box C"]
    columns = st.columns(3)
    if not st.session_state.lucky_done:
        for index, column in enumerate(columns):
            with column:
                if st.button(labels[index], use_container_width=True):
                    st.session_state.lucky_done = True
                    st.session_state.chosen_box = index
                    if index == st.session_state.lucky_winner:
                        st.session_state.score += 25
                    else:
                        st.session_state.score += 5
                    st.rerun()
    else:
        chosen = st.session_state.chosen_box
        winner = st.session_state.lucky_winner
        if chosen == winner:
            st.balloons()
            st.success("🏆 You found the Golden Mysore Pak! +25 points")
        else:
            st.warning(f"Your box had a tiny sugarcane sticker! +5 points. The treasure was in Box {'ABC'[winner]}.")
        if st.button("See my legend result 👑", type="primary", use_container_width=True):
            st.session_state.screen = "result"
            st.rerun()


def result_screen():
    score = st.session_state.score
    if score >= 65:
        title = "Supreme Mandya Legend"
        emoji = "👑"
        message = "You may now challenge Likhith for the official crown."
        st.balloons()
    elif score >= 45:
        title = "Sugarcane Superstar"
        emoji = "🌟"
        message = "Fast reflexes, sharp brain, and excellent snack luck."
    elif score >= 25:
        title = "Mandya Explorer"
        emoji = "🚜"
        message = "A strong attempt. One more round and the crown could be yours."
    else:
        title = "Mysore Pak Trainee"
        emoji = "🍬"
        message = "The training arc has begun—and it looks delicious."

    st.markdown(
        f"""
        <div class="hero">
          <div style="font-size:4rem">{emoji}</div>
          <h1>{title}</h1>
          <p>{st.session_state.player_name} scored <b>{score} / 75</b></p>
          <p>{message}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="fun-card">
        <b>Official result:</b> {st.session_state.target_name} remains the Mandya legend—but
        <b>{st.session_state.player_name}</b> is now a certified challenger. Rematch recommended!
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("🔁 Play again", type="primary", use_container_width=True):
        reset_game()
        st.rerun()


initialize()
header()

screens = {
    "welcome": welcome_screen,
    "quiz": quiz_screen,
    "reaction": reaction_screen,
    "lucky": lucky_screen,
    "result": result_screen,
}
screens[st.session_state.screen]()

st.markdown("<p class='tiny'>Made for fun and friendship · No legends were harmed during development 😄</p>", unsafe_allow_html=True)

