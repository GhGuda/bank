from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
import hashlib

# Create your views here.

def hash_input(input_value):
    return hashlib.sha256(input_value.encode()).hexdigest()


def login_view(request):
    if request.method == "POST":
        identifier = request.POST['username'].lower()
        password = request.POST['password'].lower()
        
        # hashed_identifier = hash_input(identifier)
        # hashed_password = hash_input(password)
        
        print(identifier)
        print(password)


        
        user = authenticate(request, username=identifier, password=password)

        if user is not None:
            login(request, user)
            return redirect('transactions')
        else:
            messages.error(request, 'Invalid credentials!')

    return render(request, "index.html")


def register(request):
    if request.method == "POST":
        fullname = request.POST['fullname'].lower()
        username = request.POST['username'].lower()
        email = request.POST['email'].lower()
        phone = request.POST['phone']
        password = request.POST['password'].lower()
        password2 = request.POST['password2'].lower()
        
        if password == password2:
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, 'Username taken try different one!')
                return redirect('register')
            elif CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'Email taken try different one!')
                return redirect('register')
            else:
                user = CustomUser.objects.create_user(
                    fullname=fullname,
                    username=username,
                    email=email,
                    phone=phone,
                    password=password,
                )
                user.save()
                messages.success(request, 'Account created successfully!')
                return redirect(login)
        else:
            messages.error(request, "Password did not match!")
            return redirect('register')
            
    return render(request, "register.html")



@login_required(login_url="/")
def transactions(request):
    user_active = CustomUser.objects.get(username=request.user)
    transactions = Transactions.objects.filter(user=user_active)
    
    
    if request.method == 'POST':
        try:
            transactionType = request.POST.get('transactionTypes')
            withdrawalAmoun = request.POST.get('withdrawalAmount')
            topupAmount = request.POST.get('topupAmount')
            savingsAmount = request.POST.get('savingsAmount')
            accounttype = request.POST.get('accounttype')
            

            if not transactionType:
                messages.error(request, "Transaction type is required!")
                return redirect('transactions')
            
            elif transactionType == "withdrawal":
                if accounttype == "Banking Account":
                    try:
                        withdrawalAmoun = float(withdrawalAmoun)
                    except ValueError:
                        messages.error(request, 'Invalid withdrawal amount. Please enter a valid number.')
                        return redirect('transactions')
                    
                    if user_active.current_amount < withdrawalAmoun:
                        messages.error(request, f'You have insufficient balance in your banking account.')
                        return redirect("transactions")
                    else:
                        user_active.current_amount = user_active.current_amount - withdrawalAmoun
                        user_active.save()
                        accounttype = "Banking Account"
                        trans = Transactions.objects.create(
                            user=user_active,
                            transaction_type=transactionType,
                            amount=withdrawalAmoun,
                            account_type=accounttype
                        )
                        trans.save()
                        messages.success(request, f'You have sucessfully withdraw ¢{withdrawalAmoun} from your banking account.')
                        return redirect("transactions")
                elif accounttype == "Savings Account":
                    accounttype = "Savings Account"
                    try:
                        withdrawalAmoun = float(withdrawalAmoun)
                    except ValueError:
                        messages.error(request, 'Invalid withdrawal amount. Please enter a valid number.')
                        return redirect('transactions')
                    
                    if user_active.savings_amount < withdrawalAmoun:
                        messages.error(request, f'You have insufficient balance in your savings account.')
                        return redirect("transactions")
                    else:
                        user_active.savings_amount = user_active.savings_amount - withdrawalAmoun
                        user_active.save()
                        trans = Transactions.objects.create(
                            user=user_active,
                            transaction_type=transactionType,
                            amount=withdrawalAmoun,
                            account_type=accounttype
                        )
                        trans.save()
                        messages.success(request, f'You have sucessfully withdraw ¢{withdrawalAmoun} from your savings account.')
                        return redirect("transactions")
            
            elif transactionType == "topup":
                transactionT = "Top Up Banking Account"
                accounttype = "Banking  Account"

                try:
                    topupAmount = float(topupAmount)
                except ValueError:
                    messages.error(request, 'An error occurred, Please enter a valid number.')
                    return redirect('transactions')
                user_active.current_amount = user_active.current_amount + topupAmount
                user_active.save()
                trans = Transactions.objects.create(
                    user=user_active,
                    transaction_type=transactionT,
                    amount=topupAmount,
                    account_type=accounttype
                )
                trans.save()
                messages.success(request, f'You have sucessfully top up an amount of ¢{topupAmount} to your normal account.')
                return redirect("transactions")
            
            elif transactionType == "savings":
                accounttype = "Savings Account"
                transactionType = "Top Up Savings Account"
                
                
                if not savingsAmount:
                    messages.error(request, 'Please enter an amount to save.')
                    return redirect('transactions')
                
                    
                try:
                    savingsAmount = float(savingsAmount)
                except ValueError:
                    messages.error(request, 'An error occurred. Please enter a valid number.')
                    return redirect('transactions')
                
                if user_active.savings_amount + float(savingsAmount) <= 10000:
                    user_active.savings_amount = user_active.savings_amount + savingsAmount
                    user_active.save()
                    
                    trans = Transactions.objects.create(
                    user=user_active,
                    transaction_type=transactionType,
                    amount=savingsAmount,
                    account_type=accounttype
                    )
                    trans.save()
                    messages.success(request, f'You have successfully saved an amount of ¢{savingsAmount} to your savings account.')
                    return redirect('transactions')
                
                else:
                    messages.error(request, f"¢10000.0 is the maximum savings amount, ¢{savingsAmount} can't be added.")
                    return redirect('transactions')
            
        except Exception as e:
            messages.error(request, f"An error occured, {e}")   
        
        
    
    
    context={
        'user':user_active,
        'transactions':transactions,
    }
    return render(request, 'transaction.html',context)