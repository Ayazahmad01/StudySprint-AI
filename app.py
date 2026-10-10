
import os
import json
import re
import unicodedata
from difflib import SequenceMatcher

import streamlit as st
from dotenv import load_dotenv
from openai import (
    OpenAI,
    APIError,
    AuthenticationError,
    RateLimitError,
    APIConnectionError,
)

load_dotenv()

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="StudySprint AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# PROFESSIONAL UI THEME
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --primary: #5546e8;
        --primary-dark: #4032c5;
        --text: #172033;
        --muted: #68738a;
        --border: #e7eaf2;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        color: var(--text);
    }

    .stApp {
        background:
            radial-gradient(
                ellipse at 10% 0%,
                rgba(85,70,232,0.08),
                transparent 35%
            ),
            #f8f9fc;
    }

    .block-container {
        max-width: 1120px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        font-family: 'Manrope', sans-serif !important;
        letter-spacing: -0.035em;
        color: var(--text);
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 26px;
    }

    .brand-icon {
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #7668ff, #4b3cdb);
        border-radius: 15px;
        font-size: 25px;
        box-shadow: 0 7px 18px rgba(85,70,232,.2);
    }

    .brand-name {
        font-family: 'Manrope', sans-serif;
        font-size: 21px;
        font-weight: 800;
        letter-spacing: -0.8px;
    }

    .brand-caption {
        font-size: 13px;
        color: var(--muted);
        margin-top: 2px;
    }

    .hero {
        padding: 34px;
        border: 1px solid #e4e1ff;
        border-radius: 24px;
        background: linear-gradient(120deg, #ffffff, #f1f0ff);
        margin-bottom: 28px;
    }

    .eyebrow {
        display: inline-block;
        padding: 6px 11px;
        border: 1px solid #e0dcff;
        border-radius: 50px;
        background: #ffffff;
        color: var(--primary);
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 13px;
    }

    .hero-title {
        font-family: 'Manrope', sans-serif;
        font-size: clamp(28px, 4vw, 43px);
        line-height: 1.18;
        font-weight: 800;
        letter-spacing: -1.8px;
        max-width: 720px;
        margin-bottom: 12px;
    }

    .hero-description {
        color: var(--muted);
        font-size: 16px;
        line-height: 1.8;
        max-width: 680px;
        margin-bottom: 0;
    }

    .section-title {
        font-family: 'Manrope', sans-serif;
        font-size: 23px;
        font-weight: 800;
        letter-spacing: -0.8px;
        margin-bottom: 5px;
    }

    .section-description {
        color: var(--muted);
        font-size: 14px;
        margin-bottom: 18px;
    }

    .activity-card {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 21px;
        min-height: 158px;
        margin-bottom: 15px;
    }

    .activity-icon {
        font-size: 25px;
        margin-bottom: 12px;
    }

    .activity-title {
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 7px;
    }

    .activity-description {
        font-size: 13px;
        color: var(--muted);
        line-height: 1.7;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255,255,255,.96);
        border-color: var(--border) !important;
        border-radius: 19px !important;
    }

    .stButton > button,
    .stFormSubmitButton > button,
    .stDownloadButton > button {
        min-height: 46px;
        border-radius: 11px;
        font-weight: 700;
        transition: all .2s ease;
    }

    .stButton > button[kind="primary"],
    .stFormSubmitButton > button[kind="primary"] {
        background: var(--primary);
        border: 1px solid var(--primary);
        color: white;
        box-shadow: 0 5px 14px rgba(85,70,232,.17);
    }

    .stButton > button[kind="primary"]:hover,
    .stFormSubmitButton > button[kind="primary"]:hover {
        background: var(--primary-dark);
        border-color: var(--primary-dark);
        transform: translateY(-1px);
    }

    [data-testid="stWidgetLabel"] {
        font-weight: 600;
        color: #34405a;
    }

    .tip {
        color: var(--muted);
        font-size: 13px;
        line-height: 1.7;
        padding-top: 5px;
    }

    .footer {
        text-align: center;
        color: #8790a4;
        font-size: 12px;
        padding-top: 24px;
    }

    @media (max-width: 700px) {
        .block-container {
            padding: 1rem 1rem 2rem;
        }

        .hero {
            padding: 23px;
            border-radius: 18px;
        }

        .hero-title {
            letter-spacing: -1px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# BRAND HEADER
# ============================================================

st.markdown(
    """
    <div class="brand">
        <div class="brand-icon">🎓</div>
        <div>
            <div class="brand-name">StudySprint AI</div>
            <div class="brand-caption">
                Your personal learning companion
            </div>
        </div>
    </div>

    <div class="hero">
        <div class="eyebrow">✦ LEARN AT YOUR OWN PACE</div>
        <div class="hero-title">
            Your next learning breakthrough starts here.
        </div>
        <p class="hero-description">
            Explore concepts, practise your knowledge, and take one
            confident step forward at a time.
        </p>
    </div>

    <div class="section-title">
        What would you like to do today?
    </div>
    <div class="section-description">
        Choose a learning activity and let your AI tutor guide you.
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# ACTIVITY CARDS
# ============================================================

card1, card2 = st.columns(2, gap="medium")

with card1:
    st.markdown(
        """
        <div class="activity-card">
            <div class="activity-icon">💡</div>
            <div class="activity-title">Understand a topic</div>
            <div class="activity-description">
                Learn difficult concepts with simple explanations,
                practical examples, and a practice exercise.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with card2:
    st.markdown(
        """
        <div class="activity-card">
            <div class="activity-icon">🧩</div>
            <div class="activity-title">Test your knowledge</div>
            <div class="activity-description">
                Answer questions, get your score, review explanations,
                and discover what to study next.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# AI CLIENT
# ============================================================

SYSTEM_INSTRUCTION = """
You are StudySprint AI, an accurate and friendly university tutor.

Use clear, level-appropriate explanations.
Never claim to have executed code unless you actually did.

For lessons, explain concepts step by step and finish with
a manageable next task.

For quiz JSON, follow the requested schema exactly.
Make each question unambiguous with one objectively correct answer.
Use plausible distractors. Check the answer key and explanation
against the question before returning.

Return JSON only when JSON is requested.
"""


def create_ai_client():
    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    base_url = os.getenv(
        "OPENAI_BASE_URL",
        "https://bedrock-mantle.eu-north-1.api.aws/v1",
    ).strip()

    model_id = os.getenv(
        "BEDROCK_MODEL_ID",
        "openai.gpt-oss-120b",
    ).strip()

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is missing. Check your .env file."
        )

    if not model_id:
        raise ValueError(
            "BEDROCK_MODEL_ID is missing from your .env file."
        )

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
        timeout=120.0,
        max_retries=2,
    )

    return client, model_id


def ask_tutor(
    client,
    model_id,
    prompt,
    max_tokens=1800,
    temperature=0.3,
):
    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_INSTRUCTION,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        max_tokens=max_tokens,
        temperature=temperature,
    )

    return (
        response.choices[0].message.content or ""
    ).strip()


# ============================================================
# QUIZ VALIDATION AND DUPLICATE DETECTION
# ============================================================

def parse_json_response(text):
    """Parse JSON, including a response accidentally wrapped in fences."""
    cleaned = text.strip()

    cleaned = re.sub(
        r"^```(?:json)?\s*",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start >= 0 and end > start:
            return json.loads(cleaned[start:end + 1])

        raise ValueError(
            "The AI did not return valid quiz JSON. Please try again."
        )


def normalize_question(text):
    """Normalize question text for duplicate detection."""
    text = unicodedata.normalize("NFKC", text).lower()
    text = re.sub(r"`[^`]*`", " code ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)

    return " ".join(text.split())


def is_duplicate_question(question, existing_questions):
    normalized = normalize_question(question)

    if not normalized:
        return True

    for old_question in existing_questions:
        old_normalized = normalize_question(old_question)

        if normalized == old_normalized:
            return True

        # Fuzzy matching for questions with similar wording.
        if min(len(normalized), len(old_normalized)) >= 30:
            similarity = SequenceMatcher(
                None,
                normalized,
                old_normalized,
            ).ratio()

            if similarity >= 0.86:
                return True

    return False


def validate_question(question, number):
    """Validate quiz structure and basic answer-key consistency."""
    if not isinstance(question, dict):
        raise ValueError(
            f"Question {number} must be a JSON object."
        )

    required = {
        "question",
        "options",
        "correct_answer",
        "explanation",
    }

    missing = required - set(question)

    if missing:
        raise ValueError(
            f"Question {number} is missing: "
            + ", ".join(sorted(missing))
        )

    stem = str(question["question"]).strip()
    explanation = str(question["explanation"]).strip()
    options = question["options"]

    correct = str(
        question["correct_answer"]
    ).strip().upper()

    if len(stem) < 8:
        raise ValueError(
            f"Question {number} has insufficient question text."
        )

    if not explanation:
        raise ValueError(
            f"Question {number} has no explanation."
        )

    if not isinstance(options, dict):
        raise ValueError(
            f"Question {number} options must be an object."
        )

    if set(options.keys()) != {"A", "B", "C", "D"}:
        raise ValueError(
            f"Question {number} must contain options A, B, C, and D."
        )

    options = {
        letter: str(options[letter]).strip()
        for letter in "ABCD"
    }

    if any(not value for value in options.values()):
        raise ValueError(
            f"Question {number} has an empty option."
        )

    unique_options = {
        value.casefold()
        for value in options.values()
    }

    if len(unique_options) != 4:
        raise ValueError(
            f"Question {number} has duplicate answer options."
        )

    if correct not in {"A", "B", "C", "D"}:
        raise ValueError(
            f"Question {number} has an invalid correct answer."
        )

    question["question"] = stem
    question["options"] = options
    question["correct_answer"] = correct
    question["explanation"] = explanation
    question["topic_tag"] = str(
        question.get("topic_tag", "General")
    ).strip() or "General"

    return question


def generate_quiz_batch(
    client,
    model_id,
    subject,
    topic,
    level,
    count,
    existing_questions,
    existing_topics,
    start_number,
):
    """Generate and validate one batch; reject duplicates and retry."""

    accepted = []
    seen_questions = list(existing_questions)
    seen_topics = list(existing_topics)

    for attempt in range(3):
        needed = count - len(accepted)

        if needed <= 0:
            break

        avoid_questions = "\n".join(
            f"- {question}"
            for question in seen_questions[-40:]
        ) or "- None"

        avoid_topics = ", ".join(
            seen_topics[-40:]
        ) or "None"

        prompt = f"""
Create exactly {needed} NEW multiple-choice quiz questions.

Subject: {subject}
Topic: {topic}
Difficulty: {level}

Return JSON only, using this structure:
{{
  "questions": [
    {{
      "question": "Question text?",
      "options": {{
        "A": "First option",
        "B": "Second option",
        "C": "Third option",
        "D": "Fourth option"
      }},
      "correct_answer": "A",
      "explanation": "Why this answer is correct.",
      "topic_tag": "Short concept name"
    }}
  ]
}}

Rules:
- Return exactly {needed} questions.
- Each question must have four non-empty options: A, B, C, D.
- Exactly one option must be correct.
- correct_answer must be the correct option letter.
- Explanation must support the selected correct answer.
- Use plausible but clearly incorrect distractors.
- Avoid ambiguous or trick questions.
- Do not repeat or paraphrase existing questions.
- Prefer different concepts or reasoning tasks.
- Avoid repeating these existing questions:
{avoid_questions}
- Existing concept labels to vary where possible:
{avoid_topics}
- Review the correctness of every question and answer key before returning.
"""

        raw = ask_tutor(
            client,
            model_id,
            prompt,
            max_tokens=max(1800, needed * 500),
            temperature=0.2,
        )

        data = parse_json_response(raw)

        if not isinstance(data, dict):
            raise ValueError(
                "Quiz response must be a JSON object."
            )

        items = data.get("questions")

        if not isinstance(items, list):
            raise ValueError(
                "Quiz JSON must contain a questions list."
            )

        for item in items:
            if len(accepted) >= count:
                break

            # Skip malformed individual items and ask the model
            # for replacements in a subsequent attempt.
            try:
                candidate = validate_question(
                    item,
                    start_number + len(accepted),
                )
            except ValueError:
                continue

            if is_duplicate_question(
                candidate["question"],
                seen_questions,
            ):
                continue

            accepted.append(candidate)
            seen_questions.append(candidate["question"])
            seen_topics.append(candidate["topic_tag"])

    if len(accepted) != count:
        raise RuntimeError(
            f"Only {len(accepted)} of {count} valid, "
            "non-duplicate questions could be generated after "
            "3 attempts. Try fewer questions or a broader topic."
        )

    return accepted


# ============================================================
# LEARNING SESSION FORM
# ============================================================

st.markdown(
    """
    <div class="section-title">Build your learning session</div>
    <div class="section-description">
        Select your topic, learning level, and preferred activity.
    </div>
    """,
    unsafe_allow_html=True,
)

with st.container(border=True):
    with st.form("learning_form"):
        mode = st.radio(
            "Choose your activity",
            ["Explain a topic", "Create a quiz"],
            horizontal=True,
        )

        col1, col2 = st.columns(2, gap="large")

        with col1:
            subject = st.selectbox(
                "Subject",
                [
                    "Python Programming",
                    "Machine Learning",
                    "Data Science",
                    "Database Systems",
                    "Computer Science",
                    "Other",
                ],
            )

        with col2:
            level = st.selectbox(
                "Your current level",
                ["Beginner", "Intermediate", "Advanced"],
            )

        topic = st.text_input(
            "What would you like to learn?",
            placeholder="e.g. Python loops, KNN, correlation heatmaps",
            help="Enter one specific topic for the best results.",
        )

        question_count = 10

        if mode == "Create a quiz":
            question_count = st.number_input(
                "How many questions do you want?",
                min_value=1,
                max_value=200,
                value=10,
                step=1,
                help="Large quizzes are generated in batches.",
            )

        st.markdown(
            """
            <div class="tip">
                ✨ <b>Learning tip:</b> Choose a topic and let your
                AI tutor guide you step by step.
            </div>
            """,
            unsafe_allow_html=True,
        )

        start = st.form_submit_button(
            "Start my learning session →",
            type="primary",
            use_container_width=True,
        )


# ============================================================
# GENERATE SESSION
# ============================================================

if start:
    # Clear previous session results when a new session begins.
    for key in (
        "active_quiz",
        "quiz_submitted",
        "quiz_meta",
        "quiz_user_answers",
        "lesson_result",
    ):
        st.session_state.pop(key, None)

    if not topic.strip():
        st.warning("Please enter the topic you want to learn.")

    else:
        try:
            client, model_id = create_ai_client()

            # ------------------------------------------------
            # EXPLAIN A TOPIC
            # ------------------------------------------------

            if mode == "Explain a topic":
                prompt = f"""
Activity: Explain a topic
Subject: {subject}
Topic: {topic.strip()}
Student level: {level}

Use these sections:
1. Core Idea
2. Simple Explanation
3. Practical Example
4. Common Mistakes
5. Practice Exercise

Use suitable examples and code where helpful.
Finish with "Your Next Move" and one manageable task.
"""

                with st.spinner(
                    "Your AI tutor is preparing your lesson..."
                ):
                    answer = ask_tutor(
                        client,
                        model_id,
                        prompt,
                        max_tokens=2500,
                    )

                if answer:
                    st.session_state["lesson_result"] = {
                        "answer": answer,
                        "subject": subject,
                        "level": level,
                        "topic": topic.strip(),
                    }
                else:
                    st.warning(
                        "The tutor returned an empty response. Try again."
                    )

            # ------------------------------------------------
            # CREATE AN INTERACTIVE QUIZ
            # ------------------------------------------------

            else:
                total = int(question_count)
                batch_size = 5
                batches = (total + batch_size - 1) // batch_size

                quiz = []
                progress = st.progress(
                    0,
                    text="Preparing your quiz...",
                )

                with st.spinner(
                    "Generating questions and checking for duplicates..."
                ):
                    for batch_index in range(batches):
                        count = min(
                            batch_size,
                            total - len(quiz),
                        )

                        new_questions = generate_quiz_batch(
                            client=client,
                            model_id=model_id,
                            subject=subject,
                            topic=topic.strip(),
                            level=level,
                            count=count,
                            existing_questions=[
                                q["question"] for q in quiz
                            ],
                            existing_topics=[
                                q["topic_tag"] for q in quiz
                            ],
                            start_number=len(quiz) + 1,
                        )

                        quiz.extend(new_questions)

                        progress.progress(
                            len(quiz) / total,
                            text=(
                                f"Validated {len(quiz)} "
                                f"of {total} questions..."
                            ),
                        )

                progress.empty()

                st.session_state["active_quiz"] = quiz
                st.session_state["quiz_submitted"] = False
                st.session_state["quiz_user_answers"] = {}
                st.session_state["quiz_meta"] = {
                    "subject": subject,
                    "topic": topic.strip(),
                    "level": level,
                }

        except ValueError as error:
            st.error(str(error))

        except AuthenticationError:
            st.error(
                "Authentication failed. Check your Bedrock API key. "
                "If it has expired, create a new one."
            )

        except RateLimitError:
            st.error(
                "The model is busy or the quota was reached. "
                "Wait a little and try again."
            )

        except APIConnectionError:
            st.error(
                "Could not connect to Bedrock Mantle. "
                "Check your internet connection and OPENAI_BASE_URL."
            )

        except APIError as error:
            st.error("Your AI tutor could not complete the request.")
            st.caption(
                f"API error: {type(error).__name__}: {error}"
            )

        except RuntimeError as error:
            st.error("Quiz generation could not be completed.")
            st.caption(str(error))

        except json.JSONDecodeError:
            st.error(
                "The AI returned invalid JSON. Please try again."
            )

        except Exception as error:
            st.error("An unexpected error occurred.")
            st.caption(
                f"{type(error).__name__}: {error}"
            )


# ============================================================
# DISPLAY LESSON
# ============================================================

lesson = st.session_state.get("lesson_result")

if lesson:
    st.markdown(
        '<div class="eyebrow">YOUR SESSION IS READY</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title">Let\'s make progress.</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        f"Explain a topic · {lesson['subject']} · {lesson['level']}"
    )

    with st.container(border=True):
        st.markdown(lesson["answer"])

    st.download_button(
        "Download lesson as Markdown",
        data=lesson["answer"],
        file_name="studysprint_lesson.md",
        mime="text/markdown",
        use_container_width=True,
        key="download_lesson",
    )


# ============================================================
# INTERACTIVE QUIZ
# ============================================================

quiz = st.session_state.get("active_quiz")
quiz_meta = st.session_state.get("quiz_meta", {})

if quiz:
    st.markdown("---")

    st.markdown(
        '<div class="eyebrow">PERSONALISED QUIZ</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title">Let\'s test your knowledge.</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        f"{quiz_meta.get('subject', '')} · "
        f"{quiz_meta.get('topic', '')} · "
        f"{quiz_meta.get('level', '')}"
    )

    st.success(
        f"Quiz ready! {len(quiz)} validated questions generated."
    )

    if not st.session_state.get("quiz_submitted", False):
        st.info(
            "Select one answer per question, then submit. "
            "Correct answers and explanations remain hidden until submission."
        )

        with st.form("interactive_quiz_form"):
            for i, question in enumerate(quiz, start=1):
                st.markdown(
                    f"### {i}. {question['question']}"
                )

                choices = [
                    f"{letter}. {question['options'][letter]}"
                    for letter in "ABCD"
                ]

                st.radio(
                    "Choose your answer",
                    choices,
                    index=None,
                    key=f"quiz_answer_{i}",
                    label_visibility="collapsed",
                )

                if i < len(quiz):
                    st.divider()

            submitted = st.form_submit_button(
                "Submit my answers",
                type="primary",
                use_container_width=True,
            )

        if submitted:
            answers = {}

            for i in range(1, len(quiz) + 1):
                chosen = st.session_state.get(
                    f"quiz_answer_{i}"
                )

                answers[i] = (
                    chosen[0] if chosen else None
                )

            st.session_state["quiz_user_answers"] = answers
            st.session_state["quiz_submitted"] = True
            st.rerun()

    else:
        answers = st.session_state.get(
            "quiz_user_answers", {}
        )

        correct_count = sum(
            1
            for i, question in enumerate(quiz, start=1)
            if answers.get(i) == question["correct_answer"]
        )

        attempted = sum(
            1
            for i in range(1, len(quiz) + 1)
            if answers.get(i)
        )

        percentage = round(
            correct_count / len(quiz) * 100
        ) if quiz else 0

        st.markdown("## Your results")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Score",
            f"{correct_count}/{len(quiz)}",
        )

        col2.metric(
            "Percentage",
            f"{percentage}%",
        )

        col3.metric(
            "Answered",
            f"{attempted}/{len(quiz)}",
        )

        st.progress(percentage / 100)

        if percentage >= 90:
            st.success(
                "Excellent work! You have a strong understanding of this topic."
            )
            recommendation = (
                "Try a more advanced topic or build a small practical project."
            )

        elif percentage >= 70:
            st.success(
                "Good progress! Review the questions you missed."
            )
            recommendation = (
                "Revise the missed concepts and try another quiz at the same level."
            )

        elif percentage >= 50:
            st.warning(
                "You're building your understanding. Review the explanations."
            )
            recommendation = (
                "Review the core concepts, practise examples, and try again."
            )

        else:
            st.info(
                "Every attempt helps you learn. Take your time with the explanations."
            )
            recommendation = (
                "Revisit the basics, practise step by step, then try a shorter quiz."
            )

        st.markdown("### Review your answers")

        result_lines = [
            f"# StudySprint AI Results: {quiz_meta.get('topic', 'Quiz')}",
            f"Score: {correct_count}/{len(quiz)} ({percentage}%)",
            f"Answered: {attempted}/{len(quiz)}",
            "",
        ]

        for i, question in enumerate(quiz, start=1):
            chosen = answers.get(i)
            correct = question["correct_answer"]

            with st.container(border=True):
                st.markdown(
                    f"**{i}. {question['question']}**"
                )

                if chosen is None:
                    st.write("Your answer: Not answered")
                    st.error("Not answered")
                    your_answer_text = "Not answered"

                else:
                    st.write(
                        f"Your answer: {chosen}. "
                        f"{question['options'][chosen]}"
                    )

                    your_answer_text = (
                        f"{chosen}. {question['options'][chosen]}"
                    )

                    if chosen == correct:
                        st.success("Correct!")
                    else:
                        st.error("Incorrect")

                st.write(
                    f"**Correct answer:** {correct}. "
                    f"{question['options'][correct]}"
                )

                st.write(
                    f"**Explanation:** {question['explanation']}"
                )

                st.caption(
                    f"Concept: {question['topic_tag']}"
                )

            result_lines.extend([
                f"## {i}. {question['question']}",
                f"Your answer: {your_answer_text}",
                f"Correct answer: {correct}. "
                f"{question['options'][correct]}",
                f"Explanation: {question['explanation']}",
                "",
            ])

        st.markdown("### Your next study step")
        st.write(recommendation)

        result_lines.extend([
            "## Your next study step",
            recommendation,
        ])

        st.download_button(
            "Download results and explanations",
            data="\n".join(result_lines),
            file_name="studysprint_quiz_results.md",
            mime="text/markdown",
            use_container_width=True,
            key="download_quiz_results",
        )

        if st.button(
            "Try this quiz again",
            type="primary",
            use_container_width=True,
        ):
            st.session_state["quiz_submitted"] = False
            st.session_state["quiz_user_answers"] = {}

            for i in range(1, len(quiz) + 1):
                st.session_state.pop(
                    f"quiz_answer_{i}",
                    None,
                )

            st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        StudySprint AI · Made for curious minds<br>
        Learn a little. Improve every day.
    </div>
    """,
    unsafe_allow_html=True,
)