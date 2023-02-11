from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *
from .utils import *



class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Women.objects.filter(is_published=True)


# def index(request):
#     posts = Women.objects.all()
#
#     context = {
#         'posts': posts,
#         "menu": menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#     return render(request, 'women/index.html', context=context)


def about(request):
    return render(request, 'women/about.html', {"menu": menu, 'title': 'О сайте'})




class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForms
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))




# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForms(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForms()
#     return render(request, 'women/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})


# def contact(request):
#     return HttpResponse(f'<h1> Обратная связь</h1>')

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')



class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))




# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#     return render(request, 'women/post.html', context=context)


class WomenCategory(DataMixin, ListView):
    model = Category
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория -' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))

# def show_category(request, cat_id):
#     posts = Women.objects.filter(cat_id=cat_id)
#
#     context = {
#         'posts': posts,
#         "menu": menu,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat_id,
#     }
#     return render(request, 'women/index.html', context=context)

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

# При регистрации сразу авторизовываем
    def form_valid(self, form):
        user = form.save()
        login(self.request,user)
        return redirect('home')



# def login(request):
#     return HttpResponse('Авторизация')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))
    def get_success_url(self):
        return reverse_lazy('home')


# выход с сайта
def logout_user(request):
    logout(request)
    return redirect('login')