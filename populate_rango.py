import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page


python_pages = [
    {"title": "Official Python Tutorial",
     "url": "http://docs.python.org/2/tutorial/"},
    {"title":"How to Think like a Computer Scientist",
     "url": "http://www.greenteapress.com/thinkpython/"},
    {"title": "Learn Python in 10 Minutes",
     "url": "http://www.korokithakis.net/tutorials/python/"},
    {"title": "Test",
     "url": "http://www.test/"}]

django_pages = [
    {"title": "Official Django Tutorial",
     "url": "https://docs.djangoproject.com/en/1.9/intro/tutorial01/"},
    {"title": "Django Rocks",
     "url": "http://www.djangorocks.com/"},
    {"title": "How to Tango with Django",
     "url": "http://www.tangowithdjango.com/"}]

other_pages = [
    {"title": "Bottle",
     "url": "http://bottlepy.org/docs/dev/"},
    {"title": "Flask",
     "url": "http://flask.pocoo.org"}]

cats = {"Python": {"pages": python_pages},
        "Django": {"pages": django_pages},
        "Other Frameworks": {"pages": other_pages}}


def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    if name is 'Python':
        c.views = 128
        c.likes = 64
    if name is 'Django':
        c.views = 64
        c.likes = 32
    else:
        c.views = 32
        c.likes = 16
    c.save()
    return c


def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title, url=url, views=views)[0]
    return p


def populate():
    for c, c_data in cats.items():
        c = add_cat(c)
        for page in c_data['pages']:
            add_page(c, page["title"], page["url"])

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))


if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()



