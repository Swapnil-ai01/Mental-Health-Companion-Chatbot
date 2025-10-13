from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from datetime import datetime

GOOGLE_API_KEY= "AIzaSyA2dj78hDEYjt639DWu8-L9bKm2jWPhbiA" 
genai.configure(api_key=GOOGLE_API_KEY)

if "chat_history" not in st.session_state:
    st.session_state.chat_history=[]
if "dia_entries" not in st.session_state:
    st.session_state.dia_entries = []
if 'User_profile' not in st.session_state:
    st.session_state.User_profile = {
        'Nickname' : '',
        'Age' : '' ,
        'Occupation' : '',
        'Medical conditions' : 'None'
    }
def get_gemini_response(input_prompt):
    model = genai.GenerativeModel('gemini-2.5-flash')
    content = [input_prompt]
    try:
        response = model.generate_content(content)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

st.set_page_config(page_title="AI Mental Health Companion", layout="wide")
st.header("AI Mental Health Companion")

with st.sidebar:
    st.subheader("User Profile")

    nickname = st.text_area("Nickname",
                            value=st.session_state.User_profile['Nickname'],
                            placeholder="Set any name that bot call to you.(Optional)")
    age_options = ["select", "4-10 years", "11-18 years", "19-25 years", "26-45 years", "45-80 years"]
    age_index = age_options.index(st.session_state.User_profile['Age']) if st.session_state.User_profile['Age'] in age_options else 0
    age = st.selectbox("Age", age_options, index=age_index)

    occupation = st.text_area("Occupation",
                             value=st.session_state.User_profile['Occupation'],
                             placeholder="Student\Professionals")
    medical_conditions = st.text_area("Medical conditions",
                                      value=st.session_state.User_profile['Medical conditions'])

    if st.button("Update Profile"):
        st.session_state.User_profile = {
            'Nickname': nickname,
            'Age' : age,
            'Occupation' : occupation,
            'Medical conditions' : medical_conditions
        }
        st.success("Profile updated!")

tab1, tab2 = st.tabs(["Professional counselors", "Diary"])

with tab1:
    st.subheader("🌞Personalized Professional counselors")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Chitchat with AI")
        mood = st.radio("How are you feeling today?", ["😣anxious", "😨stressed", "😁Happy"])
        user_input = st.text_area("What's on your mind free-to expressions:",
                                  placeholder="e.g., 'I feel anxious about exam'")
    with col2:
        st.write("### Your Profile")
        st.json(st.session_state.User_profile)

    if st.button("Send 🚀"):
        is_profile_complete = (
            st.session_state.User_profile['Nickname'] != '',
            st.session_state.User_profile['Age'] != 'select' and
            st.session_state.User_profile['Occupation'] != ''
        )

        if not is_profile_complete:
            st.warning("Please complete your profile in the sidebar first")
        else:
            with st.spinner("Creating your Personalized counselors..."):
                prompt = f"""
                Dear {st.session_state.User_profile['Nickname']},
                Respond to the user in an empathetic and mood-matching tone. For example, if the user is happy, say, "I'm so happy to hear that!" or if the user is feeling anxious,
                say, "I'm sorry to hear you're feeling anxious. I'm here to help."
                Based on the following user profile and additional requirements:
                Age: {st.session_state.User_profile['Age']}
                Occupation: {st.session_state.User_profile['Occupation']}
                Medical conditions: {st.session_state.User_profile['Medical conditions']}

                Additional Requirement: {user_input if user_input else "None Provided"}

                Please provide a response that includes:
                1. Provide a safe, and empathetic response, using techniques inspired by cognitive behavioral therapy (CBT) to help the user manage their thoughts and feelings.
                2. Offer a motivational thought or affirmation that is relevant to the user's mood and situation.
                3. Suggest a simple, practical activity or exercise that can help the user feel better, such as a mindfulness technique or a physical stretch.
                Format the output clearly with the following headings and bullet points. **Start the response with a friendly and supportive greeting and end with a gentle
                disclaimer that you are an AI and not a substitute for professional help.**
                """
                response = get_gemini_response(prompt)

                st.subheader("Personalized Professional counselors")
                st.markdown(response)

with tab2:
    st.title("Diary")
    st.markdown("Write freely about your thoughts. This is just")
    dia_input = st.text_area("Today's reflection",
                             placeholder="Write anything you want to reflect on ...")
    if st.button("Save Entry", key="dia_save"):
        if dia_input:
            current_date_str = datetime.now().strftime("%Y-%m-%d")
            if st.session_state.dia_entries and st.session_state.dia_entries[-1]['date'] == current_date_str:
                st.session_state.dia_entries[-1]['text'] += f"\n\n---\n\n{dia_input}"
            else:
                entry_with_date = {
                    "date": current_date_str,
                    "text": dia_input
                }
                st.session_state.dia_entries.append(entry_with_date)
            st.success("Diary entry saved!")
    if st.session_state.dia_entries:
        st.markdown("### Your Entries")
        for entry in st.session_state.dia_entries:
            st.markdown(f"**Date:** {entry['date']}")
            st.markdown(entry['text'])
            st.markdown("---")
