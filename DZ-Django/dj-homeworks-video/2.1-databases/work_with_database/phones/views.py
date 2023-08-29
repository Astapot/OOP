from django.shortcuts import render, redirect
from phones.models import Phone

def index(request):
    return redirect('catalog')


def show_catalog(request):
    sort = request.GET.get('sort')
    template = 'catalog.html'
    phones = Phone.objects.all()
    if sort == 'min_price':
        phones = Phone.objects.order_by('price')
    elif sort == 'name':
        phones = Phone.objects.order_by('name')
    elif sort == 'max_price':
        phones = Phone.objects.order_by('-price')
    else:
        phones = Phone.objects.all()
    print(phones)
    print(phones[1].name)
    context = {'phones': phones}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.filter(slug=slug)
    context = {'phone': phone[0]}
    return render(request, template, context)
