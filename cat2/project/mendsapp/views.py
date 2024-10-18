from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import ImageCategory, Image
from .forms import CategoryData, ImageData
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    categoryForm = CategoryData()
    imageForm = ImageData()
    return render(request, 'add.html', {"categoryForm": categoryForm, "imageForm": imageForm})

def add_category(request):
    if request.method == "POST":
        categoryForm = CategoryData(request.POST)
        if categoryForm.is_valid():
            categoryForm.save()
            return HttpResponseRedirect(reverse('view'))
        else:
            categoryForm = CategoryData()
        return render(request, 'home.html', {"categoryForm": categoryForm})

def add_image(request):
    if request.method == "POST":
        imageForm = ImageData(request.POST, request.FILES)
        if imageForm.is_valid():
            imageForm.save()
            return HttpResponseRedirect(reverse('view'))
        else:
            imageForm = CategoryData()
        return render(request, 'home.html', {"imageForm": imageForm})

def view(request):
    dbCategorys = ImageCategory.objects.all()
    dbImages = Image.objects.all()
    return render(request, 'view.html', {"dbCategorys": dbCategorys, "dbImages": dbImages})

def view_cate(request, category_name):
    category = get_object_or_404(ImageCategory, name=category_name)
    image = Image.objects.filter(category=category).order_by('?')
    return render(request, 'view_cate.html', {"category": category, "image": image})

def search(request):
    query = request.GET.get('search', '')  # Get the search term from the request
    results = []  # Initialize an empty list to hold the search results

    if request.method == "GET" and query:  # Check if there's a search query
        results = Image.objects.filter(
            Q(name__icontains=query) | Q(category__name__icontains=query)  # Search by image name or category name (case insensitive)
        )

    paginator = Paginator(results, 10)  # Show 2 results per page
    page_number = request.GET.get('page')  # Get the current page number from the request
    
    try:
        results = paginator.get_page(page_number)  # Get the results for the current page
    except PageNotAnInteger:
        results = paginator.get_page(1)  # If page number is not an integer, deliver first page
    except EmptyPage:
        results = paginator.get_page(paginator.num_pages)  # If page number is out of range, deliver last page

    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'search.html', context)  # Adjust to your template name

def download_image(request, image_id):
    """Download an image file."""
    image = get_object_or_404(Image, id=image_id)  # Get the image or return 404 if not found
    response = HttpResponse(image.file, content_type='image/jpeg')  # Change content_type as needed
    response['Content-Disposition'] = f'attachment; filename="{image.name}"'  # Set the download filename
    return response
