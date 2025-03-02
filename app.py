import streamlit as st

def main():
    st.set_page_config(page_title="IP Strategy Tool", page_icon="🚀")
    
    st.title("Intellectual Property Strategy Generator")
    
    st.write("Welcome to your IP Strategy Tool!")
    
    # Basic input for business details
    business_name = st.text_input("Enter your business name")
    business_type = st.selectbox("Select your business type", [
        "Technology", 
        "Manufacturing", 
        "Software", 
        "Consulting", 
        "Other"
    ])
    
    if st.button("Generate IP Strategy"):
        if business_name and business_type:
            st.success(f"Generating IP strategy for {business_name} in {business_type} sector...")
            # Placeholder for future IP strategy generation logic
        else:
            st.warning("Please enter business name and select business type")

if __name__ == "__main__":
    main()
