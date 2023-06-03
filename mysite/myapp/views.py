from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, JsonResponse
from django.urls import reverse_lazy, reverse

from .models import Product, OrderDetail
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import stripe

# сделано через калассы
# def index(request):
#     items = Product.objects.all()
#     item_name = request.GET.get('search')
#     if item_name != '' and item_name is not None:
#         items = items.filter(name__icontains=item_name)
#
#     context = {
#         'items': items,
#         'item_name': item_name
#     }
#     return render(request, "myapp/index.html", context)


class ProductListView(ListView):
    model = Product
    template_name = 'myapp/index.html'
    context_object_name = 'items'
    paginate_by = 3


    # поиск по продуктам
    def get_queryset(self):
        search_item = self.request.GET.get('search')
        if search_item != '' and search_item is not None:
            item_name = Product.objects.filter(name__icontains=search_item)
            return item_name
        else:
            items = Product.objects.all()
            return items







# сделано через калассы
# def indexItem(request, my_id):
#     item = Product.objects.get(id=my_id)
#     context = {
#         'item': item
#     }
#     return render(request, "myapp/detail.html", context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'myapp/detail.html'
    context_object_name = 'item'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['stripe_publishable'] = settings.STRIPE_PUBLISHABLE_KEY
        return context




@login_required
def add_item(request):
    """Добавление продукта(item)"""
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES['upload']
        # получаем кто добавил товар
        seller = request.user
        item = Product(name=name, price=price, description=description, image=image, seller=seller)
        item.save()
    return render(request, "myapp/add_item.html")


def update_item(request, my_id):
    """Изменение продукта(item)"""
    item = Product.objects.get(id=my_id)
    if request.method == "POST":
        # перезаписываем данные в базе данных на новые
        item.name = request.POST.get('name')
        item.price = request.POST.get('price')
        item.description = request.POST.get('description')
        item.image = request.FILES.get('upload', item.image)
        item.save()
        return redirect('/myapp/')
    context = {
        'item': item
    }

    return render(request, "myapp/update_item.html", context)

# сделано через калассы
# def delete_item(request, my_id):
#     """Удаление продукта(item)"""
#     item = Product.objects.get(id=my_id)
#     if request.method == "POST":
#         item.delete()
#         return redirect('/myapp/')
#     context = {
#         'item': item
#     }
#
#     return render(request, "myapp/delete_item.html", context)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('myapp:index')


@csrf_exempt
def create_checkout_session(request, id):
    product = get_object_or_404(Product, pk=id)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": product.name,
                    },
                    "unit_amount": int(product.price * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=request.build_absolute_uri(reverse("myapp:success"))
        + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse("myapp:failed")),
    )

    # OrderDetail.objects.create(
    #     customer_email=email,
    #     product=product, ......
    # )

    order = OrderDetail()
    order.product = product
    order.stripe_payment_intent = checkout_session["payment_intent"]
    order.amount = int(product.price * 100)
    order.save()

    # return JsonResponse({'data': checkout_session})
    return JsonResponse({"sessionId": checkout_session.id})
