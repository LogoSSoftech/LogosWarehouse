from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from core.models import User, CoreCompanies
from core.forms import UserForm, CoreCompanyForm, RestorePasswordForm
from core import functions
from apps.warehouse.models import StockMove

#  --------------------------HOME-----------------------------#


class dashboard(LoginRequiredMixin, TemplateView):

    template_name = 'dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_moves_year_month(self):
        moves_qty = []
        try:
            year = datetime.now().year
            for month in range(1, 13):
                moves = StockMove.objects.filter(
                    date__year=year, date__month=month)
                moves_qty.append(len(moves))
        except:
            pass
        return moves_qty

    def get_context_data(self, **kwargs):
        total_year_moves = 0
        for item in self.get_moves_year_month():
            total_year_moves += item
        context = super().get_context_data(**kwargs)
        context['year'] = datetime.now().year
        context['moves_year_month'] = self.get_moves_year_month()
        context['total_year_moves'] = total_year_moves

        return context

#  ---------------------------LOGIN---------------------------#


class Login(LoginView):
    template_name = 'login/views/login.html'

    def get_company(self):
        company = False
        if len(CoreCompanies.objects.all()) > 0:
            company = True

        return company

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.get_company()
        return context


class RestorePassword(TemplateView):

    template_name = 'login/views/RestorePassword.html'
    form_class = RestorePasswordForm
    success_url = reverse_lazy('login')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'restore_password'
        context['form'] = self.form_class
        context['success_url'] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        if action == 'restore_password':
            user = functions.restore_password(request)
            if not user:
                return redirect('RestorePassword')
            else:
                return redirect(self.success_url)



#  ---------------------------USER MODEL---------------------------#
# ------------------------VIEWS------------------------------#


class ListUser(LoginRequiredMixin, ListView):

    model = User
    template_name = 'users/views/ListUser.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        create_forms = {
            'form1': {'button_create': reverse_lazy('CreateUser'),
                      'text': 'Crear Nuevo Usuario'},
        }
        context['create_forms'] = create_forms
        return context


class DetailUser(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/views/DetailUser.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.model.objects.get(pk=self.kwargs.get('pk'))
        heading = 'Detalle %s %s' % (user_id.first_name, user_id.last_name)
        context['heading'] = heading
        return context
# ------------------------FUNCTIONS------------------------------#


class CreateUser(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'users/functions/CreateUser.html'
    success_url = reverse_lazy('ListUser')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'
        context['success_url'] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'create':
                form = self.get_form()
                data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

# ------------------------FUNCTIONS------------------------------#


class EditUser(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/functions/CreateUser.html'
    success_url = reverse_lazy('ListUser')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'edit'
        context['success_url'] = self.success_url
        return context

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


class DeleteUser(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/functions/DeleteUser.html'
    success_url = reverse_lazy('ListUser')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

#  ---------------------------CORE COMPANY MODEL---------------------------#

# ------------------------VIEWS------------------------------#


class ListCompany(LoginRequiredMixin, ListView):

    model = CoreCompanies
    template_name = 'company/views/ListCompany.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = self.request.user.company_id.name
        return context


class DetailCompany(LoginRequiredMixin, DetailView):
    model = CoreCompanies
    template_name = 'company/views/DetailCompany.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company_id = self.model.objects.get(pk=self.kwargs.get('pk'))
        heading = 'Detalle %s ' % (company_id.name)
        context['heading'] = heading
        return context

# ------------------------FUNCTIONS------------------------------#


class CreateCompany(CreateView):
    model = CoreCompanies
    form_class = CoreCompanyForm
    template_name = 'company/functions/CreateCompany.html'
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'
        context['success_url'] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'create':
                form = self.get_form()
                if form.is_valid():
                    company_form = form.save(commit=False)
                    fields = {
                        'user_image': company_form.company_image,
                        'first_name': company_form.name,
                        # 'last_name': company_form.short,
                    }
                    form.save()
                    User.objects.create_superuser(
                        company_form.name, company_form.email,
                        password=company_form.rif, **fields)
                else:
                    data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


class EditCompany(LoginRequiredMixin, UpdateView):
    model = CoreCompanies
    form_class = CoreCompanyForm
    template_name = 'company/functions/EditCompany.html'
    success_url = reverse_lazy('ListCompany')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'edit'
        context['success_url'] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'create':
                form = self.get_form()
                if form.is_valid():
                    form.save()
                else:
                    data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
