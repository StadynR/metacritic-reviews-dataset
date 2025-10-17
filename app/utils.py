import streamlit as st
import pandas as pd
import joblib

def validate_inputs(features):
    """Validate user inputs and return error messages if any"""
    errors = []
    
    if not features['developer'].strip():
        errors.append("Developer name cannot be empty")
    
    if not features['platform'].strip():
        errors.append("Platform cannot be empty")
        
    if not features['genre'].strip():
        errors.append("Genre cannot be empty")
        
    if not features['manufacturer'].strip():
        errors.append("Manufacturer cannot be empty")
    
    if features['metascore'] < 0 or features['metascore'] > 100:
        errors.append("Metascore must be between 0 and 100")
    
    if features['month'] < 1 or features['month'] > 12:
        errors.append("Month must be between 1 and 12")
    
    return errors

def load_model():
    """Load the pre-trained model"""
    try:
        model = joblib.load('app/metacritic_model.pkl')
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None
    
def load_enhanced_dataset():
    """Load the enhanced dataset with precomputed features"""
    try:
        df = pd.read_csv('app/enhanced_metacritic_dataset.csv')
        return df
    except Exception as e:
        st.error(f"Error loading dataset: {str(e)}")
        return None
    
def predict_game_score(game_data: dict, model, features_df):
    try:
        developer = game_data.get("developer", "").strip()
        platform = game_data.get("platform", "").strip()
        month = game_data.get("month", 1)
        genre = game_data.get("genre", "").strip()
        manufacturer = game_data.get("manufacturer", "").strip()
        
        # Create a copy to avoid modifying the original
        processed_data = game_data.copy()
        processed_data["metascore_scaled"] = processed_data["metascore"] / 10
        processed_data.pop("metascore", None)
        
        # Calculate features with fallback values
        developer_scores = features_df[features_df["developer"] == developer]["developer_avg_score"]
        processed_data["developer_avg_score"] = developer_scores.mean() if not developer_scores.empty else features_df["developer_avg_score"].mean()
        
        platform_ages = features_df[features_df["platform"] == platform]["platform_age"]
        processed_data["platform_age"] = platform_ages.mean() if not platform_ages.empty else features_df["platform_age"].mean()
        
        processed_data["is_holiday_release"] = 1 if month in [11, 12] else 0
        
        genre_counts = features_df['genre'].value_counts()
        processed_data["genre_popularity"] = genre_counts.get(genre, genre_counts.mean())
        
        platform_genre_key = f"{platform}_{genre}"
        platform_genre_encoded = features_df[features_df["platform_genre"] == platform_genre_key]["platform_genre_encoded"]
        processed_data["platform_genre_encoded"] = platform_genre_encoded.mean() if not platform_genre_encoded.empty else features_df["platform_genre_encoded"].mean()
        
        genre_encoded = features_df[features_df["genre"] == genre]["genre_encoded"]
        processed_data["genre_encoded"] = genre_encoded.mean() if not genre_encoded.empty else features_df["genre_encoded"].mean()
        
        platform_encoded = features_df[features_df["platform"] == platform]["platform_encoded"]
        processed_data["platform_encoded"] = platform_encoded.mean() if not platform_encoded.empty else features_df["platform_encoded"].mean()
        
        manufacturer_encoded = features_df[features_df["manufacturer"] == manufacturer]["manufacturer_encoded"]
        processed_data["manufacturer_encoded"] = manufacturer_encoded.mean() if not manufacturer_encoded.empty else features_df["manufacturer_encoded"].mean()

        game_data_df = pd.DataFrame([processed_data])
        predict_df = game_data_df[model.feature_names_in_]
        predicted_score = model.predict(predict_df)[0]

        return predicted_score, None
    
    except Exception as e:
        return None, f"Prediction error: {str(e)}"