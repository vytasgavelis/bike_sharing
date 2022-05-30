import decimal
from decimal import Decimal

from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.views import View
from django.contrib import messages

class AddCreditsView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        form_data = request.POST
        credit_amount = form_data['credit_amount']

        try:
            credit_amount = Decimal(credit_amount)
        except decimal.InvalidOperation:
            messages.error(request, 'Credit amount must be a float number')
            return redirect('user_profile')

        if credit_amount <= 0:
            messages.error(request, 'Credit amount must be a positive number')
            return redirect('user_profile')

        credit_amount = round(credit_amount, 2)

        user = request.user
        user.userprofile.credits += credit_amount
        user.userprofile.save()

        messages.success(request, 'Credits have been added')
        return redirect('user_profile')