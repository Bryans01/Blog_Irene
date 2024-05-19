from pathlib import Path
import os
import blog_utils
import openai_utils
from datetime import datetime

def main():
    PATH_TO_BLOG_REPO = Path(r'C:\Stephen\Coding\Blog_3\Bryans01.github.io\.git')
    PATH_TO_BLOG = PATH_TO_BLOG_REPO.parent
    PATH_TO_CONTENT = os.path.join(PATH_TO_BLOG, "content")
    Path(PATH_TO_CONTENT).mkdir(exist_ok=True, parents=True)

    title = "Space"
    adjective = "Scary"
    story_idea_by = "Irene Bryan"
    model_name = "gpt-4"  

    blog_content, dalle2_prompt = openai_utils.get_blog_from_openai(title, adjective, model_name)

    blog_number = len(list(Path(PATH_TO_CONTENT).glob("*.html"))) + 1
    cover_image_name = f"cover_image_{blog_number}.png"
    _, cover_image_save_path = openai_utils.get_cover_image(dalle2_prompt, cover_image_name)

    timestamp = datetime.now().strftime("%Y-%m-%d")

    path_to_new_content = blog_utils.create_new_blog(PATH_TO_CONTENT, title, blog_content, cover_image_save_path, timestamp, model_name, story_idea_by)

    blog_utils.write_to_index(PATH_TO_BLOG, path_to_new_content, title, adjective, timestamp)

    blog_utils.update_blog(PATH_TO_BLOG_REPO)

if __name__ == "__main__":
    main()
