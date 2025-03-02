import streamlit as st
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_ip_strategy(business_name, business_type):
    """
    Generate a basic IP strategy based on business details.
    This is a placeholder function that will be expanded later.
    """
    try:
        # Simulate some strategy generation logic
        strategy_components = {
            "Technology": [
                "Patent protection for core technologies",
                "Trade secret management",
                "Software copyright registration"
            ],
            "Manufacturing": [
                "Design patent for unique product designs",
                "Trademark for brand protection",
                "Trade secret protection for manufacturing processes"
            ],
            "Software": [
                "Copyright registration for source code",
                "Patent protection for unique algorithms",
                "Trademark for software product name"
            ],
            "Consulting": [
                "Copyright for training materials",
                "Trademark for consulting brand",
                "Trade secret protection for methodologies"
            ],
            "Other": [
                "Comprehensive IP audit",
                "Custom IP protection strategy"
            ]
        }
        
        # Return strategy based on business type
        return strategy_components.get(business_type, strategy_components["Other"])
    
    except Exception as e:
        logger.error(f"Error generating IP strategy: {e}")
        logger.error(traceback.format_exc())
        return None

def main():
    try:
        st.set_page_config(page_title="IP Strategy Tool", page_icon="🚀")
        
        st.title("Intellectual Property Strategy Generator")
        
        st.write("Welcome to your IP Strategy Tool!")
        
        # Expanded business type selection
        business_types = [
            "Technology", 
            "Manufacturing", 
            "Software", 
            "Consulting", 
            "Other"
        ]
        
        # Input fields with validation
        col1, col2 = st.columns(2)
        
        with col1:
            business_name = st.text_input("Enter your business name", 
                                          help="Provide the legal or trading name of your business")
        
        with col2:
            business_type = st.selectbox("Select your business type", 
                                         business_types, 
                                         help="Choose the primary type of your business")
        
        # Additional context input
        business_description = st.text_area("Brief business description (optional)", 
                                            help="Provide additional context about your business")
        
        # Strategy generation button
        if st.button("Generate IP Strategy"):
            # Input validation
            if not business_name:
                st.warning("Please enter a business name")
            elif not business_type:
                st.warning("Please select a business type")
            else:
                # Attempt strategy generation
                try:
                    strategy = generate_ip_strategy(business_name, business_type)
                    
                    if strategy:
                        st.success(f"IP Strategy for {business_name}")
                        
                        # Display strategy in an expandable section
                        with st.expander("Recommended IP Protection Strategies"):
                            for idx, strategy_item in enumerate(strategy, 1):
                                st.markdown(f"{idx}. {strategy_item}")
                        
                        # Additional guidance
                        st.info("""
                        ### Next Steps
                        1. Consult with an IP attorney
                        2. Conduct a comprehensive IP audit
                        3. Develop a detailed protection plan
                        """)
                    else:
                        st.error("Unable to generate strategy. Please try again.")
                
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
                    logger.error(f"Unexpected error: {e}")
                    logger.error(traceback.format_exc())
    
    except Exception as e:
        st.error("A critical error occurred in the application")
        logger.critical(f"Critical application error: {e}")
        logger.critical(traceback.format_exc())

if __name__ == "__main__":
    main()
