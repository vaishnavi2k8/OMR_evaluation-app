# logic.py

def evaluate_omr(omr_answers, answer_key_df):
    """
    Evaluate answers against the answer key.

    Parameters:
    - omr_answers: dict {question: selected_option}
    - answer_key_df: DataFrame with 'Question' and 'Correct_Option'

    Returns:
    - results: dict {question: True/False}
    """
    answer_key = dict(zip(answer_key_df['Question'], answer_key_df['Correct_Option']))
    results = {}
    for q, user_ans in omr_answers.items():
        correct_ans = answer_key.get(q)
        results[q] = (user_ans == correct_ans)
    return results
