"""
Custom styles and components for the Streamlit app
"""

import streamlit as st

def inject_custom_css():
    """Inject custom CSS styles into the Streamlit app"""
    st.markdown("""
    <style>
    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        margin: 1rem;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #1f4e79 0%, #2d5aa0 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    /* Form styling */
    .stSelectbox > div > div > select {
        background-color: #f8f9fa;
        border: 2px solid #1f4e79;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div > select:focus {
        border-color: #2d5aa0;
        box-shadow: 0 0 0 3px rgba(45, 90, 160, 0.1);
    }
    
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #1f4e79 0%, #2d5aa0 100%);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    /* Prediction card */
    .prediction-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 15px 30px rgba(0,0,0,0.2);
        margin: 1rem 0;
        animation: fadeInUp 0.6s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        text-align: center;
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    
    /* Info cards */
    .info-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #6c757d 0%, #495057 100%);
    }
    
    .css-1d391kg .css-1v0mbdj {
        color: white;
    }
    
    /* Example buttons */
    .example-button {
        background: linear-gradient(45deg, #ff6b6b, #feca57);
        border: none;
        border-radius: 20px;
        padding: 1rem;
        color: white;
        font-weight: bold;
        width: 100%;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .example-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Success/Error message styling */
    .stAlert > div {
        border-radius: 10px;
        border: none;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Custom animations */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse-animation {
        animation: pulse 2s infinite;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
            margin: 0.5rem;
        }
        
        .main-header {
            padding: 1rem;
        }
        
        .prediction-card {
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def create_animated_metric(label, value, icon="📊"):
    """Create an animated metric card"""
    return f"""
    <div class="metric-card pulse-animation">
        <h3 style="margin: 0; color: #333;">{icon} {label}</h3>
        <h2 style="margin: 10px 0; color: #6c757d; font-size: 2rem;">{value}</h2>
    </div>
    """

def create_info_card(title, content, icon="ℹ️"):
    """Create an information card"""
    return f"""
    <div class="info-card">
        <h4 style="margin: 0 0 10px 0;">{icon} {title}</h4>
        <p style="margin: 0; opacity: 0.9;">{content}</p>
    </div>
    """

def create_feature_explanation():
    """Create feature explanation cards"""
    features_info = {
        "🎪 Metascore": "Professional critics' aggregate score (0-100). Higher scores typically correlate with better user reception.",
        "📅 Release Month": "Launch timing affects user scores. Holiday releases (Nov-Dec) often perform differently.",
        "👨‍💻 Developer": "Studio reputation and track record influence user expectations and ratings.",
        "🎮 Platform": "Gaming platform affects audience and technical performance expectations.",
        "🎭 Genre": "Game category influences user base and scoring patterns."
    }
    
    st.markdown("### 🧠 How It Works")
    st.markdown("This AI model considers these key factors:")
    
    cols = st.columns(2)
    for i, (feature, explanation) in enumerate(features_info.items()):
        with cols[i % 2]:
            st.markdown(create_info_card(feature, explanation), unsafe_allow_html=True)