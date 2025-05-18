"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from main import views
from django.contrib.auth import views as auth_views


app_name = "main"


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.submit_form, name="main"),
    path("login/", views.login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="main"), name="logout"),
    path("faq/", views.faq, name="faq"),
    path("my_forms/", views.my_forms, name="my_forms"),
    path("forms_list", views.forms_list, name="forms_list"),
    path(
        "forms_list/<int:form_id>/", views.form_detail_assign, name="form_detail_assign"
    ),
    path("faq/", views.faq, name="faq"),
    path(
        "my_forms/<int:form_id>/",
        views.employee_form_detail,
        name="employee_form_detail",
    ),
]
