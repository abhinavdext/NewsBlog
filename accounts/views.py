import random

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Count, Sum

from articles.models import (
    Article,
    Comment,
    Like,
    Bookmark,
    Notification
)


# ==========================================
# CAPTCHA HELPER
# ==========================================

def generate_captcha(request):

    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)

    request.session['captcha_answer'] = num1 + num2

    return num1, num2


# ==========================================
# USER REGISTER
# ==========================================

def register(request):

    if request.method == 'POST':

        username = request.POST.get(
            'username',
            ''
        ).strip()

        email = request.POST.get(
            'email',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )

        confirm_password = request.POST.get(
            'confirm_password',
            ''
        )

        captcha = request.POST.get(
            'captcha',
            ''
        ).strip()

        # ==================================
        # CAPTCHA CHECK
        # ==================================

        correct_answer = request.session.get(
            'captcha_answer'
        )

        if (
            correct_answer is None
            or not captcha.isdigit()
            or int(captcha) != correct_answer
        ):

            messages.error(
                request,
                "Incorrect CAPTCHA. Please solve it correctly."
            )

            num1, num2 = generate_captcha(request)

            return render(
                request,
                'accounts/register.html',
                {
                    'num1': num1,
                    'num2': num2,
                    'old_username': username,
                    'old_email': email,
                }
            )

        # ==================================
        # USERNAME CHECK
        # ==================================

        if not username:

            messages.error(
                request,
                "Username is required."
            )

            num1, num2 = generate_captcha(request)

            return render(
                request,
                'accounts/register.html',
                {
                    'num1': num1,
                    'num2': num2,
                    'old_username': username,
                    'old_email': email,
                }
            )


        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "Username already exists."
            )

            num1, num2 = generate_captcha(request)

            return render(
                request,
                'accounts/register.html',
                {
                    'num1': num1,
                    'num2': num2,
                    'old_username': username,
                    'old_email': email,
                }
            )

        # ==================================
        # EMAIL CHECK
        # ==================================

        if not email:

            messages.error(
                request,
                "Email address is required."
            )

            num1, num2 = generate_captcha(request)

            return render(
                request,
                'accounts/register.html',
                {
                    'num1': num1,
                    'num2': num2,
                    'old_username': username,
                    'old_email': email,
                }
            )


        if User.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                "Email already registered."
            )

            num1, num2 = generate_captcha(request)

            return render(
                request,
                'accounts/register.html',
                {
                    'num1': num1,
                    'num2': num2,
                    'old_username': username,
                    'old_email': email,
                }
            )

        # ==================================
        # PASSWORD CHECK
        # ==================================

        if not password:

            messages.error(
                request,
                "Password is required."
            )

            num1, num2 = generate_captcha(request)

            return render(
                request,
                'accounts/register.html',
                {
                    'num1': num1,
                    'num2': num2,
                    'old_username': username,
                    'old_email': email,
                }
            )


        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            num1, num2 = generate_captcha(request)

            return render(
                request,
                'accounts/register.html',
                {
                    'num1': num1,
                    'num2': num2,
                    'old_username': username,
                    'old_email': email,
                }
            )

        # ==================================
        # CREATE USER
        # ==================================

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # ==================================
        # REMOVE CAPTCHA
        # ==================================

        request.session.pop(
            'captcha_answer',
            None
        )

        # ==================================
        # SUCCESS MESSAGE
        # ==================================

        messages.success(
            request,
            "Account created successfully. Please login."
        )

        return redirect('login')

    # ======================================
    # GET REQUEST
    # ======================================

    num1, num2 = generate_captcha(request)

    return render(
        request,
        'accounts/register.html',
        {
            'num1': num1,
            'num2': num2,
        }
    )


# ==========================================
# USER LOGIN
# ==========================================

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get(
            'username',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )

        captcha = request.POST.get(
            'captcha',
            ''
        ).strip()

        # ==================================
        # CAPTCHA CHECK
        # ==================================

        correct_answer = request.session.get(
            'captcha_answer'
        )

        if (
            correct_answer is None
            or not captcha.isdigit()
            or int(captcha) != correct_answer
        ):

            messages.error(
                request,
                "Incorrect CAPTCHA. Please solve it correctly."
            )

            num1, num2 = generate_captcha(request)

            return render(
                request,
                'accounts/login.html',
                {
                    'num1': num1,
                    'num2': num2,
                }
            )

        # ==================================
        # AUTHENTICATE USER
        # ==================================

        user = authenticate(
            request,
            username=username,
            password=password
        )

        # ==================================
        # LOGIN SUCCESS
        # ==================================

        if user is not None:

            login(
                request,
                user
            )

            # Remove CAPTCHA
            request.session.pop(
                'captcha_answer',
                None
            )

            return redirect(
                'home'
            )

        # ==================================
        # LOGIN FAILED
        # ==================================

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

            # Generate new CAPTCHA
            num1, num2 = generate_captcha(request)

            return render(
                request,
                'accounts/login.html',
                {
                    'num1': num1,
                    'num2': num2,
                }
            )

    # ======================================
    # GET REQUEST
    # ======================================

    num1, num2 = generate_captcha(request)

    return render(
        request,
        'accounts/login.html',
        {
            'num1': num1,
            'num2': num2,
        }
    )


# ==========================================
# USER LOGOUT
# ==========================================

def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect(
        'home'
    )


# ==========================================
# USER PROFILE
# ==========================================

def profile(request):

    if not request.user.is_authenticated:

        return redirect(
            'login'
        )

    user = request.user

    # ======================================
    # TOTAL ARTICLES
    # ======================================

    total_articles = Article.objects.filter(
        author=user
    ).count()

    # ======================================
    # PUBLISHED ARTICLES
    # ======================================

    published_articles = Article.objects.filter(
        author=user,
        status='published'
    ).count()

    # ======================================
    # DRAFT ARTICLES
    # ======================================

    draft_articles = Article.objects.filter(
        author=user,
        status='draft'
    ).count()

    # ======================================
    # TOTAL VIEWS
    # ======================================

    total_views = sum(
        Article.objects.filter(
            author=user
        ).values_list(
            'views',
            flat=True
        )
    )

    # ======================================
    # TOTAL COMMENTS WRITTEN
    # ======================================

    total_comments = Comment.objects.filter(
        user=user
    ).count()

    # ======================================
    # RENDER PROFILE
    # ======================================

    return render(
        request,
        'accounts/profile.html',
        {
            'profile_user': user,

            'total_articles':
                total_articles,

            'published_articles':
                published_articles,

            'draft_articles':
                draft_articles,

            'total_views':
                total_views,

            'total_comments':
                total_comments,
        }
    )


# ==========================================
# AUTHOR DASHBOARD
# ==========================================

def dashboard(request):

    if not request.user.is_authenticated:

        return redirect(
            'login'
        )

    user = request.user

    # ======================================
    # USER ARTICLES
    # ======================================

    articles = Article.objects.filter(
        author=user
    )

    # ======================================
    # TOTAL ARTICLES
    # ======================================

    total_articles = articles.count()

    # ======================================
    # PUBLISHED ARTICLES
    # ======================================

    published_articles = articles.filter(
        status='published'
    ).count()

    # ======================================
    # DRAFT ARTICLES
    # ======================================

    draft_articles = articles.filter(
        status='draft'
    ).count()

    # ======================================
    # TOTAL VIEWS
    # ======================================

    total_views = articles.aggregate(
        total=Sum('views')
    )['total'] or 0

    # ======================================
    # TOTAL LIKES
    # ======================================

    total_likes = Like.objects.filter(
        article__author=user
    ).count()

    # ======================================
    # TOTAL COMMENTS
    # ======================================

    total_comments = Comment.objects.filter(
        article__author=user
    ).count()

    # ======================================
    # TOTAL BOOKMARKS
    # ======================================

    total_bookmarks = Bookmark.objects.filter(
        article__author=user
    ).count()

    # ======================================
    # RECENT ARTICLES
    # ======================================

    recent_articles = articles.annotate(

        like_count=Count(
            'likes',
            distinct=True
        ),

        comment_count=Count(
            'comments',
            distinct=True
        ),

        bookmark_count=Count(
            'bookmarks',
            distinct=True
        )

    ).order_by(
        '-created_at'
    )[:5]

    # ======================================
    # RENDER DASHBOARD
    # ======================================

    return render(
        request,
        'accounts/dashboard.html',
        {
            'total_articles':
                total_articles,

            'published_articles':
                published_articles,

            'draft_articles':
                draft_articles,

            'total_views':
                total_views,

            'total_likes':
                total_likes,

            'total_comments':
                total_comments,

            'total_bookmarks':
                total_bookmarks,

            'recent_articles':
                recent_articles,
        }
    )


# ==========================================
# NOTIFICATIONS
# ==========================================

def notifications(request):

    if not request.user.is_authenticated:

        return redirect(
            'login'
        )

    # ======================================
    # ALL NOTIFICATIONS
    # ======================================

    notification_list = Notification.objects.filter(
        recipient=request.user
    ).select_related(
        'sender',
        'article'
    ).order_by(
        '-created_at'
    )

    # ======================================
    # UNREAD COUNT
    # ======================================

    unread_count = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()

    # ======================================
    # RENDER
    # ======================================

    return render(
        request,
        'accounts/notifications.html',
        {
            'notifications':
                notification_list,

            'unread_count':
                unread_count,
        }
    )


# ==========================================
# MARK SINGLE NOTIFICATION AS READ
# ==========================================

def mark_notification_read(
    request,
    notification_id
):

    if not request.user.is_authenticated:

        return redirect(
            'login'
        )

    notification = get_object_or_404(
        Notification,
        id=notification_id,
        recipient=request.user
    )

    notification.is_read = True

    notification.save(
        update_fields=[
            'is_read'
        ]
    )

    return redirect(
        'notifications'
    )


# ==========================================
# MARK ALL NOTIFICATIONS AS READ
# ==========================================

def mark_all_notifications_read(request):

    if not request.user.is_authenticated:

        return redirect(
            'login'
        )

    Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).update(
        is_read=True
    )

    return redirect(
        'notifications'
    )