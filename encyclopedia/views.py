from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
import secrets

import random
from random import randint


from . import util

from markdown2 import Markdown
markdowner = Markdown()

class newEntry(forms.Form):
    title = forms.CharField(label="Title")
    textarea = forms.CharField(widget=forms.Textarea(), label='')

class Edit(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(), label='')

class Search(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs={'class':'myfieldclass', 'placeholder':'Search'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    entries = util.list_entries()
    if entry in entries:
        entryPage = util.get_entry(entry)
        pageconverted = markdowner.convert(entryPage)

        return render(request, "encyclopedia/entry.html", {
            'entry': pageconverted,
            'title': entry,
            'form': Search()
        })
    else:
       return render(request, "encyclopedia/error.html", {
           'message': 'Page was not found!'
       })

def create(request):
    if request.method == "POST":
        form = newEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            textarea =  form.cleaned_data["textarea"]
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/error.html", {
                    'message': "Page already exist!",
                    'form': Search()
                })
            else:
                util.save_entry(title, textarea)
                entry = util.get_entry(title)
                entry_convert = markdowner.convert(entry)

                return render(request, "encyclopedia/entry.html", {
                    'page': entry_convert,
                    'title': title,
                    'form': Search()
                })
    else:
        return render(request, "encyclopedia/create.html", {
            'post': newEntry(),
            'form': Search()
        })


def search(request):
    value = request.GET.get('q','')
    if(util.get_entry(value) is not None):
        return HttpResponseRedirect(reverse("entry", kwargs={'entry': value}))
    else:
        subStr = []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                subStr.append(entry)
        
        return render(request, "encyclopedia/index.html", {
            "entries": subStr,
            "search": True,
            "value": value
        })

def edit(request, entry):
    if request.method == 'GET':
        entryPage = util.get_entry(entry)

        return render(request, "encyclopedia/edit.html", {
            'form': Search(),
            'edit': Edit(initial={'textarea': entryPage}),
            'title': entry
        })

    else:
        form = Edit(request.POST)
        if form.is_valid():
            textarea = form.cleaned_data["textarea"]
            util.save_entry(entry, textarea)
            entryPage = util.get_entry(entry)
            pageconverted = markdowner.convert(entryPage)

            return render(request, "encyclopedia/entry.html", {
                'form': Search(),
                'entry': pageconverted,
                'title': entry
            })


def randomPage(request):
    entries = util.list_entries()
    randomEntry = secrets.choice(entries)
    return HttpResponseRedirect(reverse("entry", kwargs={'entry': randomEntry}))
