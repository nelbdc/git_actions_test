from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import CompanySerializers
from .models import Company
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail


def fibonacci_dynamic(n):
    fib_list = [0, 1]
    for i in range(n + 1):
        fib_list.append(fib_list[i] + fib_list[i + 1])
    return fib_list[n]


class CompanyView(ModelViewSet):
    serializer_class = CompanySerializers
    queryset = Company.objects.all().order_by("-last_update")
    pagination_class = PageNumberPagination


@api_view(http_method_names=["POST"])
def send_company_email(request):
    subject = request.data.get("data", None)
    message = request.data.get("message", None)

    send_mail(
        subject=subject,
        message=message,
        from_email="egresados398@gmail.com",
        recipient_list=["njborrego@uniguajira.edu.co"],
    )

    return Response(
        {
            "status": "success",
            "info": "email sent successfully",
        },
        status=200,
    )


@api_view(http_method_names=["POST"])
def fibonacci_url_test(request):
    number = request.data.get("number", None)

    if type(number) == type("") and not number.isdigit():
        return Response(
            {"status": "failed", "info": "The number should be a digit"}, status=404
        )

    number = int(number)
    if number < 0:
        return Response(
            {"status": "failed", "info": "The number should be a digit more than 0"},
            status=404,
        )

    rest = fibonacci_dynamic(number)
    return Response({"status": "success", "info": rest}, status=200)
