# lms_teacher_app_advanced.py

import streamlit as st
import pandas as pd
from supabase import create_client
import datetime
import matplotlib.pyplot as plt

# -----------------------------
# Supabase Configuration
# -----------------------------
SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_KEY = st.secrets["supabase"]["key"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("🎓 Advanced LMS Lecturer Dashboard")

# -----------------------------
# Lecturer Login
# -----------------------------
lecturer_id = st.text_input("Enter your Lecturer ID", type="password")

if lecturer_id:

    # -----------------------------
    # Module Content Upload
    # -----------------------------
    st.header(" Upload Content for a Module")
    course_list = supabase.table("courses").select("id, course_name").eq("lecturer_id", int(lecturer_id)).execute()
    courses = {c["course_name"]: c["id"] for c in course_list.data}
    
    selected_course = st.selectbox("Select Course", list(courses.keys()))
    uploaded_file = st.file_uploader("Choose a file")
    title = st.text_input("Content Title")
    content_type = st.selectbox("Content Type", ["PDF", "Video"])
    
    if st.button("Upload Content") and uploaded_file and title:
        # Upload file to Supabase Storage
        file_bytes = uploaded_file.read()
        storage_response = supabase.storage.from_("course-content").upload(
            f"{selected_course}/{uploaded_file.name}", file_bytes
        )
        if storage_response.error:
            st.error(f"File upload failed: {storage_response.error['message']}")
        else:
            # Get public URL for the uploaded file
            public_url = supabase.storage.from_("course-content").get_public_url(f"{selected_course}/{uploaded_file.name}")
            supabase.table("course_content").insert({
                "course_id": courses[selected_course],
                "title": title,
                "content_type": content_type,
                "file_url": public_url,
                "created_at": datetime.datetime.utcnow().isoformat()
            }).execute()
            st.success("Content uploaded successfully!")

    # -----------------------------
    # Quiz Upload
    # -----------------------------
    st.header(" Upload Quiz for a Module")
    quiz_course = st.selectbox("Select Course for Quiz", list(courses.keys()), key="quiz_course")
    quiz_title = st.text_input("Quiz Title")
    questions_json = st.text_area("Questions JSON", '{"question": "Q1?", "options": ["A","B","C"], "answer": "A"}')
    
    if st.button("Upload Quiz"):
        supabase.table("quizzes").insert({
            "title": quiz_title,
            "chapter": quiz_title,
            "questions": questions_json,
            "course_id": courses[quiz_course],
            "created_by": int(lecturer_id),
            "created_at": datetime.datetime.utcnow().isoformat()
        }).execute()
        st.success("Quiz uploaded successfully!")

    # -----------------------------
    # Analytics Overview
    # -----------------------------
    st.header(" Analytics Overview")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Show Leaderboard"):
            leaderboard = supabase.rpc("get_leaderboard_for_lecturer", {"p_lecturer_id": int(lecturer_id)}).execute()
            df_leaderboard = pd.DataFrame(leaderboard.data)
            st.dataframe(df_leaderboard)
            if not df_leaderboard.empty:
                st.bar_chart(df_leaderboard.set_index("first_name")["points"])
    
    with col2:
        if st.button("Show Engagement"):
            engagement = supabase.rpc("get_student_engagement", {"p_lecturer_id": int(lecturer_id)}).execute()
            engaged_count = engagement.data[0]["engaged_students"] if engagement.data else 0
            st.metric("Engaged Students (last 30 days)", engaged_count)
    
    with col3:
        if st.button("Show Quiz Averages"):
            quiz_avg = supabase.rpc("get_course_quiz_average", {"p_lecturer_id": int(lecturer_id)}).execute()
            df_quiz_avg = pd.DataFrame(quiz_avg.data)
            st.dataframe(df_quiz_avg)
            if not df_quiz_avg.empty:
                st.bar_chart(df_quiz_avg.set_index("course_name")["avg_score"])

    # -----------------------------
    # Drill-down: Individual Student Analytics
    # -----------------------------
    st.header(" Student Performance Drill-down")
    student_ids = df_leaderboard['student_id'].tolist() if not df_leaderboard.empty else []
    selected_student = st.selectbox("Select Student ID", student_ids)

    if selected_student:
        # Quiz Performance
        quiz_perf = supabase.rpc("get_student_quiz_performance", {
            "p_student_id": int(selected_student),
            "p_lecturer_id": int(lecturer_id)
        }).execute()
        df_quiz = pd.DataFrame(quiz_perf.data)
        st.subheader("Quiz Performance")
        st.dataframe(df_quiz)
        if not df_quiz.empty:
            st.bar_chart(df_quiz.set_index("quiz_title")["score"])

        # Chatbot interactions
        chat_history = supabase.rpc("get_student_chat_history", {
            "p_student_id": int(selected_student),
            "p_lecturer_id": int(lecturer_id)
        }).execute()
        df_chat = pd.DataFrame(chat_history.data)
        st.subheader("Chatbot Interaction")
        st.dataframe(df_chat)

        # Gamification
        gamification = supabase.rpc("get_student_gamification", {
            "p_student_id": int(selected_student),
            "p_lecturer_id": int(lecturer_id)
        }).execute()
        df_gam = pd.DataFrame(gamification.data)
        st.subheader("Gamification & Engagement")
        st.dataframe(df_gam)
        if not df_gam.empty:
            st.line_chart(df_gam.set_index("course_name")["points"])
        
        # Module completion example chart
        st.subheader("Module Completion")
        completed = len(df_gam)  # Example: using gamification rows as completed modules
        pending = 5 - completed   # Assume 5 modules
        fig, ax = plt.subplots()
        ax.pie([completed, pending], labels=["Completed", "Pending"], autopct="%1.1f%%")
        st.pyplot(fig)

    st.success(" Analytics loaded successfully!")

    # -----------------------------
    # ML Predictions (placeholder)
    # -----------------------------
    st.header(" Student Risk Predictions")
    if st.button("Predict At-Risk Students"):
        st.info("ML model placeholder: will predict students likely to perform poorly or disengage.")
        # Here you can fetch Supabase data, feed it to a trained model, and display predictions
