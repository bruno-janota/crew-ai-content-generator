import os
import re
from dotenv import load_dotenv, find_dotenv
import logging
import datetime
import textwrap
import yaml

def load_env():
    _ = load_dotenv(find_dotenv())


def load_yaml_config(file_path):
    """Load YAML configurations from a given file."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)
    

def get_openai_api_key():
    load_env()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    return openai_api_key


def sanitize_filename(subject):
    """Sanitize subject string to create a valid filename."""
    filename = subject.lower()
    filename = re.sub(r'[^a-z0-9]+', '-', filename)  # Replace invalid characters with hyphens
    filename = filename.strip('-')  
    return filename[:50]  # Limit filename length to avoid OS issues


def display_social_content(result):
    """Prints the generated social media posts."""
    logging.info("\n📢 Generated Social Media Posts:\n" + "-"*50)

    for post in result.social_media_posts:
        print(f"🔹 {post.platform.upper()}:")
        print(textwrap.fill(post.content, width=80))
        print("-" * 50)


def save_content(result, subject):
    """Save generated content to a timestamped folder with a clean filename."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    sanitized_subject = sanitize_filename(subject)

    output_dir = os.path.join("generated_content", f"{timestamp}_{sanitized_subject}")
    os.makedirs(output_dir, exist_ok=True)

    blog_filename = f"{sanitized_subject}.md"
    social_media_filename = "social_media_posts.txt"

    # Save blog post
    with open(os.path.join(output_dir, blog_filename), "w", encoding="utf-8") as f:
        f.write(result.article)

    # Save social media posts
    with open(os.path.join(output_dir, social_media_filename), "w", encoding="utf-8") as f:
        for post in result.social_media_posts:
            f.write(f"{post.platform}: {post.content}\n\n")

    logging.info(f"📂 Content saved in `{output_dir}/`")