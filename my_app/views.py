import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models
# Create your views here.

BASE_ADVERTS_URL = 'https://www.adverts.ie/for-sale/q_{}/price_{}-{}/'
# BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    from_price = request.POST.get('from_price', 0)
    to_price = request.POST.get('to_price', 1000)
    final_url = BASE_ADVERTS_URL.format(quote_plus(search), from_price, to_price)
    print(final_url)
    # Getting the webpage, creating a Response object.
    response = requests.get(final_url)
    # Extracting the source code of the page.
    data = response.text
    # Passing the source code to Beautiful Soup to create a BeautifulSoup object for it.
    soup = BeautifulSoup(data, features="html.parser")
    # Extracting all the <div> tags whose class name is 'sr-grid-cell quick-peek-container' into a list.
    post_listings = soup.find_all('div', {'class':
                                          'sr-grid-cell quick-peek-container'})
    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='title').text
        post_url = "https://www.adverts.ie" + post.find(
            class_='main-image').get('href')
        if post.find(class_='price'):
            post_price = post.find(class_='price').text
        else:
            post_price = 'N/A'

        ''' if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(
                class_='result-image').get(
                'data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'
        '''
        post_image_url = post.find('img').get('src')
        final_postings.append((post_title, post_url, post_price, post_image_url))

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
