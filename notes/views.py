from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count
from django.core.paginator import Paginator
from unicodedata import category
from django.db.models import Q
from django.db import transaction
from .tasks import notify_note_created

from .forms import  NoteForm
from .models import Note, Category
from .services import get_categories_with_counts, notify_external_service

PAGE_SIZE = 20

def index(request):
    notes = Note.objects.select_related("category", "owner").prefetch_related("tags")
    if request.GET.get("category"):
        notes = notes.filter(category_id=request.GET["category"])
    if request.GET.get("active"):
        notes = notes.filter(is_done=False)
    if request.GET.get("q"):
        notes = notes.filter(title__icontains=request.GET["q"])

    paginator = Paginator(notes,20)
    page = paginator.get_page(request.GET.get("page"))
    categories = get_categories_with_counts()
    return render(request, "notes/note_list.html", {
        "page": page, "categories": categories,
    })

def note_create(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save()
            transaction.on_commit(lambda: notify_note_created.delay(note.pk))
            return redirect("notes:index")
    else:
        form = NoteForm()
    return render(request, "notes/note_form.html", {"form": form, "title": "Новая заметка"})

def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect("notes:index")
    else:
        form = NoteForm(instance=note)
    return render(request, "notes/note_form.html", {"form": form, "title": "Редактирование"})

def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == "POST":
        note.delete()
        return redirect("notes:index")
    return render(request, "notes/note_confirm_delete.html", {"note": note})

def feed(request):
    notes = Note.objects.select_related("category", "owner").prefetch_related("tags")
    after = request.GET.get("after")
    if after:
        last = Note.objects.only("created_at").get(pk=after)
        notes = notes.filter(
            Q(created_at__lt=last.created_at)
            | Q(created_at=last.created_at, id__lt=last.pk)
        )
    notes = list(notes[:PAGE_SIZE + 1])
    has_next = len(notes) > PAGE_SIZE
    notes = notes[:PAGE_SIZE]
    return render(request, "notes/note_feed.html", {
        "notes": notes,
        "next_after": notes[-1].pk if has_next else None,
    })