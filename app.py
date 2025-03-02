import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY', '')

def generate_comprehensive_ip_strategy(business_name, business_type, business_description):
    """
    Generate a comprehensive IP strategy using OpenAI's GPT model
    """
    if not openai.api_key:
        return "Error: OpenAI API key is not configured"
    
    try:
        prompt = f"""
        Provide a comprehensive Intellectual Property (IP) strategy for a {business_type} business named {business_name}.

        Business Description: {business_description}

        The IP strategy should cover:

        1. IP Landscape Analysis
        - Current IP protection status
        - Potential IP risks and opportunities
        - Competitive IP landscape

        2. Recommended IP Protection Strategies
        - Patent strategy
        - Trademark protection
        - Copyright considerations
        - Trade secret management

        3. Detailed Recommendations
        - Specific action points for each IP type
        - Estimated costs and timelines
        - Potential challenges and mitigation strategies

        4. Strategic Insights
        - Long-term IP positioning
        - Innovation protection approach
        - Potential monetization strategies

        5. Compliance and Legal Considerations
        - Regulatory compliance
        - International IP protection
        - Enforcement strategies

        6. Financial Implications
        - Investment required
        - Potential ROI from IP protection
        - Cost-benefit analysis

        Provide a professional, detailed, and actionable strategy that is tailored to the specific needs of a {business_type} business.
        """

        response = openai.ChatCompletion.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an expert IP strategy consultant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,
            temperature=0.7
        )

        return response.choices[0].message.content

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
        "OpenAI API Key (optional)", 
        type="password", 
        help="If you have an OpenAI API key, enter it here. Otherwise, a default key will be used."
    )
    
    # Strategy Generation Button
    if st.button("Generate Comprehensive IP Strategy"):
        # Validate inputs
        if not business_name or not business_type:
            st.warning("Please enter business name and select business type")
        else:
            # Use provided API key or fall back to environment variable
            if api_key:
                openai.api_key = api_key
            
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
