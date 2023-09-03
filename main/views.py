from django.shortcuts import render
from django.http import HttpResponse
import chromadb
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


def home(request):

    url = 'https://tailwindcss.com/docs/screens'

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        anchor_tags = soup.find_all('a')
        proper_links = []
        parsed_start_url = urlparse(url)
        for anchor_tag in anchor_tags:
            link = anchor_tag.get('href')
            if link:
                absolute_link = urljoin(url, link)
                parsed_absolute_link = urlparse(absolute_link)
                if parsed_absolute_link.netloc == parsed_start_url.netloc and '#' not in absolute_link:
                    proper_links.append(absolute_link)

        folder_name = 'code_snippets'
        os.makedirs(folder_name, exist_ok=True)
        for link in proper_links:
            print(link)
            response = requests.get(link)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                code_tags = soup.find_all('code')
                minimum_code_size = 50
                for index, code_tag in enumerate(code_tags):
                    code_content = code_tag.get_text()
                    if len(code_content) >= minimum_code_size:
                        filename = os.path.join(
                            folder_name, f'code_{index + 1}.txt')
                        with open(filename, 'w', encoding='utf-8') as code_file:
                            code_file.write(code_content)

                print(
                    f'Code snippets have been saved to the "{folder_name}" folder.')

    else:
        print('Failed to retrieve data from the website.')
    return HttpResponse("hello world i love you")


def read_files_from_folder(folder_path):
    file_data = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            with open(os.path.join(folder_path, file_name), 'r') as file:
                content = file.read()
                file_data.append({"file_name": file_name, "content": content})
            print(file_name)
    return file_data


def ask(request):
    chroma_client = chromadb.Client()
    code_collection = chroma_client.create_collection("code_collection")
    folder_path = "code_snippets"
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            with open(os.path.join(folder_path, file_name), 'r') as file:
                content = file.read()
                metadata = {'source': file_name}
                code_collection.add(
                    documents=content,
                    metadatas=metadata,
                    ids=file_name
                )
            print("added to embedding"+metadata['source'])
    results = code_collection.query(
        query_texts=["How do i order flex and grid items?"],
        n_results=1
    )

    print(results['documents'][0][0])
    return render(request, "home.html")
