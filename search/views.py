from django.shortcuts import render
import requests
from bs4 import BeautifulSoup


def search(request):
    if request.method == 'POST':
        book = request.POST['book']
        chapter = request.POST['chapter']
        verse1 = request.POST['verse_start']
        verse2 = request.POST['verse_end']

        url = f"http://ibibles.net/quote.php?kor-{book}/{chapter}:{verse1}-{verse2}"
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')

        verse_list = []
        verses = soup.find_all('small')
        for verse in verses:
            verse_list.append(verse.text)

        content_list = []
        contents = soup.find_all('body')[0].contents
        for content in contents:
            if content != '\n' and not content.name:
                content_list.append(content)

        verse_list = [verse.text.strip() for verse in soup.find_all('small')]
        content_list = [content.text.strip() for content in soup.find_all('body')]
        verse_content_list = list(zip(verse_list, content_list))

        return render(request, 'index.html', {'verse_content_list': verse_content_list})
    else:
        return render(request, 'index.html')
