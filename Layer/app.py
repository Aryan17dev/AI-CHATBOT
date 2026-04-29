import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import re
import pickle

@st.cache_resource
def load_model():
    with open('case_category_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('tfidf_vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    return model, vectorizer


def validate_input(first_party, second_party, facts):
    if not first_party.strip():
        return "First Party cannot be empty."
    
    if not second_party.strip():
        return "Second Party cannot be empty."
    
    if not facts.strip():
        return "Case facts cannot be empty."
    
    if len(facts) < 20:
        return "Case facts must be at least 20 characters long."
    
    if not re.match(r"^[a-zA-Z0-9\s.,!?'-]+$", facts):
        return "Case facts contain invalid characters. Only letters, numbers, spaces, and basic punctuation are allowed."
    
    return None  
def predict_outcome(model, vectorizer, first_party, second_party, facts):
    input_text = first_party + " " + second_party + " " + facts
    input_vectorized = vectorizer.transform([input_text])
    probabilities = model.predict_proba(input_vectorized)[0]
    return {
        "Petitioner": probabilities[0] * 100,
        "Respondent": probabilities[1] * 100
    }

def plot_pie_chart(prediction):
    labels = ['Petitioner', 'Respondent']
    sizes = [prediction['Petitioner'], prediction['Respondent']]
    colors = ['#ff9999','#66b3ff']
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')  
    
    st.pyplot(fig)

def main():
    st.title("Judgement Prediction Model")

    st.sidebar.title("AI Assistant Navigation")
    st.sidebar.markdown("[💬 Chatbot](https://ai-chatbot-696h.onrender.com/)")
    st.sidebar.markdown("[📄 Doc Generator](https://ai-chatbot-uk2s.onrender.com/)")
    st.sidebar.markdown("**⚖️ Case Outcome Prediction (Current)**")

    model, vectorizer = load_model()

    st.header("Predict Outcome")
    first_party = st.text_input("Enter First Party")
    second_party = st.text_input("Enter Second Party")
    facts = st.text_area("Enter Case Facts")

    if st.button("Predict"):
        error_message = validate_input(first_party, second_party, facts)
        
        if error_message:
            st.error(error_message)  
        else:
            prediction = predict_outcome(model, vectorizer, first_party, second_party, facts)
            st.write(f"Chances of Petitioner winning: {prediction['Petitioner']:.2f}%")
            st.write(f"Chances of Respondent winning: {prediction['Respondent']:.2f}%")
           
            plot_pie_chart(prediction)

if __name__ == "__main__":
    main()
