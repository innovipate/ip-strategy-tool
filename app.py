import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_comprehensive_ip_strategy(business_name, business_type, business_description):
    """
    Generate a comprehensive IP strategy using Hugging Face's free inference API
    """
    # Hugging Face API endpoint
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {
        "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY', '')}"
    }

    # Detailed prompt for IP strategy generation
    prompt = f"""
    You are an expert IP strategy consultant. Provide a comprehensive Intellectual Property (IP) strategy for a {business_type} business named {business_name}.

    Business Description: {business_description}

    Comprehensive IP Strategy Outline:

    1. IP Landscape Analysis
    - Detailed assessment of current IP protection status
    - Identification of potential IP risks and opportunities
    - Competitive IP landscape evaluation

    2. Recommended IP Protection Strategies
    - Comprehensive patent strategy
    - Trademark protection approach
    - Copyright considerations and recommendations
    - Trade secret management plan

    3. Detailed Recommendations
    - Specific, actionable points for each IP type
    - Estimated costs and implementation timelines
    - Potential challenges and strategic mitigation approaches

    4. Strategic Insights
    - Long-term IP positioning strategy
    - Innovation protection methodology
    - Potential IP monetization strategies

    5. Compliance and Legal Considerations
    - Regulatory compliance framework
    - International IP protection strategies
    - Enforcement and defense mechanisms

    6. Financial Implications
    - Comprehensive investment requirements
    - Potential return on IP investment
    - Detailed cost-benefit analysis

    Provide a professional, in-depth, and actionable strategy tailored specifically to a {business_type} business.

    Response Format: Provide a structured, markdown-formatted response with clear sections and actionable insights.
    """

    try:
        # Payload for Hugging Face API
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 4000,
                "temperature": 0.7,
                "top_p": 0.9
            }
        }

        # Make API request
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            # Extract generated text
            generated_text = response.json()[0]['generated_text']
            
            # Clean up the response
            strategy = generated_text.split(prompt)[-1].strip()
            return strategy
        else:
            return f"Error: Unable to generate strategy. Status code: {response.status_code}"

    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    st.set_page_config(page_title="AI IP Strategy Generator", page_icon="🚀")
    
    st.title("AI-Powered Intellectual Property Strategy Generator")
    
    # Input columns
    col1, col2 = st.columns(2)
    
    with col1:
        business_name = st.text_input("Business Name", 
                                      help="Enter the legal or trading name of your business")
    
    with col2:
        business_types = [
            "Technology", 
            "Manufacturing", 
            "Software", 
            "Consulting", 
            "Biotechnology",
            "Healthcare",
            "E-commerce",
            "Other"
        ]
        business_type = st.selectbox("Business Type", business_types)
    
    # Business description
    business_description = st.text_area(
        "Business Description", 
        help="Provide a brief overview of your business, key products/services, and unique value proposition",
        height=150
    )
    
    # API Key input (optional, for demonstration)
    api_key = st.text_input(
        "Hugging Face API Key (optional)", 
        type="password", 
        help="If you have a Hugging Face API key, enter it here."
    )
    
    # Strategy Generation Button
    if st.button("Generate Comprehensive IP Strategy"):
        # Validate inputs
        if not business_name or not business_type:
            st.warning("Please enter business name and select business type")
        else:
            # Use provided API key or fall back to environment variable
            if api_key:
                os.environ['HUGGINGFACE_API_KEY'] = api_key
            
            # Show loading spinner
            with st.spinner('Generating comprehensive IP strategy...'):
                strategy = generate_comprehensive_ip_strategy(
                    business_name, 
                    business_type, 
                    business_description
                )
            
            # Display strategy
            if strategy.startswith("Error"):
                st.error(strategy)
            else:
                st.success(f"IP Strategy for {business_name}")
                
                # Expandable strategy sections
                with st.expander("Comprehensive IP Strategy", expanded=True):
                    st.markdown(strategy)
                
                # Additional guidance
                st.info("""
                ### Next Steps
                1. Review the generated strategy carefully
                2. Consult with an IP attorney
                3. Develop a detailed implementation plan
                4. Regularly review and update your IP strategy
                """)

if __name__ == "__main__":
    main()
