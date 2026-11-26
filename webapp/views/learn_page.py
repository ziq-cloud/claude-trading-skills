import streamlit as st
from core import training

from views import nav
from views.lang import t
from views.state import level_info


def render():
    level, info, progress, acct = level_info()
    st.title("🎓 " + t("nav.learn"))
    st.write(t("learn.intro"))

    cols = st.columns(4)
    for n, lv in training.LEVELS.items():
        with cols[n - 1].container(border=True):
            mark = "✅" if n < level else ("👉" if n == level else "🔒")
            st.markdown(f"{mark} **{t('side.level', n=n, name=t(f'level.{n}.name'))}**")
            st.caption(t(f"level.{n}.goal"))
            st.caption(t("learn.max_risk", pct=lv["max_risk_pct"]))

    st.subheader(t("learn.progress"))
    replay = training.trade_stats(progress.replays)
    demo = training.trade_stats(acct["closed"] if acct else [])
    passed = training.quiz_passed(progress.quiz_score)
    m = st.columns(4)
    m[0].metric(
        t("learn.m_quiz"),
        f"{progress.quiz_score}/{len(training.QUIZ)}",
        t("learn.passed") if passed else t("learn.not_passed"),
        delta_color="normal" if passed else "off",
    )
    m[1].metric(
        t("learn.m_replays"),
        f"{replay['trades']}/{training.REPLAYS_FOR_LEVEL_3}",
        t("learn.avg_r", r=f"{replay['expectancy_r']:+.2f}") if replay["trades"] else None,
        delta_color="off",
    )
    m[2].metric(t("learn.m_demo"), f"{demo['trades']}/{training.DEMO_TRADES_FOR_LEVEL_4}")
    m[3].metric(t("learn.m_expect"), f"{demo['expectancy_r']:+.2f}R" if demo["trades"] else "—")
    if level < 4:
        st.info(t("learn.next", unlock=info["unlock"]))
    else:
        st.success(t("learn.top"))

    st.subheader(t("learn.lessons", n=level, name=info["name"]))
    for lesson in info["lessons"]:
        with st.expander(t(f"lesson.{lesson}.title")):
            st.markdown(t(f"lesson.{lesson}.body"))
    if level > 1:
        with st.expander(t("learn.review")):
            for n in range(1, level):
                for lesson in training.LEVELS[n]["lessons"]:
                    st.markdown(
                        f"**L{n} · {t(f'lesson.{lesson}.title')}** — {t(f'lesson.{lesson}.body')}"
                    )

    st.subheader(t("learn.quiz"))
    with st.form("quiz_form"):
        answers = []
        for i, _ in enumerate(training.QUIZ, start=1):
            opts = t(f"quiz.{i}.opts")
            choice = st.radio(
                f"{i}. {t(f'quiz.{i}.q')}",
                range(len(opts)),
                index=None,
                format_func=lambda k, o=opts: o[k],
                key=f"quiz_{i}",
            )
            answers.append(-1 if choice is None else choice)
        if st.form_submit_button(t("learn.submit"), type="primary"):
            score = training.grade_quiz(answers)
            progress.quiz_score = max(progress.quiz_score, score)
            training.save_progress(progress)
            total = len(training.QUIZ)
            if training.quiz_passed(score):
                st.success(t("learn.quiz_pass", score=score, total=total))
            else:
                st.error(t("learn.quiz_fail", score=score, total=total))
                for i, (q, a) in enumerate(zip(training.QUIZ, answers), start=1):
                    if a != q["answer"]:
                        st.caption(f"✗ {t(f'quiz.{i}.q')} → **{t(f'quiz.{i}.opts')[q['answer']]}**")

    c1, c2 = st.columns(2)
    if c1.button(t("learn.btn_replay"), use_container_width=True):
        nav.go("replay")
    if c2.button(t("learn.btn_demo"), use_container_width=True):
        nav.go("demo")
