import streamlit as st
from app.router import router
from app.sql import sql_chain
from app.faq import ingest_faq_data, faq_chain, faq_path

ingest_faq_data(faq_path)

st.markdown("""
    <style>
    .stMarkdown a {
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        word-break: break-all !important;
    }
    </style>
""", unsafe_allow_html=True)

def ask(query):
    route = router(query).name
    print(route)
    if route == 'faq':
        output = faq_chain(query)
        return output
    elif route == 'sql':
        output = sql_chain(query)
        return output
    else:
        return f"Route {route} Not Impletemented yet"

st.title("🛍️ E-Commerce Chatbot")

query = st.chat_input("Write your query")
if "messages" not in st.session_state:
    st.session_state["messages"] = []

for messages in st.session_state.messages:
    with st.chat_message(messages['role']):
        st.markdown(messages['content'])

try:
    if query:
        with st.chat_message("user"):
            st.markdown(query)
        st.session_state.messages.append({"role":"user", "content":query})

        response = ask(query)
        formatted_response = ""
        if isinstance(response, list):
            for idx, product in enumerate(response):
                formatted_response += f"""
                    **{idx+1}) {product['name']}**

                    💰 Rs. {product['price']} ({int(product['discount'])}% off)  
                    ⭐ Rating: {product['rating']}  
                    🔗 [View Product]({product['url']})

                    ---
                    """
        else:
            formatted_response = response

        with st.chat_message("assistant"):  
            st.markdown(formatted_response)
        st.session_state.messages.append({"role": "assistant","content": formatted_response})

except Exception as e:
    st.markdown("Oops! Something went wrong, Please try again.")
    print(f"Error occured: {e}")