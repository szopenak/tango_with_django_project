from django.shortcuts import render
from django.http import HttpResponse
import datetime
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from django.core.urlresolvers import reverse

def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list,
                    'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!",
                    'pages': page_list}
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    st = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
    context_dict = {'cur_date': st}
    return render(request, 'rango/about.html', context=context_dict)


def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = {}
    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        # Retrieve all of the associated pages.
        # Note that filter() will return a list of page objects or an empty list
        pages = Page.objects.filter(category=category)
        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict['category'] = None
        context_dict['pages'] = None
        # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context=context_dict)


def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            cat = form.save(commit=True)
            print("Created category: ", cat, cat.slug)
            # Now that the category is saved
            # We could give a confirmation message
            # But since the most recent category added is on the index page
            # Then we can direct the user back to the index page.
            return render(request, 'rango/add_category.html', {'form': form})
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            return render(request, 'rango/add_category.html', {'form': form})
    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    else:
        return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    form = PageForm()
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                pag = form.save(commit=False)
                pag.category = cat
                pag.save()
                print('Page created: '+str(pag))
                return show_category(request, category_name_slug)
        else:
            return render(request, 'rango/add_page.html', {'form': form, 'category': cat})
    else:
        return render(request, 'rango/add_page.html', {'form': form, 'category': cat})
