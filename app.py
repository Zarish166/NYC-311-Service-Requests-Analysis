import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="NYC 311 Data Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- ANIMATED 3D BACKGROUND (THREE.JS) ---
# We inject this at the very top to ensure it sits behind all Streamlit elements
st.markdown("""
    <div id="starfield-container" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -1; overflow: hidden; background: #020205;">
        <canvas id="starfield-canvas"></canvas>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        const canvas = document.getElementById('starfield-canvas');
        const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.setSize(window.innerWidth, window.innerHeight);

        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 1, 1000);
        camera.position.z = 1;
        camera.rotation.x = Math.PI / 2;

        const starGeo = new THREE.BufferGeometry();
        const starCount = 10000;
        const positions = new Float32Array(starCount * 3);
        for (let i = 0; i < starCount * 3; i++) {
            positions[i] = Math.random() * 800 - 400;
        }
        starGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));

        const starMaterial = new THREE.PointsMaterial({
            color: 0xffffff,
            size: 0.8,
            transparent: true,
            opacity: 0.8,
            blending: THREE.AdditiveBlending
        });

        const stars = new THREE.Points(starGeo, starMaterial);
        scene.add(stars);

        function animate() {
            const positions = starGeo.attributes.position.array;
            for (let i = 0; i < positions.length; i += 3) {
                positions[i + 1] -= 0.15; // Vertical drift
                if (positions[i + 1] < -400) {
                    positions[i + 1] = 400;
                }
            }
            starGeo.attributes.position.needsUpdate = true;
            stars.rotation.y += 0.0005;
            renderer.render(scene, camera);
            requestAnimationFrame(animate);
        }

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });

        animate();
    </script>
    """, unsafe_allow_html=True)

# --- CUSTOM STYLES (MATCHING CANVAS AESTHETIC) ---
st.markdown("""
    <style>
    /* Make Streamlit background transparent to see the 3D stars */
    .stApp {
        background-color: transparent !important;
        color: #e6e6eb;
    }
    
    /* Overlay a soft gradient to improve readability */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: radial-gradient(circle at top right, rgba(176, 122, 161, 0.05), transparent 60%);
        pointer-events: none;
        z-index: -1;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(5, 5, 10, 0.4) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Custom Headers */
    .main-title {
        font-size: 4rem;
        font-weight: 900;
        letter-spacing: -0.05em;
        line-height: 1;
        margin-bottom: 0.5rem;
        color: white;
    }
    
    .gradient-text {
        background: -webkit-linear-gradient(#b07aa1, #e6b6cf);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Cards and Containers */
    .glass-card {
        background: rgba(13, 13, 20, 0.4);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    .stat-card {
        background: rgba(13, 13, 20, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 1.25rem;
        text-align: center;
        backdrop-filter: blur(5px);
    }
    
    .stat-val {
        font-size: 1.8rem;
        font-weight: 900;
        color: white;
    }
    
    .stat-label {
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        color: #b3b3bd;
    }
    
    /* Hide Streamlit Branded Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Adjust for Streamlit's default padding */
    .block-container {
        padding-top: 2rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA CONFIGURATION ---
TABLEAU_URLS = {
    "Temporal Flow": "https://public.tableau.com/views/Project_17660793660610/TemporalPattrensofNYC?:showVizHome=no&:embed=yes",
    "Spatial Reach": "https://public.tableau.com/views/Project_17660793660610/Dashboard2?:showVizHome=no&:embed=yes",
    "Performance": "https://public.tableau.com/views/Project_17660793660610/Dashboard3?:showVizHome=no&:embed=yes",
}

DRIVE_EMBEDS = {
    "Technical Report": "https://drive.google.com/file/d/1RMyoIJ3h8hKZL9LtiFtMXGgJ2aUxMv9y/preview",
    "Executive Presentation": "https://drive.google.com/file/d/1-3LfSX-yjGqdXMi-RH6rT4XFdU_D4ov0/preview",
    "Video Walkthrough": "https://drive.google.com/file/d/1HaoVQBW6YRdLzLoxef232iHtU6TeI9IP/preview"
}

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown('<h1 style="font-size: 1.8rem; font-weight: 900; color: white;">NYC <span style="color: #b07aa1;">311</span></h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.2em; color: #666675; margin-top: -15px;">Data Intelligence</p>', unsafe_allow_html=True)
    st.write("---")
    
    page = st.radio(
        "Navigation",
        ["Overview", "Temporal Flow", "Spatial Reach", "Performance", "Technical Report", "Executive Presentation", "Video Walkthrough", "Tools"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.caption("🟢 Live Feed Synchronized")

# --- MAIN CONTENT AREA ---

if page == "Overview":
    st.markdown('<h1 class="main-title">Citywide <span class="gradient-text">Analytics</span></h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #b3b3bd; font-weight: 500; letter-spacing: 0.2em; text-transform: uppercase; font-size: 0.8rem;">Mission Intelligence Dashboard</p>', unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
        <div class="glass-card">
            <p style="font-size: 1.5rem; line-height: 1.6; color: #d1d1d6;">
                Transforming millions of raw civic data points into a <b style="color: white;">dynamic visual narrative</b> of New York City's heartbeat. Explore temporal fluctuations, spatial disparities, and agency responsiveness in real-time.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Stats Grid
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="stat-card"><p class="stat-label">Avg Volume</p><p class="stat-val">2.4M+</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-card"><p class="stat-label">Agencies</p><p class="stat-val">25+</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-card"><p class="stat-label">Uptime</p><p class="stat-val">99.9%</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="stat-card"><p class="stat-label">Latency</p><p class="stat-val">45ms</p></div>', unsafe_allow_html=True)

    st.write("## Intelligence Modules")
    
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.markdown("""
            <div class="glass-card">
                <h3 style="color: white; font-weight: 900;">Temporal Trends</h3>
                <p style="color: #b3b3bd; font-size: 0.9rem;">Identification of long-term patterns, seasonal fluctuations, and peak reporting periods.</p>
            </div>
            <div class="glass-card">
                <h3 style="color: white; font-weight: 900;">Service Performance</h3>
                <p style="color: #b3b3bd; font-size: 0.9rem;">Analysis of complaint status, resolution behaviour, and operational efficiency.</p>
            </div>
        """, unsafe_allow_html=True)
    with m_col2:
        st.markdown("""
            <div class="glass-card">
                <h3 style="color: white; font-weight: 900;">Geographic Distribution</h3>
                <p style="color: #b3b3bd; font-size: 0.9rem;">Comparison of complaint volumes across boroughs to reveal spatial differences.</p>
            </div>
            <div class="glass-card">
                <h3 style="color: white; font-weight: 900;">Behavioural Patterns</h3>
                <p style="color: #b3b3bd; font-size: 0.9rem;">Examination of reporting behaviour by time of day, month, and year.</p>
            </div>
        """, unsafe_allow_html=True)

    # Project Significance
    st.markdown("""
        <div style="background: linear-gradient(135deg, #b07aa1, #6a4a61); padding: 3rem; border-radius: 3rem; color: white; margin-top: 2rem;">
            <h3 style="font-weight: 900; text-transform: uppercase; letter-spacing: 0.2em; margin-bottom: 1rem;">Project Significance</h3>
            <p style="font-size: 1.5rem; font-weight: 500; font-style: italic;">
                "By converting raw civic data into structured and interactive dashboards, this application demonstrates how data analytics can support transparency and data-driven decision-making in urban environments."
            </p>
        </div>
    """, unsafe_allow_html=True)

elif page in TABLEAU_URLS:
    st.markdown(f'<h1 class="main-title">{page}</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #b3b3bd; font-weight: 700; text-transform: uppercase; letter-spacing: 0.3em; font-size: 0.7rem; margin-bottom: 2rem;">Tableau Virtual Engine Active</p>', unsafe_allow_html=True)
    components.iframe(TABLEAU_URLS[page], height=850, scrolling=False)

elif page in DRIVE_EMBEDS:
    st.markdown(f'<h1 class="main-title">{page}</h1>', unsafe_allow_html=True)
    if page == "Video Walkthrough":
        st.video("https://drive.google.com/file/d/1HaoVQBW6YRdLzLoxef232iHtU6TeI9IP/view?usp=sharing")
        st.markdown("""
            <div style="text-align: center; margin-top: 2rem;">
                <a href="https://drive.google.com/file/d/1HaoVQBW6YRdLzLoxef232iHtU6TeI9IP/view?usp=sharing" target="_blank" style="text-decoration: none;">
                    <button style="background: #b07aa1; color: white; border: none; padding: 1rem 2rem; border-radius: 2rem; font-weight: 900; cursor: pointer;">
                        OPEN IN SYSTEM SOURCE
                    </button>
                </a>
            </div>
        """, unsafe_allow_html=True)
    else:
        components.iframe(DRIVE_EMBEDS[page], height=850)

elif page == "Tools":
    st.markdown('<h1 class="main-title">System <span class="gradient-text">Architecture</span></h1>', unsafe_allow_html=True)
    t_col1, t_col2, t_col3, t_col4 = st.columns(4)
    tools = [
        {"name": "Streamlit", "desc": "App Framework"},
        {"name": "Python", "desc": "Logic Engine"},
        {"name": "Tableau", "desc": "Vizualization"},
        {"name": "Lucide", "desc": "Iconography"}
    ]
    for i, tool in enumerate(tools):
        with [t_col1, t_col2, t_col3, t_col4][i]:
            st.markdown(f"""
                <div class="glass-card" style="text-align: center;">
                    <h4 style="color: white; font-weight: 900; margin-bottom: 0;">{tool['name']}</h4>
                    <p style="color: #b3b3bd; font-size: 0.7rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0.1em;">{tool['desc']}</p>
                </div>
            """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
f_col1, f_col2 = st.columns([2, 1])
with f_col1:
    st.markdown("""
        <h4 style="color: #b07aa1; font-weight: 900; text-transform: uppercase; letter-spacing: 0.4em; font-size: 0.7rem;">Lead Data Engineers</h4>
        <div style="margin-bottom: 1.5rem;">
            <span style="font-size: 1.5rem; font-weight: 900; color: white;">Zarish Asim</span>
            <span style="color: #666675; font-family: monospace; margin-left: 1rem;">2022640</span><br/>
            <span style="font-size: 0.7rem; font-weight: 900; color: #b3b3bd;">u2022640@giki.edu.pk</span>
        </div>
        <div>
            <span style="font-size: 1.5rem; font-weight: 900; color: white;">Adina Kamran</span>
            <span style="color: #666675; font-family: monospace; margin-left: 1rem;">2022044</span><br/>
            <span style="font-size: 0.7rem; font-weight: 900; color: #b3b3bd;">u2022044@giki.edu.pk</span>
        </div>
    """, unsafe_allow_html=True)
with f_col2:
    st.markdown("""
        <div style="text-align: right;">
            <p style="font-size: 2rem; font-weight: 900; color: rgba(255,255,255,0.05); font-style: italic; margin-bottom: 0;">INTEL SYSTEM 311</p>
            <p style="color: #b3b3bd; font-size: 0.6rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0.3em;">Developed for GIKI Data Lab © 2025</p>
        </div>
    """, unsafe_allow_html=True)