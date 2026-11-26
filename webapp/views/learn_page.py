import streamlit as st
from core import training

from views import nav
from views.state import level_info


def render():
    level, info, progress, acct = level_info()
    st.title("🎓 Learning Path")
    st.write(
        "Go from zero to an advanced, rule-based process. Each level unlocks by doing, "
        "not by reading: pass the quiz, practise on historical charts, then prove it "
        "on the demo account."
    )

    cols = st.columns(4)
    for n, lv in training.LEVELS.items():
        with cols[n - 1].container(border=True):
            mark = "✅" if n < level else ("👉" if n == level else "🔒")
            st.markdown(f"{mark} **Level {n}: {lv['name']}**")
            st.caption(lv["goal"])
            st.caption(f"Max risk/trade: **{lv['max_risk_pct']}%**")

    st.subheader("Your progress")
    replay = training.trade_stats(progress.replays)
    demo = training.trade_stats(acct["closed"] if acct else [])
    m = st.columns(4)
    m[0].metric(
        "Quiz",
        f"{progress.quiz_score}/{len(training.QUIZ)}",
        "passed" if training.quiz_passed(progress.quiz_score) else "not passed",
        delta_color="normal" if training.quiz_passed(progress.quiz_score) else "off",
    )
    m[1].metric(
        "Replay trades",
        f"{replay['trades']}/{training.REPLAYS_FOR_LEVEL_3}",
        f"{replay['expectancy_r']:+.2f}R avg" if replay["trades"] else None,
        delta_color="off",
    )
    m[2].metric("Demo trades closed", f"{demo['trades']}/{training.DEMO_TRADES_FOR_LEVEL_4}")
    m[3].metric("Demo expectancy", f"{demo['expectancy_r']:+.2f}R" if demo["trades"] else "—")
    if level < 4:
        st.info(f"**Next step:** {info['unlock']}")
    else:
        st.success("You've reached the top level. Keep journaling and reviewing.")

    st.subheader(f"Level {level} lessons: {info['name']}")
    for title, body in info["lessons"]:
        with st.expander(title):
            st.markdown(body)
    if level > 1:
        with st.expander("Review earlier levels"):
            for n in range(1, level):
                for title, body in training.LEVELS[n]["lessons"]:
                    st.markdown(f"**L{n} · {title}** — {body}")

    st.subheader("Basics quiz")
    with st.form("quiz_form"):
        answers = []
        for i, q in enumerate(training.QUIZ):
            choice = st.radio(f"{i + 1}. {q['q']}", q["options"], index=None, key=f"quiz_{i}")
            answers.append(q["options"].index(choice) if choice is not None else -1)
        if st.form_submit_button("Submit answers", type="primary"):
            score = training.grade_quiz(answers)
            progress.quiz_score = max(progress.quiz_score, score)
            training.save_progress(progress)
            if training.quiz_passed(score):
                st.success(f"{score}/{len(training.QUIZ)} — passed! Level 2 unlocked.")
            else:
                st.error(f"{score}/{len(training.QUIZ)} — review the lessons and try again.")
                for q, a in zip(training.QUIZ, answers):
                    if a != q["answer"]:
                        st.caption(f"✗ {q['q']} → **{q['options'][q['answer']]}**")

    c1, c2 = st.columns(2)
    if c1.button("▶ Practise on Chart Replay", use_container_width=True):
        nav.go("replay")
    if c2.button("💼 Open Demo Account", use_container_width=True):
        nav.go("demo")
