import streamlit as st
import google.generativeai as genai
from PIL import Image

# Directly configure the Google Generative AI library with your API key
GOOGLE_API_KEY = 'AIzaSyCCgRg-qDY4T89i_-m_cr3zYkEvsR75gNQ'
genai.configure(api_key=GOOGLE_API_KEY)

# Function to get response from Gemini Pro model
def get_gemini_response(input, image, prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content([input, image[0], prompt])
        return response.text
    except Exception as e:
        st.error(f"Error getting response from Gemini: {e}")
        return None

# Function to process uploaded image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        try:
            bytes_data = uploaded_file.getvalue()
            image_parts = [
                {
                    "mime_type": uploaded_file.type,
                    "data": bytes_data
                }
            ]
            return image_parts
        except Exception as e:
            st.error(f"Error processing uploaded file: {e}")
            return None
    else:
        st.error("No file uploaded")
        return None

# Define the input prompt
input_prompt = """
You’re a highly skilled nutritionist with extensive experience in analyzing food items. You have the capability to estimate caloric content based solely on visual information from images, without considering the quantity or cooking style. Your expertise enables you to provide approximate calorie counts for various food items.

Your task is to analyze an image of food items and calculate their estimated calories. Please review the image I will provide and process it accordingly. 

  

Keep in mind that the estimations should focus solely on the appearance of the food items and their general caloric density without accounting for specific quantities or preparation methods.

For clarification, please ensure you consider the following when processing the image:  
- Identify and categorize the food items present.
- Estimate calories using common knowledge about typical caloric values associated with similar food appearances.

Feel free to use this methodology as a guideline for your response.
"""

# Streamlit UI
st.set_page_config(page_title="AI Nutritionist", page_icon="🍽️", layout="wide")

st.title("🍽️ AI Nutritionist App")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("📸 Upload Your Meal Image")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
    else:
        st.info("👆 Please upload an image to get started.")

with col2:
    st.header("🔍 Calorie Analysis")
    if uploaded_file is not None:
        if st.button("🧮 Calculate Calories", key="calculate"):
            with st.spinner("Analyzing your meal..."):
                image_parts = input_image_setup(uploaded_file)
                if image_parts:
                    response = get_gemini_response("calories", image_parts, input_prompt)
                    if response:
                        st.success("Analysis complete!")
                        st.markdown("### 📊 Calorie Breakdown")
                        st.write(response)
    else:
        st.warning("⚠️ Please upload an image before calculating calories.")

st.markdown("---")
st.markdown("### How to use:")
st.markdown("""
1. Upload a clear image of your meal.
2. Click the 'Calculate Calories' button.
3. Wait for the AI to analyze your meal.
4. View the calorie breakdown for each food item.
""")

st.sidebar.title("About")
st.sidebar.info(
    "This AI Nutritionist app uses Google's Gemini model to analyze "
    "food images and estimate calorie content. It's designed for educational "
    "purposes and should not be used as a substitute for professional "
    "nutritional advice."
)