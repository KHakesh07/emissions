import streamlit as st
def Overview():
    st.subheader("Emissions")
    st.write("Emissions refer to the release of gases, particles, or pollutants into the atmosphere from various sources. These emissions can originate from natural processes (such as volcanic eruptions or wildfires) or human activities (such as burning fossil fuels, industrial processes, and agriculture).")
    st.write("The emissions can be categorized into three scopes:")
    st.write("These three categories are used in Greenhouse Gas (GHG) accounting to measure and report emissions from different sources. They help organizations track their carbon footprint and take action to reduce it.")
    st.subheader("Scope 1")
    st.write("(Direct Emissions) - Emissions from sources owned or controlled by a company")
    st.subheader("Scope 2")
    st.write("(Indirect Emissions) - Emissions from the generation of purchased electricity, heating, or cooling purchased by a company")
    st.subheader("Scope 3")
    st.write("(Indirect Emissions from the Supply Chain and Other Activities) – Emissions from sources not owned or controlled by the company but related to its activities")

    st.subheader("Why These emissions Matters")
    st.write("Addressing all three scopes is vital for achieving net-zero goals, improving sustainability, meeting regulatory requirements, and gaining consumer trust in a world increasingly focused on environmental responsibility. 🌍💚")

    st.subheader("How Do We Calculate These Emissions")

    st.html(
        "<h4>Emissions=Activity Data x Emission Factor</h4>"
    )

    st.subheader("Why Are These Important")
    st.write("""Why Are Emissions Important?
    Climate Change: GHGs trap heat in the atmosphere, leading to global warming.
    Air Pollution & Health Risks: Pollutants cause respiratory diseases, heart problems, and other health issues.
    Environmental Impact: Acid rain, ocean acidification, and habitat destruction.
    Efforts to reduce emissions include renewable energy adoption, energy efficiency, carbon capture, and policies like the Paris Agreement. 🚀🌍""")