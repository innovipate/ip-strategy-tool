import streamlit as st
import requests
import os
from dotenv import load_dotenv
import time
import hashlib

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="AI IP Strategy Generator", 
    page_icon="🚀", 
    layout="wide"
)

# Caching mechanism for API calls
@st.cache_data(show_spinner=False, ttl=3600)
def generate_comprehensive_ip_strategy(business_name, business_type, business_description):
    """
    Generate a comprehensive IP strategy using Hugging Face's free inference API
    with advanced error handling and caching
    """
    # Retrieve Hugging Face credentials
    huggingface_username = os.getenv('huggingface_username', '')
    huggingface_token = os.getenv('huggingface_token', '')

    # Validate credentials
    if not huggingface_token:
        st.error("Hugging Face API token is missing. Please configure your credentials.")
        return None

    # Hugging Face API endpoint
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {
        "Authorization": f"Bearer {huggingface_token}"
    }

    # Create a unique hash for caching
    cache_key = hashlib.md5(
        f"{business_name}{business_type}{business_description}".encode()
    ).hexdigest()

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
                "top_p": 0.9,
                "repetition_penalty": 1.2
            }
        }

        # Make API request with timeout
        response = requests.post(
            API_URL, 
            headers=headers, 
            json=payload, 
            timeout=45
        )
        
        if response.status_code == 200:
            # Extract generated text
            generated_text = response.json()[0]['generated_text']
            
            # Clean up the response
            strategy = generated_text.split(prompt)[-1].strip()
            return strategy
        else:
            st.error(f"API Error: Unable to generate strategy. Status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        st.error(f"Network Error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected Error: {str(e)}")
        return None

def main():
    st.title("🚀 AI-Powered Intellectual Property Strategy Generator")
    
    # Business Type Selection
    business_types = [
        "Technology", "Manufacturing", "Software", 
        "Consulting", "Biotechnology", "Healthcare", 
        "E-commerce", "Other"
    ]

    # Input columns
    col1, col2 = st.columns(2)
    
    with col1:
        business_name = st.text_input(
            "Business Name", 
            help="Enter the legal or trading name of your business",
            max_chars=100
        )
    
    with col2:
        business_type = st.selectbox(
            "Business Type", 
            business_types, 
            help="Select the most appropriate category for your business"
        )

    # Business Description
    business_description = st.text_area(
        "Business Description", 
        help="Provide a brief overview of your business, its core activities, and unique value proposition",
        height=150,
        max_chars=500
    )

    # Generate Strategy Button
    if st.button("Generate IP Strategy", type="primary"):
        if not all([business_name, business_type, business_description]):
            st.warning("Please fill in all fields before generating the strategy.")
        else:
            with st.spinner("Generating comprehensive IP strategy..."):
                strategy = generate_comprehensive_ip_strategy(
                    business_name, business_type, business_description
                )
                
                if strategy:
                    st.markdown("## 📄 Your Comprehensive IP Strategy")
                    st.markdown(strategy)
                    
                    # Download option
                    st.download_button(
                        label="Download Strategy",
                        data=strategy,
                        file_name=f"{business_name}_ip_strategy.md",
                        mime="text/markdown"
                    )
                else:
                    st.error("Failed to generate IP strategy. Please try again.")

    # Footer
    st.markdown("---")
    st.markdown("""
    ### 💡 About This Tool
    - AI-powered IP strategy generation using advanced language models
    - Tailored recommendations based on your business type
    - Free and confidential strategy insights
    """)

if __name__ == "__main__":
    main()
