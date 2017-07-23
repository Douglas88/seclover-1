from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from rest_framework import permissions
from rest_framework import mixins
from rest_framework import generics
from django.views.generic import TemplateView
from .permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer


class IndexTemplateView(TemplateView):
    '''
    www.seclover.com 主页
    '''

    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexTemplateView, self).get_context_data(**kwargs)
        context['title'] = 'Welcome to seclover.com'
        return context


def register(request):
    '''
    用户注册
    '''
    if request.method == "POST":
        user = User()
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.username = request.POST['username']
        username = request.POST['username']
        user.email = request.POST['email']
        email = request.POST['email']
        user.password = request.POST['password']
        password = request.POST['password']
        user.set_password(request.POST['password'])
        if not User.objects.filter(email=email).exists():
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    request.session['username'] = username
                    password = request.POST['password']
                    request.session['password'] = password
                    return redirect('/index/')
        else:
            error = {'error': 'email address already exists, please sign up with another one!'}
            return render(request, 'register.html', error)
    return render(request, 'register.html')


def log_in(request):
    '''
    用户登录
    '''
    if request.session.has_key('username'):
        username = request.session['username']
        return render(request, 'loggedin.html', {"username": username})
    elif request.method == "POST":
        username = request.POST['username']
        request.session['username'] = username
        password = request.POST['password']
        request.session['password'] = password
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/index/')
            else:
                return render(request, 'login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login'})
    return render(request, 'login.html')


def log_out(request):
    '''
    登出
    '''

    try:
        del request.session['username']
    except:
        pass
    logout(request)
    return redirect('/index/')


#通过rest framework mixins 实现增删改查

class PostList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

