from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def render_index_page(request):
    return render(request, 'index.html')

@login_required(login_url='/auth/login/')
def render_lk_page(request):
    template = 'lk.html'
    # template = 'lk-order.html'
    return render(request, template)
