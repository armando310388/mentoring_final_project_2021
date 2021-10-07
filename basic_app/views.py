from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from basic_app.models import News
from django.views.generic.base import RedirectView

# Create your views here.

class NewsListView(ListView):
    '''List all news in inverse chronological order'''
    model = News
    paginate_by = 10
    template_name = 'home.html'

    def get_queryset(self):
        return News.objects.order_by('-creation_time')


class NewCounterRedirectView(RedirectView):
    '''Manage the redirection for counting the clicks'''
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        single_new = get_object_or_404(News, pk=kwargs['pk'])
        single_new.update_counter()
        return single_new.url