import streamlit as st
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Load Gemini pro vision

model = genai.GenerativeModel("gemini-pro-vision")

def get_final_response(system_prompt,input_image,user_prompt):
    response = model.generate_content([system_prompt,input_image[0],user_prompt])
    for candidate in response.candidates:
        return [part.text for part in candidate.content.parts][0]
    #return response.text

def image_processing(upload_file):
    """
    This function converts the image in bytes
    """

    if upload_file is not None:
        data_bytes = upload_file.getvalue()
        image_parts = [
            {
                "mime_type" : upload_file.type,
                "data" : data_bytes
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file is uploaded.")
    
system_prompt  = """
You're developing an advanced nutritional analysis tool that uses image recognition technology to estimate calorie intake from food images. 
The system should be capable of accurately identifying different types of food items in an image and calculating the total calorie intake as well as providing a breakdown
 of calorie counts for each food item detected. At the same time keep a count of quantity of each item and calculate calorie accordingly.

The system will accept food images as input and return the following output (in bullet points):


        Total calories : Sum of calories of all food item
        1. Food item 1 (Quantity): Calorie count of food item 1 
        2. Food item 2 (Quantity): Calorie count of food item 2 
        3. Food item 3 (Quantity): Calorie count of food item 3 
        .
        .
        . and so on..

"""

## Stremlit code:
    
st.set_page_config(page_title="Nutritional Model 🍿🍜")

st.header("Calorie Analysis 🍔🍕")
input = st.text_input("Input Prompt: ", key= "user_prompt")
upload_file = st.file_uploader("Upload your Food Image", type = ["jpg", "jpeg", "png"])
submit = st.button("Generate Calorie Analysis")

image = ""

if submit:
    image_data = image_processing(upload_file)
    response =  get_final_response(system_prompt,image_data,input)
    st.subheader("See Calorie Analysis below : ")
    st.success(response)

if upload_file is not None:
     image = Image.open(upload_file)
     st.image(image, caption = "Uploaded image",width=500)




