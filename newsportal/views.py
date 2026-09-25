from django.shortcuts import render
from articles.models import Article

def home(request):

    latest_articles = Article.objects.filter(
        status='published'
    ).order_by(
        '-created_at'
    )[:6]

    return render(
        request,
        'home.html',
        {
            'latest_articles': latest_articles,
        }
    )