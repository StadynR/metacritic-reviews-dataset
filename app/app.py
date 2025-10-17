import streamlit as st
from styles import inject_custom_css, create_animated_metric, create_feature_explanation
from utils import validate_inputs, load_model, load_enhanced_dataset, predict_game_score, get_popular_options, get_valid_example_values
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
import os

# Try to import plotly, but don't fail if not available
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# Configure page settings
st.set_page_config(
    page_title="Metacritic Game Score Predictor",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def create_score_gauge(score):
    """Create a beautiful gauge chart for the prediction score"""
    if not PLOTLY_AVAILABLE:
        return None
        
    fig = go.Figure(go.Indicator( # type: ignore
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
            ]
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white", 'family': "Arial"},
        height=400
    )
    
    return fig

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
    #     background: linear-gradient(90deg, #495057 0%, #6c757d 100%);
    #     padding: 2rem;
    #     border-radius: 15px;
    #     text-align: center;
    #     color: white;
    #     margin-bottom: 2rem;
    #     box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    # }
    # .prediction-card {
    #     background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
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
    
    # Check if data/model loading failed
    data_loaded = df_enhanced is not None and model is not None

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
        """)
        
        # Show dataset insights only if data is loaded
        if data_loaded:
            show_data_insights(df_enhanced)
        else:
            st.warning("⚠️ Dataset not loaded. Using default options.")
        
        st.markdown("---")
        
        # Add feature explanation if custom styles are available
        try:
            create_feature_explanation()
        except:
            pass

        st.markdown("🔗 **Data Source**: Metacritic Reviews Dataset")
        st.markdown("🤖 **Model**: Random Forest Regressor")

    # Get options for dropdowns - with fallbacks
    if data_loaded:
        developers, platforms, genres = get_popular_options(df_enhanced)
    else:
        # Provide default options when data isn't loaded
        developers = ["Nintendo", "Sony", "Microsoft", "EA", "Ubisoft", "Activision", "Square Enix", "Capcom"]
        platforms = ["PC", "PlayStation 5", "Xbox Series X", "Nintendo Switch", "PlayStation 4", "Xbox One"]
        genres = ["Action", "Adventure", "RPG", "Strategy", "Sports", "Racing", "Simulation", "Puzzle"]

    # Use full width layout
    st.subheader("🎯 Game Information")
    
    # Show data loading status
    if not data_loaded:
        st.warning("⚠️ **Limited Mode**: Using default options. Some features may not work correctly until data is loaded.")
    
    # Show message if example was loaded
    if st.session_state.get('example_features'):
        st.success("🎮 Example values loaded! Modify as needed and click Predict.")
    
    # Input form with better styling - full width
        with st.form("prediction_form"):
            # Check if example features are available in session state
            raw_example_features = st.session_state.get('example_features', {})
            
            # Validate example features against available options
            if raw_example_features:
                example_features = get_valid_example_values(raw_example_features, developers, platforms, genres)
            else:
                example_features = {}
            
            # Create horizontal layout with more columns to use full width
            col1, col2, col3, col4, col5 = st.columns([1.2, 1, 1, 1, 1])
            
            with col1:
                metascore = st.slider(
                    "🎪 Metascore (Professional Rating)", 
                    min_value=0, max_value=100, 
                    value=example_features.get('metascore', 75),
                    help="Professional critics' score from 0-100"
                )
            
            with col2:
                # Get month value from examples or default
                month_value = example_features.get('month', 6)
                month_index = month_value - 1 if month_value in range(1, 13) else 5
                
                month = st.selectbox(
                    "📅 Release Month",
                    options=list(range(1, 13)),
                    index=month_index,
                    format_func=lambda x: {
                        1: "January", 2: "February", 3: "March", 4: "April",
                        5: "May", 6: "June", 7: "July", 8: "August",
                        9: "September", 10: "October", 11: "November", 12: "December"
                    }[x]
                )
            
            with col3:
                # Get developer index from validated examples
                example_developer = example_features.get('developer', '')
                developer_index = 0
                if example_developer and developers and example_developer in developers:
                    developer_index = developers.index(example_developer)
                
                developer = st.selectbox(
                    "👨‍💻 Developer",
                    options=developers,
                    index=developer_index if developers else None,
                    help="Select the game development studio"
                )
            
            with col4:
                # Get platform index from validated examples
                example_platform = example_features.get('platform', '')
                platform_index = 0
                if example_platform and platforms and example_platform in platforms:
                    platform_index = platforms.index(example_platform)
                
                platform = st.selectbox(
                    "🎮 Platform",
                    options=platforms,
                    index=platform_index if platforms else None,
                    help="Select the gaming platform"
                )
            
            with col5:
                # Get genre index from validated examples
                example_genre = example_features.get('genre', '')
                genre_index = 0
                if example_genre and genres and example_genre in genres:
                    genre_index = genres.index(example_genre)
                
                genre = st.selectbox(
                    "🎭 Genre",
                    options=genres,
                    index=genre_index if genres else None,
                    help="Select the game genre/category"
                )
            
            # Submit button with custom styling - full width below all inputs
            submitted = st.form_submit_button(
                "🔮 Predict Score", 
                use_container_width=True,
                type="primary"
            )
                
            # Clear example features after form submission
            if submitted and 'example_features' in st.session_state:
                del st.session_state.example_features

            if submitted:
                # Collect features
                features = {
                    'metascore': metascore,
                    'month': month,
                    'developer': developer or "",
                    'platform': platform or "",
                    'genre': genre or "",
                }
                
                # Check if data and model are available
                if not data_loaded:
                    st.error("❌ **Cannot make predictions**: Dataset and/or model failed to load. Please check the app files and try refreshing the page.")
                    st.info("💡 **Tip**: Ensure 'metacritic_dataset_features_enhanced.csv' and 'metacritic_model.pkl' are in the app folder.")
                    return
                
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
                        # Show prediction result - reorganized for better space usage
                        st.markdown("---")
                        st.subheader("🎯 Prediction Results")
                        
                        # Create three columns for horizontal layout - better proportions
                        col_gauge, col_metrics, col_category = st.columns([1, 1, 1])
                        
                        # Ensure prediction is valid before proceeding
                        if prediction is not None and isinstance(prediction, (int, float)):
                            with col_gauge:
                                # Show gauge chart if plotly is available
                                if PLOTLY_AVAILABLE:
                                    try:
                                        fig = create_score_gauge(prediction)
                                        if fig is not None:
                                            st.plotly_chart(fig, use_container_width=True)
                                        else:
                                            # Fallback with larger score display
                                            st.markdown(f"""
                                            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #6c757d 0%, #495057 100%); border-radius: 15px; color: white;">
                                                <h3>Predicted Score</h3>
                                                <h1 style="font-size: 4rem; margin: 1rem 0;">{prediction:.2f}</h1>
                                                <p>out of 10</p>
                                            </div>
                                            """, unsafe_allow_html=True)
                                            st.progress(prediction / 10)
                                    except:
                                        # Fallback with larger score display
                                        st.markdown(f"""
                                        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #6c757d 0%, #495057 100%); border-radius: 15px; color: white;">
                                            <h3>Predicted Score</h3>
                                            <h1 style="font-size: 4rem; margin: 1rem 0;">{prediction:.2f}</h1>
                                            <p>out of 10</p>
                                        </div>
                                        """, unsafe_allow_html=True)
                                        st.progress(prediction / 10)
                                else:
                                    # Fallback with larger score display
                                    st.markdown(f"""
                                    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #6c757d 0%, #495057 100%); border-radius: 15px; color: white;">
                                        <h3>Predicted Score</h3>
                                        <h1 style="font-size: 4rem; margin: 1rem 0;">{prediction:.2f}</h1>
                                        <p>out of 10</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    st.progress(prediction / 10)
                            
                            with col_metrics:
                                # Larger score percentage metric
                                score_percentage = (prediction / 10) * 100
                                st.markdown(f"""
                                <div style="text-align: center; padding: 2rem; background: white; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); border-left: 6px solid #6c757d;">
                                    <h3 style="color: #495057; margin-bottom: 1rem;">📊 Score Percentage</h3>
                                    <h1 style="color: #6c757d; font-size: 3.5rem; margin: 1rem 0;">{score_percentage:.1f}%</h1>
                                    <p style="color: #666; font-size: 1.1rem;">
                                        {"+" if score_percentage > 70 else ""}{score_percentage - 70:.1f}% vs Average
                                    </p>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with col_category:
                                # Larger category display
                                if prediction >= 8.5:
                                    category = "🌟 Exceptional"
                                    category_color = "#28a745"
                                    category_bg = "#d4edda"
                                elif prediction >= 7.0:
                                    category = "👍 Good"
                                    category_color = "#17a2b8"
                                    category_bg = "#d1ecf1"
                                elif prediction >= 5.0:
                                    category = "⚠️ Mixed"
                                    category_color = "#ffc107"
                                    category_bg = "#fff3cd"
                                else:
                                    category = "👎 Poor"
                                    category_color = "#dc3545"
                                    category_bg = "#f8d7da"
                                
                                st.markdown(f"""
                                <div style="text-align: center; padding: 2rem; background: {category_bg}; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); border-left: 6px solid {category_color};">
                                    <h3 style="color: #495057; margin-bottom: 1rem;">🎯 Category</h3>
                                    <h2 style="color: {category_color}; font-size: 2.5rem; margin: 1rem 0;">{category}</h2>
                                    <p style="color: #666; font-size: 1.1rem;">Quality Rating</p>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            # Score interpretation below in a single row
                            if prediction >= 8.5:
                                st.success("🌟 **Exceptional!** This game is predicted to be loved by users!")
                            elif prediction >= 7.0:
                                st.info("👍 **Good!** Users will likely enjoy this game.")
                            elif prediction >= 5.0:
                                st.warning("⚠️ **Mixed reviews expected.** Some will like it, others won't.")
                            else:
                                st.error("👎 **Poor reception predicted.** Users might not enjoy this game.")
                        else:
                            st.error("❌ Invalid prediction result. Please try again.")

    # Show example predictions
    st.markdown("---")
    st.subheader("🎲 Try These Examples")
    
    examples = [
        {
            "name": "Nintendo Switch Zelda Game",
            "features": {"metascore": 95, "month": 11, "developer": "Nintendo", 
                        "platform": "Nintendo Switch", "genre": "Open-World Action"}
        },
        {
            "name": "PlayStation Action Game", 
            "features": {"metascore": 85, "month": 6, "developer": "Sony", 
                        "platform": "PlayStation 5", "genre": "Action"}
        },
        {
            "name": "PC Strategy Game",
            "features": {"metascore": 70, "month": 3, "developer": "Paradox Interactive", 
                        "platform": "PC", "genre": "Strategy"}
        }
    ]
    
    cols = st.columns(len(examples))
    for i, example in enumerate(examples):
        with cols[i]:
            if st.button(f"🎮 {example['name']}", key=f"example_{i}"):
                # Set the example features in session state
                st.session_state.example_features = example['features']
                # Clear after setting to avoid persistence issues
                st.rerun()

def test():
    """Test function for development"""
    sample_game = {
        'metascore': 85,
        'month': 11,
        'developer': "Nintendo",
        'platform': "Nintendo Switch",
        'genre': "Action"
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