import csv
import os

def clean_twitter_data(input_file_path, output_csv_path):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            # Read the entire content as one string and split by the delimiter
            content = file.read()
            tweets = content.split('~~~TWEET_DELIMITER~~~')
    except FileNotFoundError:
        print(f"Error: The file '{input_file_path}' does not exist.")
        return
    except Exception as e:
        print(f"Error reading the file: {e}")
        return

    # Clean and store the tweets
    cleaned_tweets = []

    for index, tweet in enumerate(tweets, 1):  # Start numbering tweets from 1
        tweet = tweet.strip()  # Remove leading/trailing whitespace

        # Skip empty tweets
        if not tweet:
            continue

        # Store each tweet with its number
        cleaned_tweets.append({'tweet_number': index, 'tweet': tweet})

    if not cleaned_tweets:
        print("No tweets were found in the input file.")
        return

    # Make sure the directory exists, create it if not
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

    # Write the cleaned tweets to the CSV
    try:
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['tweet_number', 'tweet']  # Include tweet number in the fieldnames
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()  # Write the header
            writer.writerows(cleaned_tweets)  # Write all tweets

        print(f"Data has been written to {output_csv_path}")
    except Exception as e:
        print(f"Error writing to CSV file: {e}")
# Example usage
input_file_path = r'tweets\tweets_2024.txt'  # Path to the input text file
output_csv_path = r'tweets\tweets_2024.csv'  # Path to the output CSV file
clean_twitter_data(input_file_path, output_csv_path)