

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Movie, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import base64
from io import BytesIO
from collections import Counter

def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'name':'Nicolas Vasquez', 'searchTerm':searchTerm, 'movies': movies})

def about(request):
    return render(request, 'about.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def detail(request, movie_id):
    movie = get_object_or_404(Movie,pk=movie_id)
    reviews = Review.objects.filter(movie = movie)
    return render(request, 'detail.html', {'movie':movie, 'reviews': reviews})

@login_required
def createreview(request, movie_id):
    movie = get_object_or_404(Movie,pk=movie_id)
    if request.method == 'GET':
        return render(request, 'createreview.html', {'form':ReviewForm(), 'movie': movie})
    else:
        try:
            form = ReviewForm(request.POST)
            newReview = form.save(commit=False)
            newReview.user = request.user
            newReview.movie = movie
            newReview.save()
            return redirect('detail', newReview.movie.id)
        except ValueError:
            return render(request, 'createreview.html', {'form':ReviewForm(),'error':'bad data passed in'})

@login_required
def updatereview(request, review_id):
    review = get_object_or_404(Review,pk=review_id,user=request.user)
    if request.method == 'GET':
        form = ReviewForm(instance=review)
        return render(request, 'updatereview.html',{'review': review,'form':form})
    else:
        try:
            form = ReviewForm(request.POST, instance=review)
            form.save()
            return redirect('detail', review.movie.id)
        except ValueError:
            return render(request, 'updatereview.html',{'review': review,'form':form,'error':'Bad data in form'})

@login_required
def deletereview(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    review.delete()
    return redirect('detail', review.movie.id)

def statistics_view(request):
    movies = Movie.objects.all()
    
    # Gráfica por año
    years = [movie.year for movie in movies if movie.year]
    year_counts = Counter(years)
    
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.bar(year_counts.keys(), year_counts.values())
    plt.title('Movies by Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    plt.xticks(rotation=45)
    
    # Gráfica por género (primer género)
    genres = []
    for movie in movies:
        if movie.genre:
            first_genre = movie.genre.split('/')[0].strip()
            genres.append(first_genre)
    
    genre_counts = Counter(genres)
    
    plt.subplot(1, 2, 2)
    plt.bar(genre_counts.keys(), genre_counts.values())
    plt.title('Movies by Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    
    # Convertir a base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    graphic = base64.b64encode(image_png).decode('utf-8')
    plt.close()
    
    return render(request, 'statistics.html', {'graphic': graphic})


