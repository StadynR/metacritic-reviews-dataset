import streamlit as st
import pandas as pd
import joblib

MANUFACTURERS = {
    'Nintendo': ['Nintendo 64', 'GameCube', 'Wii', 'Wii U', 'Nintendo Switch', 'Nintendo Switch 2', 'Game Boy Advance', 'DS', '3DS'],
    'Sony': ['PlayStation', 'PlayStation 2', 'PlayStation 3', 'PlayStation 4', 'PlayStation 5', 'PSP', 'PlayStation Vita'],
    'Microsoft': ['Xbox', 'Xbox 360', 'Xbox One', 'Xbox Series X'],
    'Sega': ['Dreamcast'],
    'Apple': ['iOS (iPhone/iPad)'],
    'VR': ['Meta Quest'],
    'PC': ['PC']
}

def map_manufacturers(platform):
    for manufacturer, platforms in MANUFACTURERS.items():
        if platform in platforms:
            return manufacturer
    return 'Other'

def validate_inputs(features):
    """Validate user inputs and return error messages if any"""
    errors = []
    
    if not features['developer'].strip():
        errors.append("Developer name cannot be empty")
    
    if not features['platform'].strip():
        errors.append("Platform cannot be empty")
        
    if not features['genre'].strip():
        errors.append("Genre cannot be empty")
    
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
        df = pd.read_csv('app/metacritic_dataset_features_enhanced.csv')
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
        
        # Create a copy to avoid modifying the original
        processed_data = game_data.copy()
        processed_data["metascore_scaled"] = processed_data["metascore"] / 10
        processed_data["manufacturer"] = map_manufacturers(processed_data["platform"])
        manufacturer = processed_data["manufacturer"]
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
    
def get_valid_example_values(example_features, developers, platforms, genres):
    """Ensure example values exist in the dataset, provide fallbacks if not"""
    validated = {}
    
    # Validate and set metascore
    validated['metascore'] = max(0, min(100, example_features.get('metascore', 75)))
    
    # Validate and set month
    month_val = example_features.get('month', 6)
    validated['month'] = month_val if month_val in range(1, 13) else 6
    
    # Validate developer
    example_dev = example_features.get('developer', '')
    if example_dev and developers and example_dev in developers:
        validated['developer'] = example_dev
    elif developers:
        # Find similar developers or use first available
        similar_devs = [dev for dev in developers if any(word in dev.lower() for word in example_dev.lower().split())]
        validated['developer'] = similar_devs[0] if similar_devs else developers[0]
    else:
        validated['developer'] = ''
    
    # Validate platform
    example_plat = example_features.get('platform', '')
    if example_plat and platforms and example_plat in platforms:
        validated['platform'] = example_plat
    elif platforms:
        similar_plats = [plat for plat in platforms if any(word in plat.lower() for word in example_plat.lower().split())]
        validated['platform'] = similar_plats[0] if similar_plats else platforms[0]
    else:
        validated['platform'] = ''
    
    # Validate genre
    example_genre = example_features.get('genre', '')
    if example_genre and genres and example_genre in genres:
        validated['genre'] = example_genre
    elif genres:
        similar_genres = [genre for genre in genres if any(word in genre.lower() for word in example_genre.lower().split())]
        validated['genre'] = similar_genres[0] if similar_genres else genres[0]
    else:
        validated['genre'] = ''
    
    return validated

def get_popular_options(df):
    """Get popular options for dropdowns"""
    if df is None:
        return [], [], []
    try:
        developers = sorted(df['developer'].unique())
        platforms = sorted(df['platform'].unique())
        genres = sorted(df['genre'].unique())
        
        return developers, platforms, genres
    except Exception:
        return [], [], []