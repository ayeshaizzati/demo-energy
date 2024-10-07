import streamlit as st

st.title('Hello, Streamlit!')
st.write('This is your first Streamlit app')

user_input = st.text_input("Enter some text:")
st.write("You entered:", user_input)

mass = st.text_input("Enter your mass (kg)")
