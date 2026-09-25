from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from .forms import CommentForm, ArticleForm
from .models import Article, Category, Comment, Like, Bookmark, Notification


def article_list(request):

    category = request.GET.get('category')
    search = request.GET.get('search')

    articles = Article.objects.filter(
        status='published'
    ).order_by('-created_at')

    categories = Category.objects.all()

    # Category filter
    if category:
        articles = articles.filter(
            category__slug=category
        )

    # Search filter
    if search:
        articles = articles.filter(
            title__icontains=search
        )

    # Pagination
    paginator = Paginator(articles, 6)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'articles/article_list.html',
        {
            'articles': page_obj,
            'categories': categories,
            'search': search,
            'category': category,
        }
    )

def article_detail(request, slug):

    article = get_object_or_404(
        Article,
        slug=slug,
        status='published'
    )

    # Increase article views
    article.views += 1

    article.save(
        update_fields=['views']
    )

    comments = article.comments.all().order_by(
        '-created_at'
    )

    # =========================
    # LIKE DATA
    # =========================

    like_count = article.likes.count()

    user_liked = False

    if request.user.is_authenticated:

        user_liked = article.likes.filter(
            user=request.user
        ).exists()

    # =========================
    # BOOKMARK DATA
    # =========================

    bookmark_count = article.bookmarks.count()

    user_bookmarked = False

    if request.user.is_authenticated:

        user_bookmarked = article.bookmarks.filter(
            user=request.user
        ).exists()

    # =========================
    # COMMENT
    # =========================

    if request.method == 'POST':

        if not request.user.is_authenticated:
            return redirect('login')

        form = CommentForm(request.POST)

        if form.is_valid():

            comment = form.save(
                commit=False
            )

            comment.article = article
            comment.user = request.user

            comment.save()

            # =========================
            # COMMENT NOTIFICATION
            # =========================

            # Don't notify the author
            # if they comment on their own article

            if article.author != request.user:

                Notification.objects.create(
                    recipient=article.author,
                    sender=request.user,
                    article=article,
                    notification_type='comment',
                    message=f'{request.user.username} commented on your article "{article.title}"'
                )

            return redirect(
                'article_detail',
                slug=article.slug
            )

    else:

        form = CommentForm()

    return render(
        request,
        'articles/article_detail.html',
        {
            'article': article,
            'comments': comments,
            'form': form,

            # Like data
            'like_count': like_count,
            'user_liked': user_liked,

            # Bookmark data
            'bookmark_count': bookmark_count,
            'user_bookmarked': user_bookmarked,
        }
    )

def delete_comment(request, comment_id):

    if not request.user.is_authenticated:
        return redirect('login')

    comment = get_object_or_404(
        Comment,
        id=comment_id
    )

    if (
        request.method == 'POST'
        and comment.user == request.user
    ):

        article_slug = comment.article.slug

        comment.delete()

        return redirect(
            'article_detail',
            slug=article_slug
        )

    return redirect(
        'article_detail',
        slug=comment.article.slug
    )


def edit_comment(request, comment_id):

    if not request.user.is_authenticated:
        return redirect('login')

    comment = get_object_or_404(
        Comment,
        id=comment_id
    )

    # Only comment owner can edit
    if comment.user != request.user:

        return redirect(
            'article_detail',
            slug=comment.article.slug
        )

    if request.method == 'POST':

        form = CommentForm(
            request.POST,
            instance=comment
        )

        if form.is_valid():

            form.save()

            return redirect(
                'article_detail',
                slug=comment.article.slug
            )

    else:

        form = CommentForm(
            instance=comment
        )

    return render(
        request,
        'articles/edit_comment.html',
        {
            'form': form,
            'comment': comment,
        }
    )


def create_article(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':

        form = ArticleForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            article = form.save(
                commit=False
            )

            article.author = request.user

            article.save()

            return redirect(
                'article_detail',
                slug=article.slug
            )

    else:

        form = ArticleForm()

    return render(
        request,
        'articles/create_article.html',
        {
            'form': form,
        }
    )


def my_articles(request):

    if not request.user.is_authenticated:
        return redirect('login')

    articles = Article.objects.filter(
        author=request.user
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'articles/my_articles.html',
        {
            'articles': articles,
        }
    )

def like_article(request, slug):

    if not request.user.is_authenticated:
        return redirect('login')

    article = get_object_or_404(
        Article,
        slug=slug,
        status='published'
    )

    like = Like.objects.filter(
        article=article,
        user=request.user
    ).first()

    if like:

        # Unlike
        like.delete()

        # Remove corresponding notification
        Notification.objects.filter(
            recipient=article.author,
            sender=request.user,
            article=article,
            notification_type='like'
        ).delete()

    else:

        # Like
        Like.objects.create(
            article=article,
            user=request.user
        )

        # Don't notify yourself
        if article.author != request.user:

            Notification.objects.create(
                recipient=article.author,
                sender=request.user,
                article=article,
                notification_type='like',
                message=f'{request.user.username} liked your article "{article.title}"'
            )

    return redirect(
        'article_detail',
        slug=article.slug
    )

def edit_article(request, slug):

    if not request.user.is_authenticated:
        return redirect('login')

    article = get_object_or_404(
        Article,
        slug=slug
    )

    # Only article owner can edit
    if article.author != request.user:

        return redirect(
            'article_detail',
            slug=article.slug
        )

    if request.method == 'POST':

        form = ArticleForm(
            request.POST,
            request.FILES,
            instance=article
        )

        if form.is_valid():

            form.save()

            return redirect(
                'article_detail',
                slug=article.slug
            )

    else:

        form = ArticleForm(
            instance=article
        )

    return render(
        request,
        'articles/edit_article.html',
        {
            'form': form,
            'article': article,
        }
    )


def delete_article(request, slug):

    if not request.user.is_authenticated:
        return redirect('login')

    article = get_object_or_404(
        Article,
        slug=slug
    )

    # Only article owner can delete
    if article.author != request.user:

        return redirect(
            'article_detail',
            slug=article.slug
        )

    if request.method == 'POST':

        article.delete()

        return redirect(
            'my_articles'
        )

    return render(
        request,
        'articles/delete_article.html',
        {
            'article': article,
        }
    )


def category_articles(request, slug):

    category = get_object_or_404(
        Category,
        slug=slug
    )

    articles = Article.objects.filter(
        category=category,
        status='published'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'articles/category_articles.html',
        {
            'category': category,
            'articles': articles,
        }
    )



def bookmark_article(request, slug):

    if not request.user.is_authenticated:
        return redirect('login')

    article = get_object_or_404(
        Article,
        slug=slug,
        status='published'
    )

    bookmark = Bookmark.objects.filter(
        article=article,
        user=request.user
    ).first()

    if bookmark:

        # =========================
        # REMOVE BOOKMARK
        # =========================

        bookmark.delete()

        # Remove corresponding notification
        Notification.objects.filter(
            recipient=article.author,
            sender=request.user,
            article=article,
            notification_type='bookmark'
        ).delete()

    else:

        # =========================
        # ADD BOOKMARK
        # =========================

        Bookmark.objects.create(
            article=article,
            user=request.user
        )

        # Don't notify yourself
        if article.author != request.user:

            Notification.objects.create(
                recipient=article.author,
                sender=request.user,
                article=article,
                notification_type='bookmark',
                message=(
                    f'{request.user.username} bookmarked '
                    f'your article "{article.title}"'
                )
            )

    return redirect(
        'article_detail',
        slug=article.slug
    )

def my_bookmarks(request):

    if not request.user.is_authenticated:
        return redirect('login')

    bookmarks = Bookmark.objects.filter(
        user=request.user
    ).select_related(
        'article',
        'article__category',
        'article__author'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'articles/my_bookmarks.html',
        {
            'bookmarks': bookmarks,
        }
    )