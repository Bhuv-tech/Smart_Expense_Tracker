from django.shortcuts import render
from .models import Expense
from .forms import ExpenseForm
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.utils.timezone import now
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from .ml import predict_next_month


# Create your views here.
@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'expenses/expense_list.html', {
        'expenses': expenses
    })

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()

    return render(request, 'expenses/expense_form.html', {
        'form': form
    })

def edit_expense(request, id):
    expense = get_object_or_404(Expense, id=id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'expenses/expense_form.html', {
        'form': form
    })

def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id)
    expense.delete()
    return redirect('expense_list')
   
def monthly_summary(request):
    current_month = now().month
    current_year = now().year

    monthly_total = Expense.objects.filter(
        date__month=current_month,
        date__year=current_year
    ).aggregate(total=Sum('amount'))

    month_expenses = Expense.objects.filter(
        date__year=current_year
    ).values('date__month').annotate(
        total=Sum('amount')
    ).order_by('date__month')

    return render(request, 'expenses/monthly_summary.html', {
        'monthly_total': monthly_total['total'],
        'month_expenses': month_expenses
    })

def category_summary(request):
    category_expenses = Expense.objects.values('category').annotate(
        total=Sum('amount')
    ).order_by('-total')

    return render(request, 'expenses/category_summary.html', {
        'category_expenses': category_expenses
    })

def charts_view(request):
    category_data = Expense.objects.values('category').annotate(
        total=Sum('amount')
    )

    monthly_data = Expense.objects.values('date__month').annotate(
        total=Sum('amount')
    ).order_by('date__month')

    categories = []
    category_totals = []

    for item in category_data:
        categories.append(item['category'])
        category_totals.append(float(item['total']))

    months = []
    month_totals = []

    for item in monthly_data:
        months.append(item['date__month'])
        month_totals.append(float(item['total']))

    context = {
        'categories': json.dumps(categories),
        'category_totals': json.dumps(category_totals),
        'months': json.dumps(months),
        'month_totals': json.dumps(month_totals),
    }

    return render(request, 'expenses/charts.html', context)


def logout_view(request):
    """Log out the user and redirect to the expense list (which will redirect to login if needed)."""
    logout(request)
    return redirect('expense_list')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('expense_list')
    else:
        form = UserCreationForm()

    return render(request, 'expenses/signup.html', {
        'form': form
    })

@login_required
def predict_expense(request):
    data = Expense.objects.filter(
        user=request.user
    ).values('date__month').annotate(
        total=Sum('amount')
    ).order_by('date__month')

    months = [item['date__month'] for item in data]
    totals = [float(item['total']) for item in data]

    prediction = None
    if len(months) >= 2:  # minimum data for ML
        prediction = predict_next_month(months, totals)

    return render(request, 'expenses/predict.html', {
        'prediction': prediction
    })