import requests
import openai
from azure.storage.blob import BlobServiceClient
import streamlit as st
import json

openai.api_type = "azure"
openai.api_base = "https://cog-ps4mawleuhav4.openai.azure.com/"
openai.api_version = "2023-06-01-preview"
openai.api_key = "d8280e16a8c44a49bf3b833a73a6cc52"
azure_connection_string = "DefaultEndpointsProtocol=https;AccountName=sitecoredemoblobstorage;AccountKey=NV6YxWWitdhtSm0rzzX6xrTux/RmtgxWIY+Psobwz4vJM3GBMg+2KgLi7C6XUHtiuWFa3LfhoSID+AStZEFo2g==;EndpointSuffix=core.windows.net"

def generate_website_content(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=1.0,
        max_tokens=2000
    )
    return response.choices[0].text.strip()

def upload_text_to_blob_storage(text, container_name, blob_name):
    blob_service_client = BlobServiceClient.from_connection_string(azure_connection_string)
    blob_client = blob_service_client.get_blob_client(container_name, blob_name)
    blob_client.upload_blob(text.encode(), overwrite=True)

if __name__ == "_main_":
    st.sidebar.title("Azure AOAI with GTI")
    st.sidebar.image("https://media.licdn.com/dms/image/C560BAQG-z4mFpkcj1g/company-logo_200_200/0/1631388948853?e=2147483647&v=beta&t=9K8Ajrde__ehRbdaYlLsp7oJhqfEUPZuSBs7StG2h6k", width=200)
    st.title("Marketing Content Generator")
    st.write("Provide the prompt for the content you want to generate:")
    text_prompt = st.text_input("Text Prompt", "Generate a compelling call to action for our website that encourages visitors to try our AI-powered solutions.")

prompts = ["Write a compelling hero banner for our website that highlights our AI-powered solutions.",
               "Generate a compelling call to action for our website that encourages visitors to try our AI-powered solutions.",
               "Create a persuasive 'Checkout Now' message for customers who have added our AI-powered solutions to their cart."]

for i, prompt in enumerate(prompts):
    text_prompt = st.text_input(f"Text Prompt {i+1}", prompt)

    if text_prompt:
        st.write(f"Generating content for prompt {i+1}...")
        content = generate_website_content(text_prompt)
        st.markdown(f"## {content}")

        blob_name = f"generated_text_{i+1}.json"
        json_content = json.dumps(content)  # Convert content to JSON
        upload_text_to_blob_storage(json_content, "testcontainer", blob_name)  # Upload JSON content
        st.write(f"Content for prompt {i+1} uploaded to blob storage.")