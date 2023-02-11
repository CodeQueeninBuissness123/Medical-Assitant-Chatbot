import openai
import sqlite3
import streamlit as st

openai.api_key = "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"

conn = sqlite3.connect("diagnoses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS diagnoses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symptoms TEXT,
    age INTEGER,
    duration TEXT,
    gender TEXT,
    diagnosis TEXT
)
""")

conn.commit()


def get_diagnosis(symptoms):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt="Please diagnose the following symptoms: " + symptoms,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    ).choices[0].text

    return response


def save_diagnosis(symptoms, age, duration, gender, diagnosis):
    cursor.execute("""
    INSERT INTO diagnoses (symptoms, age, duration, gender, diagnosis) 
    VALUES (?, ?, ?, ?, ?)
    """, (symptoms, age, duration, gender, diagnosis))
    conn.commit()


def main():
    st.title("Medical Assistant Chatbot")
    symptoms = st.text_input("Enter your symptoms:")
    age = st.slider("Select your age:", 0, 120, 25)
    duration = st.selectbox("Select the duration of your symptoms:",
                            ["0 to 6 hours", "7 to 24 hours", "24 to 48 hours", "48 to 72 hours +"])
    gender = st.selectbox("Select your gender:", ["Male", "Female"])
    if st.button("Get Diagnosis"):
        diagnosis = get_diagnosis(symptoms)
        st.success("The diagnosis is: " + diagnosis)
        save_diagnosis(symptoms, age, duration, gender, diagnosis)


if __name__ == "__main__":
    main()
