
import os

git_executable_path = 'C:/Stephen/Software/Git/bin/git.exe'  # Replace with the correct path to your git executable if different
os.environ['GIT_PYTHON_GIT_EXECUTABLE'] = git_executable_path

from git import Repo

from pathlib import Path
import shutil
import os
from jinja2 import Template

from bs4 import BeautifulSoup as Soup
from git import Repo


def create_new_blog(path_to_content, title, content, cover_image, timestamp, model_name, story_idea_by):

    path_to_content = Path(path_to_content)
    cover_image = Path(cover_image)
    
    files = len(list(path_to_content.glob("*.html")))
    new_title = f"{files + 1}.html"
    path_to_new_content = path_to_content / new_title
    
    with open(Path(__file__).parent / 'base_template.html') as f:
        template = Template(f.read())

    # Use a relative path for the cover image
    relative_cover_image = f"{cover_image.name}"

    # Pass the timestamp and model name to the template
    rendered_template = template.render(title=title, content=content, cover_image=relative_cover_image, timestamp=timestamp, model_name=model_name, story_idea_by=story_idea_by)


    shutil.copy(cover_image, path_to_content)
    with open(path_to_new_content, "w") as f:
        f.write(rendered_template)
    
    print("Blog created")
    return path_to_new_content


def check_for_duplicate_links(path_to_new_content, links):
    urls = [str(link.get("href")) for link in links]
    content_path = str(Path(*path_to_new_content.parts[-2:]))
    return content_path in urls


def write_to_index(path_to_blog, path_to_new_content, title, adjective, timestamp):
    with open(path_to_blog/"index.html") as index:
        soup = Soup(index.read(), features="lxml")

    links = soup.find_all("a")

    link_to_new_blog = soup.new_tag("a", href=Path(*path_to_new_content.parts[-2:]))
    
    post_title = soup.new_tag("span", attrs={"class": "post-title"})
    post_title.string = title
    link_to_new_blog.append(post_title)
    
    post_adjective = soup.new_tag("span", attrs={"class": "post-adjective"})
    post_adjective.string = adjective.capitalize()
    link_to_new_blog.append(post_adjective)

    post_timestamp = soup.new_tag("span", attrs={"class": "post-timestamp"})
    post_timestamp.string = timestamp
    link_to_new_blog.append(post_timestamp)

    new_post_div = soup.new_tag("div", attrs={"class": "index-post"})
    new_post_div.append(link_to_new_blog)

    if links:
        if check_for_duplicate_links(path_to_new_content, links):
            raise ValueError("Link does already exist!")

        # Insert the newest blog at the top
        soup.body.main.insert(0, new_post_div)  # Change this line
    else:
        soup.body.main.append(new_post_div)

    with open(path_to_blog/"index.html", "w") as f:
        f.write(str(soup.prettify(formatter='html')))


def update_blog(path_to_blog_repo, commit_message="Updated blog"):
    repo = Repo(path_to_blog_repo)
    repo.git.add(all=True)
    repo.index.commit(commit_message)
    origin = repo.remote(name='origin')
    origin.push()
