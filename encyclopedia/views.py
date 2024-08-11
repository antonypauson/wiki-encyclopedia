from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from . import util
from markdown2 import Markdown
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry_content = util.get_entry(title)
    if entry_content is None:
        return HttpResponseNotFound("The request page was not found")
    else:
        
        markdowner = Markdown()
        html_content = markdowner.convert(entry_content)
        # print(html_content)
        return render(request, "encyclopedia/entry.html", {
            "title": title, 
            "html_content": html_content
        })
    

def search(request):
    query = request.GET.get('q', '')
    if query:
        entries = util.list_entries()
        matching_entries = [entry for entry in entries if query.lower() in entry.lower()]

        if query in entries: 
            return redirect('entry', title=query)
        else:
            return render(request, "encyclopedia/search_results.html", {
                "query": query, 
                "entries": matching_entries
            })
        
    return redirect('index')

def create_new_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if not content.startswith("# "):
            content = f"# {title}\n\n{content}"

        util.save_entry(title,content)
        return redirect("entry", title=title)

    return render(request, "encyclopedia/create_new_page.html")

def edit(request, title):
    entry_content = util.get_entry(title)

    if request.method == "POST":
        new_content = request.POST.get("content")
        util.save_entry(title,new_content)
        return redirect("entry", title=title)

    return render(request, "encyclopedia/edit.html", {
        "title": title, 
        "content": entry_content
    })

def random_page(request):
    entries = util.list_entries()
    if entries:
        random_title = random.choice(entries)
        return redirect("entry", title=random_title)
    



    




    
