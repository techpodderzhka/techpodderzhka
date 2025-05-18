from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import FormSubmissionForm
from .models import Form, FormAssignment, Employee
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.db.models import OuterRef, Subquery, Q
from django.utils import timezone


# Create your views here.


def is_admin(user):
    return user.groups.filter(name="admin").exists()


def main(request):
    return render(request, "base.html")


def faq(request):
    return render(request, "faq.html")


def submit_form(request):
    categories = Form.objects.values_list("category", flat=True).distinct()
    if request.method == "POST":
        form = FormSubmissionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ваша заявка успешно отправлена.")

        else:
            messages.error(
                request,
                "Произошла ошибка при отправке заявки. Пожалуйста, проверьте форму.",
            )

    else:
        form = FormSubmissionForm()

    return render(request, "submit_form.html", {"form": form, "categories": categories})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("main")
        else:
            messages.error(request, "Неверное имя пользователя или пароль")
    return render(request, "login.html")


def logout_view():
    return redirect("login")


@login_required
@user_passes_test(is_admin)
def forms_list(request):
    latest_assignment = FormAssignment.objects.filter(form=OuterRef("pk")).order_by(
        "-assigned_at"
    )

    forms = Form.objects.all().annotate(
        assigned_employee_name=Subquery(latest_assignment.values("employee__name")[:1]),
        assigned_employee_surname=Subquery(
            latest_assignment.values("employee__surname")[:1]
        ),
        latest_assignment_status=Subquery(latest_assignment.values("status")[:1]),
        latest_assignment_finished_at=Subquery(
            latest_assignment.values("finished_at")[:1]
        ),
        latest_assignment_assigned_at=Subquery(
            latest_assignment.values("assigned_at")[:1]
        ),
    )

    context = {
        "forms": forms,
    }
    return render(request, "forms_list.html", context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name="admin").exists())
def form_detail_assign(request, form_id):
    form = get_object_or_404(Form, form_id=form_id)

    employees = Employee.objects.all()
    assignments = FormAssignment.objects.filter(form=form)

    if request.method == "POST":
        employee_id = request.POST.get("employee")
        if employee_id:
            employee = get_object_or_404(Employee, pk=employee_id)

            if FormAssignment.objects.filter(form=form, employee=employee).exists():
                messages.error(request, f"Форма уже назначена сотруднику {employee}.")
            else:
                FormAssignment.objects.create(
                    form=form, employee=employee, status="обрабатывается"
                )

                form.status = "обрабатывается"
                form.save()

                messages.success(request, f"Форма назначена сотруднику {employee}.")
                return redirect("forms_list")
        else:
            messages.error(request, "Пожалуйста, выберите сотрудника для назначения.")

    context = {
        "form": form,
        "employees": employees,
        "assignments": assignments,
    }
    return render(request, "form_detail_assign.html", context)


@login_required
def my_forms(request):
    employee = request.user
    try:
        employee_obj = employee.employee
    except:
        from .models import Employee

        employee_obj = Employee.objects.filter(username=employee.username).first()

    assignments = FormAssignment.objects.filter(employee=employee_obj).select_related(
        "form"
    )

    return render(request, "my_forms.html", {"assignments": assignments})


@login_required
def employee_form_detail(request, form_id):
    employee = get_object_or_404(Employee, username=request.user.username)

    assignment = get_object_or_404(
        FormAssignment, form__form_id=form_id, employee=employee
    )

    if request.method == "POST":
        assignment.status = "завершен"
        assignment.finished_at = timezone.now()
        assignment.save()

        form = assignment.form
        if not form.formassignment_set.filter(~Q(status="завершен")).exists():
            form.status = "завершен"
        elif form.formassignment_set.filter(status="обрабатывается").exists():
            form.status = "обрабатывается"
        else:
            form.status = "не назначен"
        form.save()

        messages.success(request, "Заявка успешно завершена.")
        return redirect("my_forms")

    form = assignment.form
    context = {
        "form": form,
        "assignment": assignment,
    }
    return render(request, "employee_form_detail.html", context)
