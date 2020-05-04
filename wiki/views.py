from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView


from wiki.models import Page
from .forms import PageForm



class PageListView(ListView):
    """ Renders a list of all Pages. """
    model = Page

    def get(self, request):
        """ GET a list of Pages. """
        pages = self.get_queryset().all()
        return render(request, 'list.html', {
          'pages': pages
        })

class PageDetailView(DetailView):
    """ Renders a specific page based on it's slug."""
    model = Page

    def get(self, request, slug):
        """ Returns a specific wiki page by slug. """
        page = self.get_queryset().get(slug__iexact=slug)
        return render(request, 'page.html', {
          'page': page
        })

class PageCreateView(CreateView):
    def get(self, request, *args, **kwargs):
      context = {'form': PageForm()}
      return render(request, 'create_page.html', context)

    def post(self, request, *args, **kwargs):
      form = PageForm(request.POST)
      if form.is_valid():
          wiki = form.save()
          wiki.save()
          return HttpResponseRedirect(reverse_lazy('wiki-details-page', args=[wiki.slug]))
      return render(request, 'create_page.html', {'form': form})


def PageEdit(request, slug):
    page = get_object_or_404(Page, slug=slug)
    form = PageForm(request.POST, instance=page)  
    if request.method == "POST":
        if form.is_valid():
            page = form.save(commit=False)
            page.save()
            return HttpResponseRedirect(reverse_lazy('wiki-details-page', args=[page.slug]))
        else:
            form = PostForm(instance=page)
    return render(request, 'create_page.html', {'form': form})

