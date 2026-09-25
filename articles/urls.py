from django.urls import path
from . import views


urlpatterns = [

    # ARTICLE LIST

    path(
        '',
        views.article_list,
        name='article_list'
    ),


    # CREATE ARTICLE

    path(
        'create/',
        views.create_article,
        name='create_article'
    ),


    # MY ARTICLES

    path(
        'my-articles/',
        views.my_articles,
        name='my_articles'
    ),


    # MY BOOKMARKS

    path(
        'my-bookmarks/',
        views.my_bookmarks,
        name='my_bookmarks'
    ),


    # LIKE / UNLIKE ARTICLE

    path(
        'like/<slug:slug>/',
        views.like_article,
        name='like_article'
    ),


    # BOOKMARK / REMOVE BOOKMARK

    path(
        'bookmark/<slug:slug>/',
        views.bookmark_article,
        name='bookmark_article'
    ),


    # EDIT ARTICLE

    path(
        'edit/<slug:slug>/',
        views.edit_article,
        name='edit_article'
    ),


    # DELETE ARTICLE

    path(
        'delete/<slug:slug>/',
        views.delete_article,
        name='delete_article'
    ),


    # CATEGORY ARTICLES

    path(
        'category/<slug:slug>/',
        views.category_articles,
        name='category_articles'
    ),


    # EDIT COMMENT

    path(
        'comment/<int:comment_id>/edit/',
        views.edit_comment,
        name='edit_comment'
    ),


    # DELETE COMMENT

    path(
        'comment/<int:comment_id>/delete/',
        views.delete_comment,
        name='delete_comment'
    ),


    # ARTICLE DETAIL
    # Keep this at the end

    path(
        '<slug:slug>/',
        views.article_detail,
        name='article_detail'
    ),

]