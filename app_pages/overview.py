import streamlit as st

def overview_page():
    if "logged_in_user" not in st.session_state:
        st.error("Login is required")
        return
    st.subheader("Emissions")
    st.write(
        "Emissions refer to the release of gases, particles, or pollutants into the atmosphere from various sources. "
        "These emissions can originate from natural processes (such as volcanic eruptions or wildfires) or human activities "
        "(such as burning fossil fuels, industrial processes, and agriculture)."
    )
    st.write("The emissions can be categorized into three scopes:")
    st.write(
        "These three categories are used in Greenhouse Gas (GHG) accounting to measure and report emissions from different sources. "
        "They help organizations track their carbon footprint and take action to reduce it."
    )
    
    st.subheader("Scope 1")
    st.write("(Direct Emissions) - Emissions from sources owned or controlled by a company.")
    
    st.subheader("Scope 2")
    st.write("(Indirect Emissions) - Emissions from the generation of purchased electricity, heating, or cooling consumed by a company.")
    
    st.subheader("Scope 3")
    st.write("(Indirect Emissions from the Supply Chain and Other Activities) – Emissions from sources not owned or controlled by the company but related to its activities.")
    
    st.subheader("Why These Emissions Matter")
    st.write(
        "Addressing all three scopes is vital for achieving net-zero goals, improving sustainability, meeting regulatory requirements, "
        "and gaining consumer trust in an increasingly environmentally conscious world. 🌍💚"
    )
    
    st.subheader("How Do We Calculate These Emissions")
    st.markdown("<h4>Emissions = Activity Data x Emission Factor</h4>", unsafe_allow_html=True)
    
    st.subheader("Why Are These Important")
    st.write(
        """
        **Why Are Emissions Important?**
        
        - **Climate Change:** GHGs trap heat in the atmosphere, contributing to global warming.
        - **Air Pollution & Health Risks:** Pollutants can cause respiratory issues, heart diseases, and other health problems.
        - **Environmental Impact:** Emissions lead to phenomena such as acid rain, ocean acidification, and ecosystem disruption.
        - **Mitigation Efforts:** Strategies like renewable energy adoption, energy efficiency, carbon capture, and policy initiatives (e.g., the Paris Agreement) are key to reducing emissions.
        """
    )

