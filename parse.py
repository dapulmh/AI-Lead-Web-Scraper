from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd

model = OllamaLLM(model="llama3.1")

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **Ensure Table Format:** Your output should always be in table format with consistent column headers.\n"
    "3. **Standardized Headers:** The table must always include the following headers: {headers}. Ensure consistency across all batches.\n"
    "4. **Handle Missing Data:** If a column has no value for a particular row, keep it empty instead of omitting it.\n"
    "5. **Return Only the Table:** No extra text, comments, or explanations.\n"
    "6. **Empty Response:** If no information matches the description, return an empty string ('').\n"
    "7. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

prompt_template = ChatPromptTemplate.from_template(template)


def parse_with_ollama(dom_chunks, parse_description, headers):
    chain = prompt_template | model
    list_headers = [h.strip() for h in headers.split(",")]

    all_data = []

    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke(
            {
                "dom_content": chunk,
                "parse_description": parse_description,
                "headers": ", ".join(list_headers),
            }
        )
        print(f"Parsed Batch {i} of {len(dom_chunks)}")
        all_data.append(response)

    return "\n".join(all_data)
