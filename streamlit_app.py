import streamlit as st
from hugchat import hugchat
from hugchat.login import Login
from PIL import Image
from botTemplates import css, bot_template, user_template

def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo
    
# App title
st.set_page_config(page_title="🤗💬 Munna Bhai MBBS !")
my_logo = add_logo(logo_path="img/munnabhai_1.jpg", width=280, height=239)
#my_logo = add_logo(logo_path="img/streamlit.png", width=280, height=239)

# Hugging Face Credentials
with st.sidebar:
    st.title('🤗💬 Chat with Bhai')
    st.sidebar.image(my_logo)
    if ('EMAIL' in st.secrets) and ('PASS' in st.secrets):
        st.success('HuggingFace Login credentials already provided!', icon='✅')
        hf_email = st.secrets['EMAIL']
        hf_pass = st.secrets['PASS']
    else:
        hf_email = st.text_input('Enter E-mail:', type='password')
        hf_pass = st.text_input('Enter password:', type='password')
        if not (hf_email and hf_pass):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
    st.markdown('📖 My LinkedIn Profile [LinkedIn](https://www.linkedin.com/in/mbaig162/)!')
    st.markdown('📖 Generative AI - Image to Speech [demo](https://www.loom.com/share/1a39ba984dbc4f8d98255bc19cf98255?sid=5f322694-1162-45c5-a63f-03f9127b94c9/)!')
    st.markdown('📖 Chat with your document [demo](https://www.loom.com/share/a0175fbad3024c52aecb4aa92754ad74?sid=acf6a0ca-e355-41d6-a045-860f9caf9974/)!')
    st.markdown('📖 Learn how to build this app from dataprofessor in his [blog] (https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/)!')   
    
# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Tension nahi leneka, bhai !   Batao, apun kaise madad kar sakta hai?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        #st.write(bot_template.replace("{{MSG}}", message["content"]), unsafe_allow_html=True)
        st.write(message["content"])

# Function for generating LLM response
def generate_response(prompt_input, email, passwd):
    # Hugging Face Login
    sign = Login(email, passwd)
    cookies = sign.login()
    #sign.saveCookies()
    # Create ChatBot                        
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    prompt_template = f"""Imagine yourself as a Bollywood's movie character Munna Bhai MBBS and answer the User prompt in a Munna Bhai's slang style, polite and limit to 20 words. User prompt: {prompt_input}
    """
    return chatbot.chat(prompt_template)

# User-provided prompt
if prompt := st.chat_input(disabled=not (hf_email and hf_pass)):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(user_template.replace("{{MSG}}", prompt), unsafe_allow_html=True)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    #with st.chat_message("assistant"):
    with st.chat_message("assistant"):
        with st.spinner("Bhai, abhi thoda time lagega, apun soch raha hai..."):
            response = generate_response(prompt, hf_email, hf_pass) 
            st.write(bot_template.replace("{{MSG}}", response), unsafe_allow_html=True)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
