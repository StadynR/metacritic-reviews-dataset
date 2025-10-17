import streamlit as st
from styles import inject_custom_css, create_animated_metric, create_feature_explanation
from utils import validate_inputs, load_model, load_enhanced_dataset, predict_game_score
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import os

# Configure page settings
st.set_page_config(
    page_title="🎮 Metacritic Game Score Predictor",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

def create_score_gauge(score):
    """Create a beautiful gauge chart for the prediction score"""
        
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Predicted User Score", 'font': {'size': 24, 'color': 'white'}},
        delta = {'reference': 7.0, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
        gauge = {
            'axis': {'range': [None, 10], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 5], 'color': '#ff4444'},
                {'range': [5, 7], 'color': '#ffaa44'},
                {'range': [7, 8.5], 'color': '#44aa44'},
                {'range': [8.5, 10], 'color': '#44ff44'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 9
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white", 'family': "Arial"},
        height=400
    )
    
    return fig

def get_popular_options(df):
    """Get popular options for dropdowns"""
    if df is None:
        return {}, {}, {}, {}
    
    try:
        developers = sorted(df['developer'].unique())
        platforms = sorted(df['platform'].unique())
        genres = sorted(df['genre'].unique())
        manufacturers = sorted(df['manufacturer'].unique())
        
        return developers, platforms, genres, manufacturers
    except Exception:
        return [], [], [], []

def show_data_insights(df):
    """Show interesting insights about the dataset"""
    if df is None:
        return
        
    st.subheader("📊 Dataset Insights")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Games", len(df))
    
    with col2:
        st.metric("Average Score", f"{df['metascore'].mean():.1f}")
    
    with col3:
        st.metric("Unique Developers", df['developer'].nunique())
    
    with col4:
        st.metric("Platforms", df['platform'].nunique())

def main():
    # Inject custom CSS styles
    inject_custom_css()
    # else:
    # # Fallback basic styling
    # st.markdown("""
    # <style>
    # .main-header {
    #     background: linear-gradient(90deg, #1f4e79 0%, #2d5aa0 100%);
    #     padding: 2rem;
    #     border-radius: 15px;
    #     text-align: center;
    #     color: white;
    #     margin-bottom: 2rem;
    #     box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    # }
    # .prediction-card {
    #     background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    #     padding: 2rem;
    #     border-radius: 15px;
    #     text-align: center;
    #     color: white;
    #     box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    # }
    # </style>
    # """, unsafe_allow_html=True)

    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🎮 Metacritic Game Score Predictor</h1>
        <p>Predict user scores for video games using advanced machine learning!</p>
    </div>
    """, unsafe_allow_html=True)

    # Load data and model
    df_enhanced = load_enhanced_dataset()
    model = load_model()
    
    if df_enhanced is None or model is None:
        st.stop()

    # Sidebar for additional info
    with st.sidebar:
        st.header("ℹ️ About This App")
        st.markdown("""
        This app uses machine learning to predict Metacritic user scores based on:
        - **🎪 Metascore**: Professional critic score
        - **📅 Release timing**: Month of release
        - **👨‍💻 Developer**: Game development studio
        - **🎮 Platform**: Gaming platform
        - **🎭 Genre**: Game category
        - **🏭 Manufacturer**: Platform manufacturer
        """)
        
        # Show dataset insights
        show_data_insights(df_enhanced)
        
        st.markdown("---")
        
        # Add feature explanation if custom styles are available
        create_feature_explanation()

        st.markdown("🔗 **Data Source**: Metacritic Reviews Dataset")
        st.markdown("🤖 **Model**: Random Forest Regressor")

    # Get options for dropdowns
    developers, platforms, genres, manufacturers = get_popular_options(df_enhanced)

    # Create two columns for input
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("🎯 Game Information")
        
        # Input form with better styling
        with st.form("prediction_form"):
            # Numerical inputs
            col_num1, col_num2 = st.columns(2)
            with col_num1:
                metascore = st.slider(
                    "🎪 Metascore (Professional Rating)", 
                    min_value=0, max_value=100, value=75,
                    help="Professional critics' score from 0-100"
                )
            
            with col_num2:
                month = st.selectbox(
                    "📅 Release Month",
                    options=list(range(1, 13)),
                    index=5,
                    format_func=lambda x: {
                        1: "January", 2: "February", 3: "March", 4: "April",
                        5: "May", 6: "June", 7: "July", 8: "August",
                        9: "September", 10: "October", 11: "November", 12: "December"
                    }[x]
                )
            
            # Categorical inputs with search functionality
            col_cat1, col_cat2 = st.columns(2)
            with col_cat1:
                developer = st.selectbox(
                    "👨‍💻 Developer",
                    options=developers,
                    index=0 if developers else None,
                    help="Select the game development studio"
                )
                
                platform = st.selectbox(
                    "🎮 Platform",
                    options=platforms,
                    index=0 if platforms else None,
                    help="Select the gaming platform"
                )
            
            with col_cat2:
                genre = st.selectbox(
                    "🎭 Genre",
                    options=genres,
                    index=0 if genres else None,
                    help="Select the game genre/category"
                )
                
                manufacturer = st.selectbox(
                    "🏭 Manufacturer",
                    options=manufacturers,
                    index=0 if manufacturers else None,
                    help="Select the platform manufacturer"
                )

            # Submit button with custom styling
            submitted = st.form_submit_button(
                "🔮 Predict Score", 
                use_container_width=True,
                type="primary"
            )

            if submitted:
                # Collect features
                features = {
                    'metascore': metascore,
                    'month': month,
                    'developer': developer or "",
                    'platform': platform or "",
                    'genre': genre or "",
                    'manufacturer': manufacturer or ""
                }
                
                # Validate inputs
                errors = validate_inputs(features)
                
                if errors:
                    for error in errors:
                        st.error(f"❌ {error}")
                else:
                    # Make prediction
                    with st.spinner("🤖 Analyzing game data..."):
                        prediction, error = predict_game_score(features, model, df_enhanced)
                    
                    if error:
                        st.error(f"❌ {error}")
                    else:
                        # Show prediction result in the second column
                        with col2:
                            st.markdown(f"""
                            <div class="prediction-card">
                                <h2>🎯 Prediction Result</h2>
                                <h1 style="font-size: 3rem; margin: 1rem 0;">{prediction:.2f}</h1>
                                <p>Predicted User Score (out of 10)</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Score interpretation
                            if prediction is not None:
                                if prediction >= 8.5:
                                    st.success("🌟 Exceptional! This game is predicted to be loved by users!")
                                elif prediction >= 7.0:
                                    st.info("👍 Good! Users will likely enjoy this game.")
                                elif prediction >= 5.0:
                                    st.warning("⚠️ Mixed reviews expected. Some will like it, others won't.")
                                else:
                                    st.error("👎 Poor reception predicted. Users might not enjoy this game.")
                                
                                # Show gauge chart if plotly is available
                                try:
                                    fig = create_score_gauge(prediction)
                                    if fig is not None:
                                        st.plotly_chart(fig, use_container_width=True)
                                    else:
                                        st.progress(prediction / 10)
                                except:
                                    st.progress(prediction / 10)
                                    
                                # Additional metrics display
                                col_metric1, col_metric2 = st.columns(2)
                                with col_metric1:
                                    score_percentage = (prediction / 10) * 100
                                    st.metric(
                                        "📊 Score Percentage", 
                                        f"{score_percentage:.1f}%",
                                        delta=f"{score_percentage - 70:.1f}%" if score_percentage > 70 else None
                                    )
                                
                                with col_metric2:
                                    if prediction >= 8.5:
                                        category = "🌟 Exceptional"
                                    elif prediction >= 7.0:
                                        category = "👍 Good"
                                    elif prediction >= 5.0:
                                        category = "⚠️ Mixed"
                                    else:
                                        category = "👎 Poor"
                                    
                                    st.metric("🎯 Category", category)

    # Show example predictions
    st.markdown("---")
    st.subheader("🎲 Try These Examples")
    
    examples = [
        {
            "name": "Nintendo Switch Zelda Game",
            "features": {"metascore": 95, "month": 11, "developer": "Nintendo", 
                        "platform": "Nintendo Switch", "genre": "Open-World Action", "manufacturer": "Nintendo"}
        },
        {
            "name": "PlayStation Action Game",
            "features": {"metascore": 85, "month": 6, "developer": "Sony", 
                        "platform": "PlayStation 5", "genre": "Action", "manufacturer": "Sony"}
        },
        {
            "name": "PC Indie Game",
            "features": {"metascore": 70, "month": 3, "developer": "Independent", 
                        "platform": "PC", "genre": "Indie", "manufacturer": "PC"}
        }
    ]
    
    cols = st.columns(len(examples))
    for i, example in enumerate(examples):
        with cols[i]:
            if st.button(f"🎮 {example['name']}", key=f"example_{i}"):
                st.session_state.example_features = example['features']
                st.rerun()

def test():
    """Test function for development"""
    sample_game = {
        'metascore': 85,
        'month': 11,
        'developer': "Nintendo",
        'platform': "Nintendo Switch",
        'genre': "Action",
        'manufacturer': "Nintendo",
    }
    
    try:
        model = load_model()
        df_enhanced = load_enhanced_dataset()
        
        if model and df_enhanced is not None:
            prediction, error = predict_game_score(sample_game, model, df_enhanced)
            if error:
                print(f"Test Error: {error}")
            else:
                print(f"Test Prediction: {prediction:.2f}")
        else:
            print("Could not load model or dataset for testing")
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == '__main__':
    main()