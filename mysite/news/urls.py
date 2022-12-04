from django.urls import path
from .views import *

urlpatterns = [
    # path('', index, name='home'),
    path('', NewsBand.as_view(), name='home'),
    path('news', NewsBand.as_view()),
    path('news/<int:pk>', ViewNews.as_view(), name='news'),
    path('news/<int:pk>/upd', UpdateNews.as_view(), name='upd_news'),
    path('category/<int:category_id>/', CategoryBand.as_view(), name='category'),
    path('news/add-news/', CreateNews.as_view(), name='add_news')
]
