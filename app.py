import re
import streamlit as st

# ==================================================
# Page configuration
# ==================================================
st.set_page_config(
    page_title="NYC 311 Service Requests Dashboard",
    layout="wide"
)

# ==================================================
# Custom CSS — Dark base + Purple–Pink–Grey palette
# ==================================================
st.markdown("""
<style>

/* ===== Global base ===== */
html, body, [class*="css"] {
    font-family: "Segoe UI", Arial, sans-serif;
    background-color: #0f0f14;
    color: #e6e6eb;
}

/* ===== Main container spacing ===== */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* ===== Sidebar ===== */
section[data-testid="stSidebar"] {
    background-color: #14141c;
    border-right: 1px solid #2a2a35;
}

/* ===== Headings ===== */
h1 {
    color: #e6e6eb;
    font-weight: 600;
}

h2 {
    color: #c9c3e6;
    font-weight: 500;
}

h3 {
    color: #b07aa1;
    font-weight: 500;
}

/* ===== Text ===== */
p, li, label {
    color: #b3b3bd;
    font-size: 0.95rem;
}

/* ===== Links ===== */
a {
    color: #e6b6cf;
    text-decoration: none;
}

a:hover {
    color: #f1c7d9;
}

/* ===== Widgets ===== */
div[data-testid="stRadio"] label {
    color: #c9c3e6;
}

/* ===== Divider ===== */
hr {
    border: none;
    border-top: 1px solid #2a2a35;
    margin: 1.5rem 0;
}

/* ===== Code blocks ===== */
code {
    background-color: #1c1c26;
    color: #f1c7d9;
    border-radius: 4px;
}

/* ===== Remove footer ===== */
footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# Tableau Public URLs
# ==================================================
TABLEAU_URLS = {
    "Dashboard 1": "https://public.tableau.com/app/profile/zarish.asim/viz/Project_17660793660610/TemporalPattrensofNYC?publish=yes",
    "Dashboard 2": "https://public.tableau.com/app/profile/zarish.asim/viz/Project_17660793660610/Dashboard2?publish=yes",
    "Dashboard 3": "https://public.tableau.com/app/profile/zarish.asim/viz/Project_17660793660610/Dashboard3?publish=yes",
}

def tableau_embed_url(shared_url: str) -> str:
    base = shared_url.split("?")[0]
    m = re.search(r"/viz/([^/]+)/([^/]+)$", base)
    if m:
        workbook, sheet = m.group(1), m.group(2)
        return f"https://public.tableau.com/views/{workbook}/{sheet}?:showVizHome=no&:embed=yes"
    return shared_url

def embed_dashboard(url: str, height: int = 900):
    st.components.v1.iframe(
        tableau_embed_url(url),
        height=height,
        scrolling=True
    )

# ==================================================
# Google Drive embeds (YOUR FILES)
# ==================================================
REPORT_EMBED = "https://drive.google.com/file/d/1RMyoIJ3h8hKZL9LtiFtMXGgJ2aUxMv9y/preview"
PRESENTATION_EMBED = "https://drive.google.com/file/d/1-3LfSX-yjGqdXMi-RH6rT4XFdU_D4ov0/preview"

# ==================================================
# Sidebar Navigation
# ==================================================
with st.sidebar:
    st.markdown("### NYC 311 Dashboard")
    page = st.radio(
        "",
        [
            "Overview",
            "Dashboard 1",
            "Dashboard 2",
            "Dashboard 3",
            "Report",
            "Presentation",
            "Video",
            "Tools"
        ]
    )

# ==================================================
# Pages
# ==================================================
if page == "Overview":
    st.markdown("## NYC 311 Service Requests Analysis")

    st.markdown("""
This application presents a comprehensive and interactive analysis of **NYC 311 Service Requests**,
delivered through professionally designed **Tableau dashboards** embedded within a
**Streamlit web application**.

The project investigates how public service complaints are reported, distributed,
and resolved across New York City, transforming large-scale civic data into
clear, actionable insights.
""")

    st.markdown("---")

    st.markdown("### Analytical Focus")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
- **Temporal Trends**  
  Identification of long-term patterns, seasonal fluctuations, and peak reporting periods.

- **Geographic Distribution**  
  Comparison of complaint volumes and types across boroughs to reveal spatial differences.
""")

    with col2:
        st.markdown("""
- **Service Performance**  
  Analysis of complaint status, resolution behaviour, and operational efficiency.

- **Behavioural Patterns**  
  Examination of reporting behaviour by time of day, month, and year.
""")

    st.markdown("---")

    st.markdown("### Dataset Overview")

    st.markdown("""
The analysis is based on the **NYC 311 Service Requests dataset**, which contains
detailed records of non-emergency complaints submitted by residents across the city.
""")

    with st.expander("View dataset details"):
        st.markdown("""
**Dataset Name:** NYC 311 Service Requests  
**Data Domain:** Civic and Urban Services  

**Key Attributes:**
- Complaint creation and closure timestamps  
- Complaint categories and descriptors  
- Borough and location information  
- Responsible city agencies  
- Complaint status and service outcomes  
""")

    st.markdown("---")

    st.markdown("### Project Significance")

    st.markdown("""
By converting raw civic data into structured and interactive dashboards,
this application demonstrates how data analytics can support transparency,
operational insight, and data-driven decision-making in urban environments.
""")

elif page == "Dashboard 1":
    st.markdown("## Temporal Patterns of NYC 311 Complaints")
    st.markdown("This dashboard examines how complaint volumes change over time.")
    st.markdown("---")
    embed_dashboard(TABLEAU_URLS["Dashboard 1"])

elif page == "Dashboard 2":
    st.markdown("## Geographic Distribution and Status Analysis")
    st.markdown("This dashboard explores spatial complaint patterns and service status.")
    st.markdown("---")
    embed_dashboard(TABLEAU_URLS["Dashboard 2"])

elif page == "Dashboard 3":
    st.markdown("## Patterns, Seasonality, and Key Insights")
    st.markdown("This dashboard highlights behavioural, seasonal, and performance trends.")
    st.markdown("---")
    embed_dashboard(TABLEAU_URLS["Dashboard 3"])

elif page == "Report":
    st.markdown("## Project Report")
    st.markdown("---")
    st.components.v1.iframe(
        REPORT_EMBED,
        height=900,
        scrolling=True
    )

elif page == "Presentation":
    st.markdown("## Project Presentation")
    st.markdown("---")
    st.components.v1.iframe(
        PRESENTATION_EMBED,
        height=900,
        scrolling=True
    )

elif page == "Video":
    st.markdown("## Dashboard Walkthrough Video")
    st.code("PASTE_YOUR_VIDEO_LINK_HERE")

elif page == "Tools":
    st.markdown("## Tools and Technologies")
    st.markdown("""
- **Tableau Public** – Interactive dashboard development  
- **Streamlit** – Web application framework  
- **Python** – Application integration  
- **GitHub** – Version control and deployment  
""")
