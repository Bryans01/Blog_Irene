import os
import requests
import shutil
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def create_prompt(title, adjective):
    """Create a prompt for OpenAI API to generate a short story."""
    prompt = f"Compose a captivating story revolving around the theme of {title}, showcasing {adjective} elements."
    return prompt

def get_blog_from_openai(title, adjective, model_name):
    """Get a story from OpenAI API using the given title."""
    prompt = create_prompt(title, adjective)
    messages = [
        {"role": "system", "content": "You are an AI that writes impressive short stories."},
        {"role": "user", "content": prompt},
    ]

    max_tokens = 8000

    response = openai.ChatCompletion.create(
        model=model_name,
        messages=messages,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.5,
    )

    story = response['choices'][0]['message']['content']
    
    # Generate DALL-E 2 prompt
    image_prompt = f"Generate a prompt for creating an image representing a {adjective} cover related to the story:"
    messages.append({"role": "user", "content": image_prompt})
    
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    dalle2_prompt = response['choices'][0]['message']['content']

    return story, dalle2_prompt

def save_image(image_url, file_name):
    """Download and save an image from the given URL."""
    image_res = requests.get(image_url, stream=True)

    if image_res.status_code == 200:
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(image_res.raw, f)
    else:
        print("Error downloading image!")
    return image_res.status_code, file_name

def get_cover_image(dalle2_prompt, save_path):
    response = openai.Image.create(
        prompt=dalle2_prompt,
        n=1,
        size="1024x1024",
    )
    image_url = response['data'][0]['url']
    status_code, file_name = save_image(image_url, save_path)
    return status_code, file_name
