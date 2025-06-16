import datetime
import os
import pybtex
import setuptools
import yaml
import shutil
import importlib.resources as pkg_resources
from livereload import Server, shell
from pybtex.database import parse_file
from pybtex.plugin import find_plugin
from livereload import Server


# Constants
BUILD_DIR = '_build'

def generate_html(output, content, template, title, year, links): 
    """Generates an HTML file by replacing placeholders in the TEMPLATE."""        
    html_content = template.format(title=title, content=content, year=year)
    for link in links:
        
        html_content = html_content.replace(
            f"{{{link['name']}}}",
            f"""
            <a href="{link['url']}">{link['name']}</a>
            """
        )

    with open(output, 'w', encoding='utf-8') as file:
        file.write(html_content)
    print(f"Generated {output} successfully.")

def build():
    YEAR = datetime.datetime.now().year
    DATA = yaml.safe_load(open(
        pkg_resources.files(__package__).joinpath('data/data.yaml'),
        'r',
        encoding='utf-8'))
    TITLE = DATA.get('title', 'MadSuite')
    INTRO = DATA.get('intro', '')
    MEMBERS = DATA.get('members', [])
    PACKAGES = DATA.get('packages', [])
    NEWS = DATA.get('news', [])
    LINKS = DATA.get('links', [])
    TEMPLATE = open(
        pkg_resources.files(__package__).joinpath('data/template.html'),
        'r', encoding='utf-8').read()

    """Main function to generate the HTML content and create the index.html file."""
    # Generate HTML list for packages
    members_html = "\n".join([
        f"""
        <li>
            <a href="{member['url']}"><strong>{member['name']}</strong></a> ({member['role']}): {member['description']}
        </li>
        """ for member in MEMBERS
    ])
    
    news_html = "\n".join([
        f"""
        <li>
        <strong>{news['date']}</strong>: {news['entry']} 
        </li>
        """ for news in NEWS
    ])

    packages_html = "\n".join([
        f"""
        <li>
            <strong><a href="{pkg['url']}">{pkg['name']}</a></strong>: {pkg['description']}
        </li>
        """ for pkg in PACKAGES
    ])
    
    # Generate HTML list for publications
    bib_data = parse_file(
        pkg_resources.files(__package__).joinpath('data/references.bib'),
    )
    style = find_plugin('pybtex.style.formatting', 'plain')()
    formatted_bib = style.format_bibliography(bib_data)
    publications_html = "\n".join([
        "<li>{entry}</li>".format(entry = entry.text.render_as('html'))
        for entry in formatted_bib
    ])

    # Combine all content
    content = f"""
    <h1 class="mb-4">Home</h1>
    <p>
        {INTRO}
    </p>
    <h2 class="mt-5">Members</h2>
    <ul>
        {members_html}
    </ul>
    <h2 class="mt-5">News</h2>
    <ul>
        {news_html}
    </ul>
    <h2 class="mt-5">Packages</h2>
    <ul>
        {packages_html}
    </ul>
    <h2 class="mt-5">Publications</h2>
    <ul>
        {publications_html}
    </ul>
    """

    # Generate the HTML file
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
    os.makedirs(BUILD_DIR)
    generate_html(os.path.join(BUILD_DIR, "index.html"), content, TEMPLATE, TITLE, YEAR, LINKS)

def serve():
    # Do initial build before starting
    print("Running initial build...")
    build()

    server = Server()
    server.watch(
        './*',
        build,
    )
    server.serve(root=BUILD_DIR, port=8000) 

    
