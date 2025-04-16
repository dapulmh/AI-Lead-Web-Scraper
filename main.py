import streamlit as st
from scrape import scrape_website_premium, scrape_website_basic, clean_body_content, extract_body_content, split_dom_content
from parse import parse_with_ollama


st.title("AI Lead Web Scrapper")
url = st.text_input("Enter your webiste URL: ")
options = ["Premium", "Basic"]

# Create dropdown (selectbox)
option_approach = st.selectbox("Choose your option (premium will give you possibilities to scrape website that use credential):", options)

if st.button("Scrape Website"):
    st.write("Scraping the website")
    if url:
        if option_approach == "Premium":
            scrape_result = scrape_website_premium(url)
        else:
            scrape_result = scrape_website_basic(url)

        body_content = extract_body_content(scrape_result)
        cleaned_content = clean_body_content(body_content)

        st.session_state.dom_content = cleaned_content

        with st.expander("View Dom Content"):
            st.text_area("Dom Content", cleaned_content, height=400)


if "dom_content" in st.session_state:

    parse_description = st.text_area(
        "Describe what information you want to get?")
    headers = st.text_input(
        "Put your headers that you want to get ? Ex: No,Company,Address")
    if st.button("Parse Content"):
        if parse_description:
            st.write("Processing the content")

            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(
                dom_chunks, parse_description, headers)
            st.write(result)
