import pytumblr
import json
import random
import os

#authenticate with Tumblr API and return pytumblr object
def authenticate(consumer_key, consumer_secret, oauth_token, oauth_secret):
    client = pytumblr.TumblrRestClient(
        consumer_key,
        consumer_secret,
        oauth_token,
        oauth_secret,
    )
    return client

#post photo to tumblr
def post_photo_to_tumblr(blogname, state, tags, caption, data, client):
    client.create_photo(blogname, state=state, tags=tags, caption=caption, data=data)
    
#return # random tags from an array
def pick_random_tag(tags, num):
    random_items = random.sample(tags, 3)
    #print(random_items)
    return random_items
    
#return an item from array 1 that is not in array 2
def pick_unique_item_helper(items, used_items, text):
    for item in items:
        if item not in used_items:
            return item
    
    message = f"All {text} have been used."
    print(message)
    
    return random.choice(items)
    
#return a caption that is not in the used caption list, if all captions used, just pick a random caption
def pick_unused_caption(captions, used_captions):
    return pick_unique_item_helper(captions, used_captions, "captions")
    
#return an image that is not in the used image list, if all images used, just pick a random image 
def pick_unused_image(image_folder, used_images):
    # Get the list of files in the folder
    files = os.listdir(image_folder)

    # Filter the list to get only the image files
    image_files = [f for f in files if f.endswith(".jpg") or f.endswith(".png")]

    #get an image name that hasn't been used previously
    return pick_unique_item_helper(image_files, used_images, "images")
 
def main():
    # Set these variables
    tumblr_auth_json = '.\\tumblr_auth.json'
    metadata_json = '.\\metadata.json'
    photo_folder = '.\\images'
    blogname = '' #example: xxx@tumblr.com
    state = 'queue' #posting to tumblr post queue, as opposed to live posts
    post_number = 3 #how many posts to upload at a time

    # Read the configuration file and extract varibables
    with open(tumblr_auth_json, 'r') as f:
        config = json.load(f)
    consumer_key = config['consumer_key']
    consumer_secret = config['consumer_secret']
    oauth_token = config['oauth_token']
    oauth_secret = config['oauth_secret']

    #authenticate with tumblr API
    client = authenticate(consumer_key, consumer_secret, oauth_token, oauth_secret)
    #print(client.info()) #test to see if authentication successful
    
    #read the metadata file and extract variables
    with open(metadata_json, 'r') as f:
        metadata = json.load(f)
        
    #post this many posts       
    for i in range(post_number):
        #pick randome tags  
        tags = pick_random_tag(metadata['tags'], 3)
        
        # Retrieve an unused caption
        caption = pick_unused_caption(metadata['funny_captions'], metadata['used_captions'])
        # Update the "used_captions" array    
        metadata["used_captions"].extend([caption])
        
        #retrieve an unused image
        image = pick_unused_image(photo_folder, metadata["used_images"])
        # Update the "used_captions" array 
        metadata["used_images"].extend([image])
        # Construct full path
        data = f"{photo_folder}\\{image}"
        
        # Serialize the updated data and write it back to the file
        with open(metadata_json, "w") as f:
            json.dump(metadata, f, indent=2)
        
        #post a photo to tumlbr API
        post_photo_to_tumblr(blogname, state, tags, caption, data, client)

if __name__ == "__main__":
    main()
