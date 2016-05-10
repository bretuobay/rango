from django.template import RequestContext
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from rango.models import Page, Category
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from rango.models import Page, Category
from datetime import datetime
#from rango.models import Category

def index(request):

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    category_list = Category.objects.order_by('-likes')[:5]
    most_viewed = Page.objects.order_by('-views')[:5]
    context_dict = {
                'categories' : category_list,
                'most_viewed' : most_viewed
    }

    visits = request.session.get('visits')
    #if no visits yet, initiate?
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        #fix from 7 to 18 to fix format
        last_visit_time = datetime.strptime(last_visit[:18],"%Y-%m-%d %H:%M:%S")

        if(datetime.now()-last_visit_time).seconds > 0 :
            visits = visits + 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits

    response = render(request,'rango/index.html',context_dict)
    # Render the response and send it back!
    return response



def category(request,category_name_slug):

    #directory
    context_dict = {}

    try:
        # try and find category with this slug
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        # if we get the category, retrieve all associated pages

        pages = Page.objects.filter(category=category)
        # add this to the directory
        context_dict['pages'] = pages
        context_dict['category_name_slug'] = category.slug
        # also add the cateogry object  from the database, to be used for verifying
        #existence of a category
        context_dict['category'] = category
    except Category.DoesNotExist:
        # do nothing if no category exist
        pass
    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

def decode_url(item):
    return item.replace(' ', '')

def add_page(request, category_name_url):


    context = RequestContext(request)
    category_name = decode_url(category_name_url)


    try:
        cat = Category.objects.get(slug=category_name)
    except Category.DoesNotExist:
                cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form':form, 'category': cat}

    return render(request, 'rango/add_page.html', context_dict)
'''
@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")
'''
