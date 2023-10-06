# Version: 1.0
# Import necessary libraries
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
 |_|  \_\__,_|_| |_| |_| |_____|_| |_| |_|\__, |\__,_|_|    |_____|_| |_| |_|\__, |  \_____|\___|_| |_|by steever38
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
# Function to generate a random Imgur image URL
def generate_random_url():
    id = ''.join(random.choice(url_characters) for _ in range(5))
    image_url=f'https://i.imgur.com/{id}.jpeg'
    return id, image_url

downloaded_images = 0

# Loop until we've downloaded the desired number of images
while downloaded_images < image_number:
    id, image_url = generate_random_url()
    # Send a HEAD request to get the headers of the image
    response = requests.head(image_url)
    content_length = int(response.headers.get("content-length", 0))
    now = datetime.datetime.now().strftime("%H:%M:%S")

    # Check if the size is not 503 bytes (which means the link is dead)
    if content_length != 503:
        if content_length > 0:
            # Send a GET request to download the image
            response = requests.get(image_url)
            if response.status_code == 200:
                # Save the image to a file
                with open(f'images/{id}t.jpeg', 'wb') as file:
                    file.write(response.content)
                # Print a success message with the current time and image number
                print(f'[{now}] Image {downloaded_images + 1} ({id}) downloaded successfully.')
                # Increment the count of downloaded images
                downloaded_images += 1
                # If the user chose to send images to a Discord webhook, send a POST request to the webhook URL with the image URL
                if webhook == 'yes':
                    response = requests.post(webhook_url, json={'content': image_url})
            else:
                # If the GET request was not successful, print an error message with the image number and response status code
                print(f'Unable to download image {downloaded_images + 1}. Response status: {response.status_code}')

# After all images have been downloaded, print the total number of downloaded images
print(f'Total number of downloaded images: {downloaded_images}')
