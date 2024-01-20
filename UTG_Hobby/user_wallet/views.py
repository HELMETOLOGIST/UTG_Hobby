from django.shortcuts import render,redirect,get_object_or_404
from user_authentication.models import CustomUser
from user_wallet.models import Wallet
from django.http import JsonResponse
import razorpay
from django.contrib.auth.decorators import login_required
from decimal import Decimal



# Create your views here.

@login_required
def wallett(request):
    email = request.user.email
    user = get_object_or_404(CustomUser, email=email)
    wallet = Wallet.objects.filter(user=user).order_by("-id")
    if wallet:
        balance_amount = wallet.first().balance_amount
    else:
        balance_amount = 0
    context = {
        'wallet': wallet,
        'balance_amount': balance_amount,
    }
    return render(request, 'wallet.html', context)

client = razorpay.Client(auth=("rzp_test_uVOZmd57SunofW","mfTY9FeuzBTeYGhZB0no3TRL"))


def add_to_wallett(request):
    amount = int(request.POST.get('amount'))
    data = {'amount':amount, 'currency':'INR'}
    payment = client.order.create(data=data)
    request.session['amount'] = amount
    return JsonResponse (
        {
            "success":True,
            "payment":payment,
            "amount":amount,
        }
    )


@login_required
def update_wallett(request):
    email = request.user.email
    amount = request.session["amount"]
    user = get_object_or_404(CustomUser, email=email)
    wallet = Wallet.objects.filter(user=user).order_by("-id").first()
    
    if not wallet:  # Check if wallet is None
        balance_amount = 0
    else:
        balance_amount = wallet.balance_amount

    balance = balance_amount + Decimal(amount)
    Wallet.objects.create(
        user=user,
        balance_amount=balance,
        transaction_type="Credit",
        transaction_details=f"Added Money through RazorPay",
        transaction_amount=amount,
    )
    return redirect('wallet')
