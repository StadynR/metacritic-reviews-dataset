import streamlit as st
import joblib
import numpy as np
import pandas as pd

def predict_game_score(game_data: dict, model, features_df):
    developer = game_data.get("developer", None)
    platform = game_data.get("platform", None)
    month = game_data.get("month", None)
    genre = game_data.get("genre", None)
    manufacturer = game_data.get("manufacturer", None)
    game_data["metascore_scaled"] = game_data["metascore"] / 10
    game_data.pop("metascore", None)
    game_data["developer_avg_score"] = features_df[features_df["developer"] == developer]["developer_avg_score"].iloc[0]
    game_data["platform_age"] = features_df[features_df["platform"] == platform]["platform_age"].iloc[0]
    game_data["is_holiday_release"] = 1 if month in [11, 12] else 0
    genre_counts = features_df['genre'].value_counts()
    game_data["genre_popularity"] = genre_counts.get(genre, 0)
    game_data["platform_genre_encoded"] = features_df[features_df["platform_genre"] == f"{platform}_{genre}"]["platform_genre_encoded"].iloc[0]
    game_data["genre_encoded"] = features_df[features_df["genre"] == genre]["genre_encoded"].iloc[0]
    game_data["platform_encoded"] = features_df[features_df["platform"] == platform]["platform_encoded"].iloc[0]
    game_data["manufacturer_encoded"] = features_df[features_df["manufacturer"] == manufacturer]["manufacturer_encoded"].iloc[0]

    game_data_df = pd.DataFrame([game_data])
    predict_df = game_data_df[model.feature_names_in_]
    predicted_score = model.predict(predict_df)[0]

    return predicted_score

# Define feature names and descriptions
# When you use this - replace these features with the cols from df.columns 
# Do not include your target!
numerical_features = ['metascore', 'month']
categorical_features = ['developer', 'platform', 'genre', 'manufacturer']
feature_names = { 'metascore': 'Metascore',  'month': 'Month',  'developer': 'Developer', 'platform': 'Platform', 
                 'genre': 'Genre', 'manufacturer': 'Manufacturer' }

def main():
    st.title('Metacritic Game Score Prediction App')
    st.write("Enter the values for the features to get a prediction.")

    # Load the enhanced dataset for feature scaling
    df_enhanced = pd.read_csv('app\metacritic_dataset_features_enhanced.csv')

    # Define input fields for user to enter feature values with proper labels
    features = {}
    for value, label in feature_names.items():
        if value in categorical_features:
            feature_value = st.text_input(f'{label}', '')
        else:
            feature_value = st.number_input(f'{label}', min_value=0.0, value=0.0)
        features[value] = feature_value

    # Button to make a prediction
    if st.button('Predict'):
        try:
            model = joblib.load('app\metacritic_model.pkl')
            prediction = predict_game_score(features, model, df_enhanced)

            # Display the result
            st.write(f"Prediction: {prediction:.2f}")
        except Exception as e:
            st.error(f"Error in prediction: {e}")

def test():
    # Test the app with a sample input
    sample_game = {
        'metascore': 85,
        'month': 11,
        'developer': "Nintendo",
        'platform': "Nintendo Switch",
        'genre': "Action",
        'manufacturer': "Nintendo",
    }
    model = joblib.load('app\metacritic_model.pkl')
    df_enhanced = pd.read_csv('app\metacritic_dataset_features_enhanced.csv')
    prediction = predict_game_score(sample_game, model, df_enhanced)
    print(f"Test Prediction: {prediction:.2f}")

if __name__ == '__main__':
    main()