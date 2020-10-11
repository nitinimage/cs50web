from django.shortcuts import render, redirect
from django import forms
from . import util
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
import random

class entryform(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    content = forms.CharField(label= "Content", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, title):
    return render(request, "encyclopedia/page.html", {
        "entry_data": util.get_entry(title),
        "title": title
    })


def edit_page(request, title):
    if request.method == "GET":
        form = entryform(initial={
            'title':title,
            'content':util.get_entry(title)})  
        return render(request, "encyclopedia/edit_page.html", {
            "form" : form ,
            "title" : title

        })
    else:
        form = entryform(request.POST)
        if form.is_valid():
            updated_title = form.cleaned_data["title"]
            updated_content = form.cleaned_data["content"]
            if updated_title.lower() in [entry.lower() for entry in util.list_entries()] and updated_title.lower() != title.lower():
                return redirect(create_error)
            util.delete_entry(title)
            util.save_entry(updated_title,updated_content) 
            return redirect(page,title = updated_title)
        else:
            return render(request, "encyclopedia/edit_page.html",{
                "form" : form
            })



def create(request):
    if request.method == "POST":
        form = entryform(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title.lower() in [entry.lower() for entry in util.list_entries()]:
                return redirect(create_error)
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

def create_error(request):
    return render(request, "encyclopedia/create_error.html")

def search(request):
        query = request.GET.get('q')
        search_results = util.search_entries(query)
        return render(request, "encyclopedia/search.html",{
            "search_results": search_results
        })

def random_page(request):
    random_page = random.choice(util.list_entries())
    return render(request, "encyclopedia/page.html", {
        "entry_data": util.get_entry(random_page),
        "title": random_page
    })
    # return redirect(page,title = random_page)