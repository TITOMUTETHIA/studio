from django.http import HttpResponse

def product_list(request):
    return HttpResponse("This is the product list.")
