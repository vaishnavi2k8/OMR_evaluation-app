# app.py

import streamlit as st
import pandas as pd
import json
import os
from logic import evaluate_omr

# Folder to save multiple answer keys
SAVE_DIR = "saved_answer_keys"
os.makedirs(SAVE_DIR, exist_ok=True)

# Function to load answer key from various formats
def load_answer_key(file):
    try:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        elif file.name.endswith(".json"):
            data = json.load(file)
            if isinstance(data, dict):
                df = pd.DataFrame(list(data.items()), columns=["Question", "Correct_Option"])
            else:
                df = pd.DataFrame(data)
        elif file.name.endswith(".xlsx"):
            df = pd.read_excel(file)
        elif file.name.endswith(".txt"):
            try:
                df = pd.read_csv(file, delimiter="\t")
            except:
                file.seek(0)
                df = pd.read_csv(file)
        else:
            st.error("Unsupported file type")
            return None
        return df
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None

# Get all saved answer keys
def get_saved_answer_keys():
    return [f for f in os.listdir(SAVE_DIR) if f.endswith(".csv")]

def main():
    st.title("📄 OMR Evaluation App (Multiple Answer Key Support)")

    st.sidebar.header("Upload New Answer Key")
    new_key_file = st.sidebar.file_uploader("Upload Answer Key (CSV, JSON, XLSX, TXT)", type=["csv", "json", "xlsx", "txt"])
    if new_key_file:
        df = load_answer_key(new_key_file)
        if df is not None:
            st.sidebar.success("✅ Answer key loaded successfully!")
            st.dataframe(df)

            key_name = st.sidebar.text_input("Enter a name to save this answer key (e.g. 'math_exam')")
            if key_name:
                if not key_name.lower().endswith(".csv"):
                    key_name += ".csv"
                save_path = os.path.join(SAVE_DIR, key_name)
                df.to_csv(save_path, index=False)
                st.sidebar.success(f"✅ Saved as: {key_name}")

    st.sidebar.header("Select Existing Answer Key")
    saved_keys = get_saved_answer_keys()

    if saved_keys:
        selected_key = st.sidebar.selectbox("Choose Answer Key", saved_keys)
        key_path = os.path.join(SAVE_DIR, selected_key)
        try:
            answer_key_df = pd.read_csv(key_path)
            st.success(f"✅ Using Answer Key: {selected_key}")
            st.dataframe(answer_key_df)
        except:
            st.error("⚠️ Error loading selected answer key.")
            return
    else:
        st.warning("⚠️ No saved answer keys found. Please upload one.")
        return

    # Manual input of OMR answers
    st.header("✍️ Input OMR Answers")
    omr_answers = {}
    for q in answer_key_df['Question']:
        ans = st.selectbox(f"Answer for Question {q}", options=[0, 1, 2, 3], key=f"q{q}")
        omr_answers[q] = ans

    # Evaluate
    if st.button("✅ Evaluate OMR"):
        results = evaluate_omr(omr_answers, answer_key_df)
        st.subheader("📊 Evaluation Results")
        correct = 0
        total = len(results)
        for q, is_correct in results.items():
            if is_correct:
                st.markdown(f"*Question {q}*: ✅ Correct")
                correct += 1
            else:
                st.markdown(f"*Question {q}*: ❌ Wrong")

        st.markdown("---")
        st.success(f"🎯 You got {correct} out of {total} correct ({(correct/total)*100:.2f}%)")

if __name__ == "__main__":
    main()

