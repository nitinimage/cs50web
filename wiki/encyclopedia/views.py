from django.shortcuts import render
from django import forms
from . import util
from django.urls import reverse
from django.http import HttpResponseRedirect

class newentry(forms.Form):
    new_title = forms.CharField(label="New_title")
    new_content = forms.Textarea()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, title):
    return render(request, "encyclopedia/title.html", {
        "entry_data": util.get_entry(title),
        "title": title
    })

def create(request):
    if request.method == "POST":
        form = newentry(request.POST)
        if form.is_valid():
            new_title = form.cleaned_data["new_title"]
            new_content = form.cleaned_data["new_content"]
            util.save_entry(new_title,new_content)
            return HttpResponseRedirect(reverse('create'))
        else:
            return render(request, "encyclopedia/create.html",{
                "form" : form
            })
    else:
        return render(request, "encyclopedia/create.html",{
            "form" : newentry()
        })