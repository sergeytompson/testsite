from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import FormMixin, ModelFormMixin
from .models import News, Category, Comments
from .forms import NewsFormFromModel, CommentForm
from django.urls import reverse


# TODO придерживайся нэйминга что то вроде NewsListView
class NewsBand(ListView):
    model = News
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        return context

    def get_queryset(self):
        return News.objects.filter(is_publish=True)


# TODO CategoryListView
class CategoryBand(ListView):
    model = News
    context_object_name = 'news'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_publish=True)


# TODO CategoryDetailView
class ViewNews(FormMixin, DetailView):
    model = News
    form_class = CommentForm

    # pk_url_kwarg = 'news_id'

    # TODO можно создать в модели функцию get_absolute_url
    def get_success_url(self):
        return reverse('news', kwargs={'pk': self.object.pk})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO вместо явного указания comments в контексте можно использовать news.comment_set.all
        #  и тогда нужда в функции исчезнет
        context['comments'] = Comments.objects.filter(news=self.object.pk)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.news = News.objects.get(pk=kwargs['pk'])
            new_comment.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)


# TODO NewsCreateView
class CreateNews(CreateView):
    form_class = NewsFormFromModel
    # TODO обрати внимание, что update и create по умолчанию используют шаблон
    #  {model_name}_form.html, здесь будет news_form.html
    #  проверить это пустая форма или нет можно прямо в шаблоне
    #  form.instance.pk
    #  так же в переменной класса fields можно указать нужные для рендера поля
    template_name = 'news/add_news.html'
    # success_url = reverse_lazy('home')


class UpdateNews(UpdateView):
    form_class = NewsFormFromModel
    template_name = 'news/upd_news.html'

    def get_success_url(self):
        return reverse('news', kwargs={'pk': self.object.pk})

    # TODO обрати внимание, что можно заменить на queryset = News.objects.all()
    #  проще делать так, если в кверисете не нужны атрибуты self
    def get_queryset(self):
        return News.objects.all()

# def index(request):
#     news = News.objects.all()
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#     }
#     return render(request, 'news/index.html', context)
#
#
# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     context = {
#         'news': news,
#         'category': category
#     }
#     return render(request, 'news/category.html', context)
#
#
# def get_news(request, news_id):
#     # req_news = News.objects.get(pk=news_id)
#     req_news = get_object_or_404(News, pk=news_id)
#     context = {
#         'news': req_news
#     }
#     return render(request, 'news/news.html', context)
#
#
# def add_news(request):
#     if request.method == 'POST':
#         form = NewsFormFromModel(request.POST)
#         if form.is_valid():
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsFormFromModel()
#     return render(request, 'news/add_news.html', {'form': form})
