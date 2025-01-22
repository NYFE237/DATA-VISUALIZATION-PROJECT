import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# App Title
st.title("Traumatic Brain Injury in the USA")
st.markdown("""
This application explores civilian and military TBI patterns using:
- Yearly trends
- Injury mechanisms
- Severity distributions
""")

# Load Data
@st.cache_data
def load_data():
    age = pd.read_csv("tbi_age.csv")
    military = pd.read_csv("tbi_military.csv")
    year = pd.read_csv("tbi_year.csv")
    return age, military, year

age, military, year = load_data()

# Sidebar Navigation
st.sidebar.header("Navigation")
section = st.sidebar.radio("Select Section", ["Introduction", "Data Exploration", "Visualizations", "Conclusions"])

# Introduction Section
if section == "Introduction":
    st.header("Introduction")
    st.markdown("""
    Every March, we observe Brain Injury Awareness Month, an initiative launched about 30 years ago. 
    This annual event aims to inform the public about how frequently brain injuries occur and to highlight 
    the support required by those affected, including their families. Traumatic brain injuries (TBIs) can 
    result from various head traumas, such as impacts, sudden movements, or penetrating wounds. 
    The consequences of a TBI may be temporary or permanent, potentially altering an individual's cognitive functions, sensory perceptions, communication abilities, or emotional responses.
   
    """)

# Data Exploration Section
elif section == "Data Exploration":
    st.header("Data Exploration")
    dataset_choice = st.selectbox("Select Dataset", ["Civilian Data", "Military Data", "Yearly Combined Data"])

    if dataset_choice == "Civilian Data":
        st.subheader("Civilian Data")
        st.write(age.head())
    elif dataset_choice == "Military Data":
        st.subheader("Military Data")
        st.write(military.head())
    else:
        st.subheader("Yearly Combined Data")
        st.write(year.head())

# Visualization Section
elif section == "Visualizations":
    st.header("Visualizations")

    ## Proportions of TBI Types Across Age Groups
    st.subheader("1. Proportions of TBI Types Across Age Groups")
    proportions_by_age_type = (
        age.groupby(['age_group', 'type'])['number_est']
        .sum()
        .unstack()
        .div(age.groupby('age_group')['number_est'].sum(), axis=0) * 100
    )

    fig, ax = plt.subplots(figsize=(14, 8))
    proportions_by_age_type.plot(kind='bar', stacked=True, colormap="coolwarm", edgecolor='black', ax=ax)
    ax.set_title('Proportions of TBI Types Across Age Groups', fontsize=16)
    ax.set_xlabel('Age Group', fontsize=14)
    ax.set_ylabel('Percentage (%)', fontsize=14)
    ax.legend(title='TBI Type', fontsize=10, loc='upper left', bbox_to_anchor=(1, 1))
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    ## Distribution of TBI Rates by Injury Mechanism
    st.subheader("2.Distribution of TBI Rates by Injury Mechanism")
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.violinplot(
        data=age,
        x="injury_mechanism",
        y="rate_est",
        inner="quartile",
        scale="width",
        palette="coolwarm",
        ax=ax
    )
    ax.set_title("Distribution of TBI Rates by Injury Mechanism", fontsize=16)
    ax.set_xlabel("Injury Mechanism", fontsize=14)
    ax.set_ylabel("Rate per 100,000", fontsize=14)
    ax.tick_params(axis='x', rotation=45, labelsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    #comments
    st.markdown("""
     **Insights:**

    * **Unintentional Falls** have the highest spread of rates, indicating their dominance across multiple cases.

    * **Motor Vehicle Crashes and Unintentionally Struck by or Against an Object** show moderate variability.

    * **Self-Harm and Assault** have consistently low rates with minimal spread.""")
    
    ## Proportions of TBI Types Over Time
    st.subheader("3.Proportions of TBI Types Over Time")
    proportions_by_year_type = (
        year.groupby(['year', 'type'])['number_est']
        .sum()
        .unstack()
        .div(year.groupby('year')['number_est'].sum(), axis=0) * 100
    )

    fig, ax = plt.subplots(figsize=(14, 8))
    proportions_by_year_type.plot(kind='bar', stacked=True, colormap="coolwarm", edgecolor='black', ax=ax)
    ax.set_title('Proportions of TBI Types Over Time', fontsize=16)
    ax.set_xlabel('Year', fontsize=14)
    ax.set_ylabel('Percentage (%)', fontsize=14)
    ax.legend(title='TBI Type', fontsize=10, loc='upper left', bbox_to_anchor=(1, 1))
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    ##Comments
    st.markdown("""
     **Observations:**
    -  Unintentional Falls:
    Their proportion has steadily increased over the years, dominating the total contribution in later years.
    -  Motor Vehicle Crashes:
    Once a major contributor, their proportion has slightly decreased over time.
    -  Unintentionally Struck by or Against an Object:
    Shows a gradual increase but remains secondary compared to falls and crashes.
    -  Other Mechanisms:
    Intentional self-harm and assault consistently contribute smaller proportions.""")
    
    # Military Analysis: Service Branch Contributions with Normalized Pie Chart
    st.subheader("4.Diagnosed Injuries by Service Branch in Military ")
    military_service_data = military.groupby('service').agg({'diagnosed': 'sum'}).reset_index()
    military_service_data = military_service_data.sort_values(by='diagnosed', ascending=True)

    # Recruitment numbers for normalization
    recruitment_numbers = {
        "Army": 4849638,
        "Navy": 3010086,
        "Marines": 1738625,
        "Air Force": 2987583
    }

    # Adding recruitment data for normalization
    military_service_data['recruited'] = military_service_data['service'].map(recruitment_numbers)
    military_service_data['diagnosed_per_1000'] = (military_service_data['diagnosed'] / military_service_data['recruited']) * 1000

    # Plotting the normalized pie chart
    fig, ax = plt.subplots(figsize=(10, 8))
    wedges, texts, autotexts = ax.pie(
        military_service_data['diagnosed_per_1000'],
        labels=military_service_data['service'],
        autopct='%1.1f%%',
        startangle=90,
        explode=(0.1, 0.1, 0.1, 0.1),
        colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'],
        wedgeprops={"edgecolor": "black", "linewidth": 1}
    )

    # Adding shadows for 3D-like effect
    for wedge in wedges:
        wedge.set_linewidth(2)
        wedge.set_edgecolor("darkgrey")

    # Customizing text and labels
    for autotext in autotexts:
        autotext.set_color("black")
        autotext.set_fontsize(12)
    for text in texts:
        text.set_fontsize(12)

    ax.set_title("Normalized Diagnosed Injuries by Service Branch (2006-2014)", fontsize=14, pad=20)
    st.pyplot(fig)
    
    ## Adding Observations
    st.markdown("""
     **Observations:**
    - **Marines**: Highest proportion of diagnosed injuries relative to recruitment numbers, indicating higher risk or exposure.
    - **Army**: While the Army has the most diagnosed injuries in absolute numbers, its proportion is moderated due to a larger recruitment base.
    - **Navy and Air Force**: Lower proportions, reflecting relatively fewer diagnosed injuries per 1,000 recruits.
    """)
    
    ## Correlation Between Diagnosed Cases and Year (By Severity and Service)
    st.subheader("5.Correlation between Diagnosed Cases and Year By Severity and Service")
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.scatterplot(
        data=military,
        x="year",
        y="diagnosed",
        hue="severity",
        style="service",
        s=100,  # Marker size
        alpha=0.8,
        palette="Set2",
        ax=ax
    )

    ax.set_title("Correlation Between Diagnosed Cases and Year (By Severity and Service)", fontsize=16)
    ax.set_xlabel("Year", fontsize=14)
    ax.set_ylabel("Number of Diagnosed Cases", fontsize=14)
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    ax.legend(title="Severity and Service", fontsize=10, loc='upper left', bbox_to_anchor=(1, 1))
    ax.grid(axis="both", linestyle="--", alpha=0.7)
    st.pyplot(fig)

    # Adding Observations
    st.markdown("""
     **Observations:**
    - **Severity Distribution**: Mild injuries dominate across all years, reflected in the larger clusters. Other severities (Moderate, Severe, Penetrating) show fewer cases but consistent presence.
    - **Trends Over Time**: Diagnosed cases are relatively stable for all severities, with some fluctuations.
    - **Service Branch Influence**: The Army contributes the most across all severities, followed by other branches with smaller case counts.

    **Insights:**
    - **Mild injuries** are the primary driver of diagnosed cases, indicating the need for targeted interventions.
    - Stable trends suggest consistent reporting, though branch-level or severity-level changes might warrant further study.
    """)
# Conclusions Section
elif section == "Conclusions":
    st.header("Conclusions")
    st.markdown("""
    **Key Findings:**
    - **Unintentional Falls** are the dominant mechanism for civilian TBIs.
    - The **Army** reports the highest number of military TBIs, primarily mild cases.
    - Normalized comparisons highlight distinct patterns between civilian and military populations.

    **Future Work:**
    - Explore regional differences.
    - Analyze intervention impacts on TBI trends.
    """)
