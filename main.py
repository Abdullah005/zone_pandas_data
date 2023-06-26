import streamlit as st
from langchain.agents import create_pandas_dataframe_agent
import os
import pandas as pd
import csv
from langchain.llms import OpenAI
from streamlit_chat import message

# Set the title of the app
st.title("Zone Bot")

# Add key input
key = st.sidebar.text_input(
    label="API",
    placeholder="Enter Api Key",
    type="password")

 # Read Data as Pandas
data = pd.read_csv('3states.csv')

# Check if key is entered
if key:
    os.environ['OPENAI_API_KEY'] = key
    try:
        agent = create_pandas_dataframe_agent(OpenAI(
            temperature=0.0),data, verbose=True)

        if 'history' not in st.session_state:
            st.session_state['history'] = []

        # Define Generated and Past Chat Arrays
        if 'generated' not in st.session_state:
            st.session_state['generated'] = []

        if 'past' not in st.session_state:
            st.session_state['past'] = []

        # Accept input from user
        query = st.text_input("Enter a query:")

        # container for the chat history
        response_container = st.container()
        # container for the user's text input
        container = st.container()

        # Execute Button Logic
        if st.button("Execute") and query:
            with st.spinner('Generating response...'):
                try:
                    answer = agent.run(query)
                    st.session_state['history'].append((query, answer))

                    # Store conversation
                    st.session_state.past.append(query)
                    st.session_state.generated.append(answer)


                    # Display conversation in reverse order
                    if st.session_state['generated']:
                        with response_container:
                            for i in range(len(st.session_state['generated'])):
                                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user',
                                        avatar_style="big-smile")
                                message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")


                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
    except:
        st.error(f"Token Limit Excided")
