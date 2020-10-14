from django.shortcuts import render, redirect
from django import forms
from . import util
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
import random

class entryform(forms.Form):
    title = forms.CharField(label="Title", 
                            max_length=100, 
                            widget=forms.TextInput(attrs={'placeholder': 'Title'}) )
    content = forms.CharField(label= "Content", 
                              widget=forms.Textarea(attrs={'placeholder': 'Write here! Be Nice'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, title):
    try:
        #get a list of of all titles in lower case
        entries = [entry.lower() for entry in util.list_entries()]
        index = entries.index(title.lower())
        if title != util.list_entries()[index]: 
            new_title = util.list_entries()[index]
            return redirect(page, title = new_title) #redirect to proper case string
    except:
        title = title
    return render(request, "encyclopedia/page.html", {
        "entry_data": util.md_to_html(util.get_entry(title)) ,
        "title": title
    })


def edit_page(request, title):
    if request.method == "GET":
        #check if title exists
        entries = [entry.lower() for entry in util.list_entries()]
        if title.lower() in entries:
            form = entryform(initial={
                'title':title,
                'content':util.get_entry(title)})  
            return render(request, "encyclopedia/edit_page.html", {
                "form" : form ,
                "title" : title
            })
        else:
            return redirect(error, error='title not found')
    # POST method
    else:
        form = entryform(request.POST)
        if form.is_valid():
            updated_title = form.cleaned_data["title"]
            updated_content = form.cleaned_data["content"]
            if updated_title.lower() in [entry.lower() 
                                        for entry in util.list_entries()] and updated_title.lower() != title.lower():
                return redirect(error, error = 'title exists')
            util.delete_entry(title)
            util.save_entry(updated_title,updated_content) 
            return redirect(page,title = updated_title)
        else:
            return render(request, "encyclopedia/edit_page.html",{
                "form" : form
            })

def delete_page(request, title):
    util.delete_entry(title)
    return render(request,"encyclopedia/delete_page.html",{
        "title" : title
    })


def create(request):
    if request.method == "POST":
        form = entryform(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title.lower() in [entry.lower() for entry in util.list_entries()]:
                return redirect(error, error = 'title exists')
            util.save_entry(title,content)
            return redirect(page,title = title)
        else:
            return render(request, "encyclopedia/create.html",{
                "form" : form
            })
    else:
        return render(request, "encyclopedia/create.html",{
            "form" : entryform()
        })

def error(request, error):
    error_message = 'Error'
    if error == 'title exists':
        error_message = "Title already exists! Please try another title"
    if error == 'title not found':
        error_message = 'Title does not exist!'
    return render(request, "encyclopedia/error.html",{
        "error_message" : error_message
    })

def search(request):
    query = request.GET.get('q')
    search_results = util.search_entries(query)
    if len(search_results) == 1:
        return redirect(page, title = search_results[0])
    return render(request, "encyclopedia/search.html",{
        "search_results": search_results
    })

def random_page(request):
    random_page = random.choice(util.list_entries())
    return render(request, "encyclopedia/page.html", {
        "entry_data": util.md_to_html(util.get_entry(random_page)),
        "title": random_page
    })
    # return redirect(page,title = random_page)