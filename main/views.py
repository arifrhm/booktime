from django.shortcuts import render
from django.views.generic.edit import FormView
from main import forms
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from main import models


# Create your views here.
def home(request):
    return render(request, "home.html", {})


class ContactUsView(FormView):
    template_name = "contact_form.html"
    form_class = forms.ContactForm
    success_url = "/"

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)


def contact_us(request):
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            form.send_mail()
            return HttpResponseRedirect('/')
        else:
            form = forms.ContactForm()
    return render(request, 'contact_form.html', {'form': form})


class ProductListView(ListView):
    template_name = "main/product_list.html"
    paginate_by = 4

    def get_queryset(self):
        tag = self.kwargs['tag']
        self.tag = None
        if tag != "all":
            self.tag = get_object_or_404(
                models.ProductTag, slug=tag
            )
        if self.tag:
            products = models.Product.objects.active().filter(
                tags=self.tag
            )
        else:
            products = models.Product.objects.active()
            return products.order_by("name")
