from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Item
from .forms import ItemForm


def list_view(request):
    object_list = Item.objects.all().order_by('-created_at')
    return render(request, 'myapp/index.html', {'object_list': object_list})


def create_view(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        return render(request, 'myapp/form.html', {'form': form}, status=400)
    form = ItemForm()
    return render(request, 'myapp/form.html', {'form': form})


def update_view(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('index')
        return render(request, 'myapp/form.html', {'form': form, 'object': item}, status=400)
    form = ItemForm(instance=item)
    return render(request, 'myapp/form.html', {'form': form, 'object': item})


def delete_view(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('index')
    return render(request, 'myapp/confirm_delete.html', {'object': item})


def ping_view(request):
    return HttpResponse("OK", status=200)
