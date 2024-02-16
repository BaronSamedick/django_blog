from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from .forms import ProfileUpdateForm, UserLoginForm, UserPasswordChangeForm, UserRegisterForm, UserUpdateForm
from .models import Profile


class ProfileDetailView(DetailView):
    """
    Представление для просмотра профиля
    """

    model = Profile
    context_object_name = "profile"
    template_name = "user/profile_detail.html"
    queryset = model.objects.all().select_related("user")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Страница пользователя: {self.object.user.username}"
        return context


class ProfileUpdateView(UpdateView):
    """
    Представление для редактирования профиля
    """

    model = Profile
    form_class = ProfileUpdateForm
    template_name = "user/profile_edit.html"

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Редактирование профиля пользователя: {self.request.user.username}"
        if self.request.POST:
            context["user_form"] = UserUpdateForm(self.request.POST, instance=self.request.user)
        else:
            context["user_form"] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context["user_form"]
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
            else:
                context.update({"user_form": user_form})
                return self.render_to_response(context)
        return super().form_valid(form)


class UserRegisterView(SuccessMessageMixin, CreateView):
    """
    Представление регистрации на сайте с формой регистрации
    """

    form_class = UserRegisterForm
    success_url = reverse_lazy("home")
    template_name = "user/user_register.html"
    success_message = "Вы успешно зарегистрировались. Можете войти на сайт!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация на сайте"
        return context


class UserLoginView(SuccessMessageMixin, LoginView):
    """
    Авторизация на сайте
    """

    form_class = UserLoginForm
    template_name = "user/user_login.html"
    next_page = "home"
    success_message = "Добро пожаловать на сайт!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Авторизация на сайте"
        return context


class UserLogoutView(LogoutView):
    """
    Выход с сайта
    """

    next_page = "home"


class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    """
    Изменение пароля пользователя
    """

    form_class = UserPasswordChangeForm
    template_name = "user/user_password_change.html"
    success_message = "Ваш пароль был успешно изменён!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Изменение пароля на сайте"
        return context

    def get_success_url(self):
        return reverse_lazy("profile_detail", kwargs={"slug": self.request.user.profile.slug})
