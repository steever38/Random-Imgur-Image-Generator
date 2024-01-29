import concurrent.futures
from requests import Session
import random
import requests
import os
import datetime

# Ascii art title
print("""
  _____     _             _____                              _____                    _____            
 |  __ \   | |           |_   _|                            |_   _|                  / ____|           
 | |__) |__| |_ __ ___     | |  _ __ ___   __ _ _   _ _ __    | |  _ __ ___   __ _  | |  __  ___ _ __  
 |  _  // _` | '_ ` _ \    | | | '_ ` _ \ / _` | | | | '__|   | | | '_ ` _ \ / _` | | | |_ |/ _ \ '_ \ 
 | | \ \ (_| | | | | | |  _| |_| | | | | | (_| | |_| | |     _| |_| | | | | | (_| | | |__| |  __/ | | |
 |_|  \_\__,_|_| |_| |_| |_____|_| |_| |_|\__, |\__,_|_|    |_____|_| |_| |_|\__, |  \_____|\___|_| |_|
                                           __/ |                              __/ |                    
                                          |___/                              |___/                     
""")

# Check if the 'images' directory exists, if not, create it
if not os.path.exists("images"):
    os.mkdir("images")

print("Warning: potentially NSFW content may be present \n")
# Ask the user how many images they want to download
image_number = int(input("How many images do you want to download: "))

# Ask the user if they want to send images to a Discord webhook
webhook = input("Send images to a Discord webhook? [yes/no]: ")
while webhook == 'yes':
    if webhook == 'yes':
        # Get the URL of the Discord webhook from the user
        webhook_url = input("URL of your Discord webhook: ")
        # Send a HEAD request to the webhook URL to check if it's valid
        response = requests.head(webhook_url)
        if response.status_code != 200:
            print(f"Webhook error, error code: {response.status_code}")
            # Ask the user if they want to retry entering the webhook URL
            webhook = input("Do you want to retry the webhook URL? yes/no: ")
        else:
            break

# Define the characters that can be in an Imgur image URL
url_characters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
                  'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
                  '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# Usage of sessions for HTTP requests
session = Session()

# Using multiprocessing to download images in parallel
with concurrent.futures.ThreadPoolExecutor() as executor:
    downloaded_images = 0

    # Function to generate random url
    def generate_random_url():
        id = ''.join(random.choices(url_characters, k=5))
        return f'https://i.imgur.com/{id}.jpeg'

    # Function to download image
    def download_image(image_url):
        response = session.head(image_url)
        content_length = int(response.headers.get("content-length", 0))

        if content_length > 0 and content_length != 503:
            response = session.get(image_url)
            if response.status_code == 200:
                id = image_url.split("/")[-1].split(".")[0]
                with open(os.path.join('images', f'{id}t.jpeg'), 'wb') as file:
                    file.write(response.content)
                if webhook=="yes":
                    requests.post(webhook_url, json={"content": image_url})
                print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] Image {id} downloaded successfully.')
                return image_url

    # Using concurrent.futures to download images in parallel
    image_urls = [generate_random_url() for _ in range(image_number)]
    downloaded_images += len(list(executor.map(download_image, image_urls)))

# After all images have been downloaded, print the total number of downloaded images
print(f'Total number of downloaded images: {downloaded_images}')
