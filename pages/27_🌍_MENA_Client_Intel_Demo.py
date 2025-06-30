
import streamlit as st
import openai

st.set_page_config(layout="wide")
st.title("🌍 MENA Client Intelligence – Live LLM Demo")

st.markdown("Use OpenAI GPT-4 to extract insights from client conversations, tailored to MENA market.")

# API key input
api_key = st.text_input("🔑 Enter your OpenAI API Key:", type="password")

client_input = st.text_area("📨 Paste a client conversation, call note, or email:", 
                            "We are entering the Saudi market and concerned about FX risk and compliance with local tax reforms.")

if st.button("🎯 Analyze with GPT-4"):
    if not api_key:
        st.warning("Please enter your OpenAI API key.")
    elif not client_input.strip():
        st.warning("Client input cannot be empty.")
    else:
        openai.api_key = api_key
        with st.spinner("Calling GPT-4..."):
            try:
                prompt = f"""
You are a Relationship Manager AI assistant specialized in the MENA financial markets.

Analyze the following client input:
{client_input}

Provide:
1. Client Intent
2. Risk or Compliance Concerns
3. Recommended RM Action
4. Cross-sell or Advisory Opportunity
5. Regulatory Context (MENA-specific)

Respond in bullet points with clear section headers.
"""
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                reply = response['choices'][0]['message']['content']
                st.markdown("### ✅ GPT-4 Output")
                st.markdown(reply)
                st.success("Generated via OpenAI GPT-4")

            except Exception as e:
                st.error(f"Error: {e}")
