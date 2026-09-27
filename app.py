import streamlit as st
from langchain_groq import ChatGroq

st.set_page_config(page_title='My AI Chat', layout='centered')

st.title("🤖 The Groq Chatbot")
st.write("A fully integrated, memory-enabled AI assistant.")


# --------------------------------------------------
# 1. Sidebar
# --------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configuration")

    user_api_key = st.text_input(
        'Enter the Groq API Key:',
        type='password'
    )

    st.info('Your key is required to wake up the AI Brain')

    # System Prompt / Persona
    persona = st.text_area(
        "System Prompt:",
        value="You are a helpful assistant."
    )

    # Reset Chat Button
    if st.button("Reset Chat & Apply Persona"):
        st.session_state.messages = []
        st.rerun()


# --------------------------------------------------
# 2. Memory Vault
# --------------------------------------------------
if 'messages' not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# 3. Display History
# --------------------------------------------------
for msg in st.session_state.messages:

    # Don't display system message
    if msg['role'] == 'system':
        continue

    with st.chat_message(msg['role']):
        st.markdown(msg['content'])


# --------------------------------------------------
# 4. Chat Input and Logic
# --------------------------------------------------
if user_query := st.chat_input('Say something to the AI...'):

    if not user_api_key:

        st.error('Please enter your api key in the sidebar first!')

    else:

        # --------------------------------------------------
        # Add System Prompt only once
        # --------------------------------------------------
        if (
            not st.session_state.messages
            or st.session_state.messages[0]['role'] != 'system'
        ):
            st.session_state.messages.insert(
                0,
                {
                    'role': 'system',
                    'content': persona
                }
            )

        # Display user message instantly
        with st.chat_message('user'):
            st.markdown(user_query)

        # Store user message
        st.session_state.messages.append(
            {
                'role': 'user',
                'content': user_query
            }
        )


        # --------------------------------------------------
        # Initialise the Brain
        # --------------------------------------------------
        llm = ChatGroq(
            model='openai/gpt-oss-20b',
            temperature=0.7,
            api_key=user_api_key
        )


        # --------------------------------------------------
        # Send complete history to LLM
        # System message is always the first message
        # --------------------------------------------------
        with st.spinner('AI is thinking....'):

            response = llm.invoke(
                st.session_state.messages
            )

            bot_answer = response.content


        # Store AI response
        st.session_state.messages.append(
            {
                'role': 'assistant',
                'content': bot_answer
            }
        )


        # Display AI response
        with st.chat_message('assistant'):
            st.markdown(bot_answer)
