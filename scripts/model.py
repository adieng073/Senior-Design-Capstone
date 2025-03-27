import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
import numpy as np
import os

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Load the model and tokenizer
model_name = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Function to predict sentiment
def predict_sentiment(texts):
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    return predictions.numpy()

# Process predictions to labels
def get_sentiment_labels(predictions):
    labels = ['negative', 'neutral', 'positive']
    sentiment_scores = np.argmax(predictions, axis=1)
    return [labels[i] for i in sentiment_scores], predictions

# Load data (assuming CSV files with a column 'tweet')
def load_data(file_path):
    df = pd.read_csv(file_path)
    if 'tweet' not in df.columns:
        print(f"Error: The column 'tweet' is missing in {file_path}.")
        return []
    return df['tweet'].dropna().tolist()

# Save results to CSV
def save_results_to_csv(year, tweets, scores, labels, output_dir='post_model'):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f'sentiment_results_{year}.csv')
    df = pd.DataFrame({
        'tweet': tweets,
        'embedding_negative': scores[:, 0],
        'embedding_neutral': scores[:, 1],
        'embedding_positive': scores[:, 2],
        'sentiment': labels
    })
    df.to_csv(output_path, index=False)
    print(f"Results saved to {output_path}")

def main():
    # Load the data for 2020 and 2024
    bios_2020 = load_data(r'tweets\tweets_2020.csv')
    bios_2024 = load_data(r'tweets\tweets_2024.csv')

    if not bios_2020 or not bios_2024:
        print("Error: One of the input files is empty or not correctly loaded.")
        return

    # Perform sentiment analysis for both years
    predictions_2020 = predict_sentiment(bios_2020)
    predictions_2024 = predict_sentiment(bios_2024)

    # Get sentiment labels and scores for both years
    labels_2020, scores_2020 = get_sentiment_labels(predictions_2020)
    labels_2024, scores_2024 = get_sentiment_labels(predictions_2024)

    # Save the results to CSV for both 2020 and 2024
    save_results_to_csv(2020, bios_2020, scores_2020, labels_2020)
    save_results_to_csv(2024, bios_2024, scores_2024, labels_2024)

if __name__ == "__main__":
    main()
