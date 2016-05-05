from django.shortcuts import render

from django.http import HttpResponse

from rango.models import Page, Category

#from rango.models import Category

def index(request):

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    # Render the response and send it back!
    return render(request, 'rango/index.html', context_dict)




def about(request):
    p = Page.objects.all()
    context_dict = { 'list_items': p }
     # reminder on templates u can't do python like print for the data, no need ...just do {{}}
    return render(request, 'rango/about.html', context_dict)
