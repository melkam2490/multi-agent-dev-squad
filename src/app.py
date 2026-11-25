
import streamlit as st
from dotenv import load_dotenv

from src.orchestrator import run_squad

load_dotenv()

st.set_page_config(
    page_title="Multi-Agent Development Squad",
    page_icon="🤖"
)

st.title("🤖 Multi-Agent Development Squad")
st.write("Three AI agents work together to build and test Python code.")

user_request = st.text_area(
    "Describe the feature you want to build:",
    placeholder="Example: Create a Python function that adds two numbers."
)

if st.button("Start Agents"):
    if not user_request.strip():
        st.warning("Please describe a feature first.")
    else:
        try:
            with st.spinner("The agents are working..."):
                result = run_squad(user_request)

            st.success("The agents finished!")

            st.subheader("1. Product Specification")
            st.json(result["spec"].model_dump())

            st.subheader("2. Generated Code")
            st.code(
                result["code"].implementation_code,
                language="python"
            )

            st.subheader("3. QA Report")
            st.json(result["qa"].model_dump())

            st.subheader("4. Iteration History")
            st.write(result["history"])

        except Exception as error:
            st.error(f"Something went wrong: {error}")
