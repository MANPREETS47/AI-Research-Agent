import streamlit as st
from main import graph
from langchain_core.messages import HumanMessage

CONFIG = {'configurable': {'thread_id': "1"}}

st.set_page_config(page_title="AI Research Agent", page_icon="🔍", layout="wide")
st.title("🔍 AI Research Agent")

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'backend_state' not in st.session_state:
    st.session_state['backend_state'] = None

# Display chat messages
for msg in st.session_state['message_history']:
    with st.chat_message(msg['role']):
        st.text(msg['content'])

user_input = st.chat_input("Ask me anything...")

if user_input:
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message("user"):
        st.text(user_input)

    # Prepare the state for your graph
    state = {
        "messages": [{"role": "user", "content": user_input}],
        "user_question": user_input,
        "google_results": None,
        "bing_results": None,
        "reddit_results": None,
        "google_analysis": None,
        "bing_analysis": None,
        "reddit_analysis": None,
        "final_answer": None,
        "final_ans_framer": None,
    }

    with st.spinner("Processing your query..."):
        response = graph.invoke(state, config=CONFIG)

    ai_message = response.get('final_ans_framer') or response.get('final_answer')

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
    with st.chat_message("assistant"):
        st.markdown(ai_message)
    

    #     ai_message = response.get('final_ans_framer') or response.get('final_answer')
            


    # st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})

    # Save backend state for future use if needed
    st.session_state['backend_state'] = response
