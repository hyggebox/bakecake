from django.shortcuts import render


def render_index_page(request):
    return render(request, 'index.html')


def render_lk_page(request):
    template = 'lk.html'
    # template = 'lk-order.html'
    return render(request, template)
