import asyncio
import random
import csv
from twikit import Client

async def main():
    query = '''"election" lang:en -filter:replies'''
    seen_tweet_ids = set()  # To track tweet IDs and avoid duplicates

    # Initialize client with custom user agent
    client = Client(
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15'
    )
    
    #Cookies are gathered from the browser and saved in a file and then converted into a usable format using the json_to_cookie script
    client.load_cookies('cookies.json')

    # Open CSV file to write tweets with headers
    with open('tweets_election.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'text', 'user', 'created_at']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  # Write header to CSV

        # Continuously fetch new tweets
        while True:
            tweets = await client.search_tweet(query, 'latest')
            
            for tweet in tweets:
                if tweet.id in seen_tweet_ids:
                    continue  # Skip if we have already processed this tweet

                # Write tweet data to CSV
                writer.writerow({
                    'id': tweet.id,
                    'text': tweet.text,
                    'user': tweet.user.screen_name,
                    'created_at': tweet.created_at
                })
                seen_tweet_ids.add(tweet.id)  # Track this tweet ID
                print(tweet.id, tweet.text, tweet.user.screen_name, tweet.created_at)
                
                # Wait for a random time between 5 and 25 seconds
                await asyncio.sleep(random.randint(2, 5))

            # Wait before fetching new tweets to avoid rate limiting
            await asyncio.sleep(30)  # 30 second delay between each search for new tweets

# Run the main function
asyncio.run(main())
