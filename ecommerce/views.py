from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#from .ml.model import recommend_product, get_customer_ids
from .ml.model import get_customer_ids
from .recommendation import recommend_product_full
from .models import Recommendation
from .utils import get_product_image


def home(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    recommendation = None
    similar_products = []
    also_bought = []
    selected_customer = None
    customers = get_customer_ids()
    history = None
    product_images = {}

    if request.method == 'POST':
        selected_customer = request.POST.get('customer_id')
        if selected_customer:
            recommendation, similar_products, also_bought = recommend_product_full(selected_customer)

            # Save recommendation
            if recommendation:
                Recommendation.objects.create(
                    user=request.user,
                    customer_id=selected_customer,
                    product=recommendation
                )

            # 🔍 Get images for each product
            all_products = [recommendation] + similar_products + also_bought
            for product in all_products:
                if product:  # avoid None
                    product_images[product] = get_product_image(product)

    if selected_customer:
        history_qs = Recommendation.objects.filter(
            user=request.user,
            customer_id=selected_customer
        ).order_by('-timestamp')

        seen = set()
        history = []
        for rec in history_qs:
            if rec.product not in seen:
                history.append(rec)
                seen.add(rec.product)
            if len(history) >= 10:
                break

    return render(request, 'dashboard.html', {
        'customers': customers,
        'recommendation': recommendation,
        'selected_customer': selected_customer,
        'history': history,
        'similar_products': similar_products,
        'also_bought': also_bought,
        'product_images': product_images,  # send to template
    })


