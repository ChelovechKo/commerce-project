from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup_view, name="signup"),
    path("categories/", views.categories_view, name="categories"),
    path("categories/<int:category_id>/", views.categories_view, name="filtered_category"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("create_listing", views.create_listing_view, name="create_listing"),
    path("listing/<int:listing_id>/", views.listing_page_view, name="listing_page"),
    path("listing/<int:listing_id>/add_to_watchlist/", views.add_to_watchlist_view, name="add_to_watchlist"),
    path("listing/<int:listing_id>/remove_from_watchlist/", views.remove_from_watchlist_view, name="remove_from_watchlist"),
    path('listing/<int:listing_id>/add_comment/', views.add_comment_view, name='add_comment'),
    path('listing/<int:listing_id>/close/', views.close_auction_view, name='close_auction'),
    path('expand_description/<int:listing_id>/', views.expand_description_view, name='expand_description'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
