from django.shortcuts import render
from random import choice
from markdown2 import Markdown
from .forms import SearchBar, NewItem, EditItem

from . import util

def index(request):
    entries = util.list_entries()
    items = []
    if request.method == "POST":
        form = SearchBar(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            for i in entries:
                if search.lower() in i.lower():
                    items.append(i)
                if search in entries:
                    page = util.get_entry(search)
                    page_converted = Markdown().convert(page)
                    return render(request, "encyclopedia/info.html",
                                  {"entry": page_converted, "title": search, "form": SearchBar()})
            return render(request, "encyclopedia/search.html", {"searched": items, "form": SearchBar()})

        else:
            return render(request, "encyclopedia/index.html", {"form": form})
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(), "form": SearchBar()
        })

def new(request):
    form = NewItem(request.POST)
    if request.method == "POST" and form.is_valid():
        title = form.cleaned_data["title"]
        textarea = form.cleaned_data["textarea"]
        entries = util.list_entries()
        if title in entries:
            return render(request, "encyclopedia/error.html",
                          {"msg": "This item is already in use.", "form": SearchBar()})
        else:
            final_text = "#" + title + "\n" + textarea
            util.save_entry(title, final_text)
            entry = Markdown().convert(util.get_entry(title))
            return render(request, "encyclopedia/info.html", {
                "entry": entry, "title": title, "form": SearchBar()
            })
    else:
        return render(request, "encyclopedia/new.html", {
            "form": SearchBar(), "post": NewItem()
        })

def random(request):
    entries = choice(util.list_entries())
    entry = util.get_entry(entries)
    return render(request, "encyclopedia/info.html", {
        "title": entries,
        "form": SearchBar,
        "entry": Markdown().convert(entry)
    })

def info(request, title):
    entry = util.get_entry(title)
    msg = "This item doesn't exist"
    if entry:
        return render(request, "encyclopedia/info.html", {
            "title": title, "entry": Markdown().convert(entry),
            "form": SearchBar()
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "msg": msg,
            "form": SearchBar()
        })

def edit(request, title):
    if request.method == 'GET':
        page = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",
                      {"form": SearchBar(), "edit": EditItem(initial={'textarea': page}), 'title': title})
    else:
        form = EditItem(request.POST)
        if form.is_valid():
            textarea = form.cleaned_data["textarea"]
            util.save_entry(title, textarea)
            entry = Markdown().convert(util.get_entry(title))
            return render(request, "encyclopedia/info.html", {"form": SearchBar(), "entry": entry, "title": title})

