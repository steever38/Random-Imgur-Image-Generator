import concurrent.futures
from requests import Session
import random
import requests
import os
import datetime
from pystyle import Colors, Colorate, Write
# Ascii art title
title = """
  _____     _             _____                              _____                    _____            
 |  __ \\   | |           |_   _|                            |_   _|                  / ____|           
 | |__) |__| |_ __ ___     | |  _ __ ___   __ _ _   _ _ __    | |  _ __ ___   __ _  | |  __  ___ _ __  
 |  _  // _` | '_ ` _ \\    | | | '_ ` _ \\ / _` | | | | '__|   | | | '_ ` _ \\ / _` | | | |_ |/ _ \\ '_ \\
 | | \\ \\ (_| | | | | | |  _| |_| | | | | | (_| | |_| | |     _| |_| | | | | | (_| | | |__| |  __/ | | |
 |_|  \\_\\__,_|_| |_| |_| |_____|_| |_| |_|\\__, |\\__,_|_|    |_____|_| |_| |_|\\__, |  \\_____|\\___|_| |_|
                                           __/ |                              __/ |                    
                                          |___/                              |___/                     
"""
print(Colorate.Horizontal(Colors.green_to_yellow, title))
os.system("title " + "Random Imgur Image Generator")
# Check if the 'images' directory exists, if not, create it
if not os.path.exists("images"):
    os.mkdir("images")
print()
Write.Print("program made by steever38 (github.com/steever38) \n", Colors.red_to_yellow, interval=0.02)
print()
Write.Print("Warning: potentially NSFW content may be present \n", Colors.red, interval=0.008)
# Ask the user how many images they want to download
image_number = int(Write.Input("How many images do you want to download -> ", Colors.reset, interval=0.008))

# Ask the user if they want to send images to a Discord webhook
webhook = Write.Input("Send images to a Discord webhook, [yes/no] -> ", Colors.reset, interval=0.008)
while webhook == 'yes':
    if webhook == 'yes':
        # Get the URL of the Discord webhook from the user
        webhook_url = Write.Input("URL of your Discord webhook -> ", Colors.reset, interval=0.008)
        # Send a HEAD request to the webhook URL to check if it's valid
        response = requests.head(webhook_url)
        if response.status_code != 200:
            Write.Print(f"Webhook error, error code: {response.status_code}", Colors.red, interval=0.001)
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
        global downloaded_images_count
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
                downloaded_images_count += 1
                print(f'{downloaded_images_count} - [{datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]}] Image {id} downloaded successfully.')
                return image_url
        else: 
            new_url = generate_random_url()
            download_image(new_url)


    # Using concurrent.futures to download images in parallel
    downloaded_images_count = 0
    image_urls = [generate_random_url() for _ in range(image_number)]
    Write.Print(f"\n{image_number} random url generated", Colors.green, interval=0.02)
    print("\nReady to download images")
    # Start timer
    start_time = datetime.datetime.now()
    downloaded_images += len(list(executor.map(download_image, image_urls)))
    # End timer
    end_time = datetime.datetime.now()
    duration = end_time - start_time

seconds= duration.seconds
microseconds = duration.microseconds
ok = float(str(seconds)+"."+str(microseconds))
average_download_time = ok / downloaded_images
# After all images have been downloaded, print the total number of downloaded images, the total time to download and the average time per image
Write.Print(f'Total number of downloaded images: {downloaded_images}', Colors.green, interval=0.001)
Write.Print(f'\nTotal time to download: {duration}', Colors.yellow, interval=0.001)
Write.Print(f'\nAverage download time per image: {average_download_time:.4f} seconds', Colors.orange, interval=0.001)
