from django.contrib.messages.api import error
from django.shortcuts import render, redirect,reverse
from . models import Comment, Favourite, Like, Post, Category, Profile, Like, Dislike
from django.core.exceptions import ValidationError

from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from .forms import RegisterForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Главная страница
def index(request):
    # Все обьекты поста
    posts = Post.objects.all()
    return render(request, 'blog/index.html', {'posts':posts})


# Категории
def category(request):
    # Все обьекты категории
    categories = Category.objects.all()
    return render(request, 'blog/category.html', {'categories':categories})


# Уникальная категория
def category_detail(request, id):
    # Нашли категорию по id
    category = Category.objects.get(id = id)
    return render(request, 'blog/category-detail.html', {'category':category})


# Уникальный пост
def post_detail(request, id):
    # Нашли пост по id
    post = Post.objects.get(id = id)
    # # Все обьекты коммента
    comments = Comment.objects.order_by('-id')

    status = False

    if post.post_favourites.filter(user=request.user).filter(post=post).exists():
        status = True

    return render(request, 'blog/post-detail.html', {'post':post,'status':status, 'comments':comments})


# Создаем коммент
def comment(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Данный зареганный юзер
            user = request.user
            # Нашли пост по id
            post = Post.objects.get(id=id)
            # Коммент который написали в textarea и получаем его содержимое через name
            text = request.POST.get('text')
            # Создаем новый пустой обьект коммента
            comment = Comment()
            # Заполняем
            comment.user = user
            comment.post = post
            comment.text = text
            # Сохраняем
            comment.save()
            # reverse - перебрасывает на другую функцию вместе с аргументами
            return redirect(reverse('post_detail', kwargs={'id':post.id}))
    else:
        # redirect - пебеброска на другую функцию без аогументов
        return redirect('index')



# Удаляем коммент
def remove_comment(request, id):
    if request.user.is_authenticated:
        # Находим коммент по id
        comment = Comment.objects.get(id=id)
        # Берем id поста для переброски на данную уникальную страницу
        postId = comment.post.id
        # Удаляем
        comment.delete()
        # kwargs - передаем id для перехода в функцию которая принимает аргумент
        return redirect(reverse('post_detail', kwargs={'id':postId}))
    else:
        return redirect('index')

# Профайл

# Главная страница
def profile_index(request):
    if request.user.is_authenticated:
        return render(request, 'profile/index.html')
    else:
        return redirect('index')


# Данные профайла
def profile_data(request):
    if request.user.is_authenticated:
        # Находим профайла через юзера
        profile = Profile.objects.get(user = request.user)
        return render(request, 'profile/profile-data.html', {'profile':profile})
    else:
        return redirect('index')



# Редактирование данных профайла
def profile_data_edit(request):
    if request.user.is_authenticated:
        # Находим профайл для изменения его содержимого
        profile = Profile.objects.get(user = request.user)
        if request.method == 'POST':
            # Находим юзера и меняем его содержимое
            user = request.user
            user.username = request.POST.get('username')
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            # Сохраняем юзера
            user.save()

            # Сохраняем профайла который привязан к юзеру
            profile.date = request.POST.get('date')
            profile.save()

            return redirect('profile_data')

        else:
            return render(request, 'profile/profile-data-edit.html', {'profile':profile})
    else:
        return redirect('index')


def profile_favourite(request):
    if request.user.is_authenticated:
        user = request.user
        favourites = user.user_favourites.all()
        return render(request, 'profile/favourite.html',{'favourites':favourites})
    else:
        return redirect('index')
  
def likePages(request):
    if request.user.is_authenticated:
        user = request.user
        likes = user.user_favourites.all()
        return render(request, 'profile/likePage.html',{'likes':likes})
    else:
        return redirect('index')
  

# Админ панель


# Главная страница админа
def profile_admin1(request):
    return render(request, 'admin/index.html')


# Все категории
def categories(request):
    # Все обьекты категории
    categories = Category.objects.all()
    return render(request, 'admin/allcategory.html', {'categories':categories})


# Редактирование категори
def categories_edit(request, id):
    # Берем id для изменения категори или же для перехода на страницу уникального где мы изменяем категори
    categories = Category.get(id = id)
    # Если метод POST то срабатывает функция которая изменяет наш категори
    if request.method == 'POST':
        categories.title = request.POST.get('title')
        categoryId = int(request.POST.get('category'))
        categories.category = Category.objects.get(id = categoryId)
    else:
        # Передаем все обьекты категорий
        categories = Category.objects.order_by("title")
        return render(request, 'admin/post-detail-edit.html', {'categories':categories})   



# Все посты
def posts(request):
    # Все обьекты поста
    posts = Post.objects.all()
    return render(request, 'admin/posts.html', {'posts':posts})

# Редактирование поста
def post_edit(request, id):
    # Берем id для изменения поста или же для перехода на страницу уникального где мы изменяем пост
    post = Post.objects.get(id = id)
    # Если метод POST то срабатывает функция которая изменяет наш пост
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.body = request.POST.get('body')
        categoryId = int(request.POST.get('category'))
        post.category = Category.objects.get(id = categoryId)

        if request.POST.get('image') == '':
            post.save()
            return redirect('posts')
        else:
            myfile = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            post.image = filename
            post.save()
            return  redirect('posts')
    # Иначе просто перенаправляет на страницу уникального поста
    else:
        # Передаем все обьекты категорий
        categories = Category.objects.order_by("title")
        return render(request, 'admin/post-detail-edit.html', {'post':post, 'categories':categories})   

# Создание kategori
def createCategory(request):
    if request.method == 'POST':
        # Создаем новый, пустой обьект поста
        category = Category()
        # Заполняем
        category.title = request.POST.get('title')
        category.save()
        return redirect('categories')
    else:
        # Передаем все обьекты категорий
        return render(request, 'admin/createCategory.html')



# Создание поста
def create(request):
    if request.method == 'POST':
        # Создаем новый, пустой обьект поста
        post = Post()
        # Заполняем
        categoryId = request.POST.get('category')
        post.title = request.POST.get('title')
        post.body = request.POST.get('body')
        post.category = Category.objects.get(id=categoryId)
        # Если картинка пустая, то просто сохраням и завершаем функцию
        if request.POST.get('image') == '':
            post.save()
            return redirect('posts')
        # Или же если картинка имеется, то заполянем и сохраняем
        else:
            # Запомните эту формулу для загрузки картинки
            myfile = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            post.image = filename
            post.save()
            return  redirect('posts')

    else:
        # Передаем все обьекты категорий
        categories = Category.objects.order_by('title')
        return render(request, 'admin/create.html', {"categories": categories})


# Удалаем пост
def remove_post(request, id):
    # Находим пост по id и удаляем
    post = Post.objects.get(id=id)
    post.delete()
    return redirect('posts')


# Удаление постов
def remove_posts(request):
    if request.method == 'POST':
        # Ответ из select
        answer = request.POST.get('answer')
        # Если delete то берем все айдишки постов где мы поставили галочки и запихиваем в массив
        if answer =='delete':
            # get()- принимает одну информацию через name(типа querrySelector)
            # getlist() - принимает несколько информаций через name(типа querrySelectorAll)
            items = request.POST.getlist('items')
            # Через цикл for удяляем постов по его id
            for item_id in items:
                post = Post.objects.get(id=item_id)
                post.delete()
            return redirect('categories')
        else:
            return redirect('categories')


# Udalit category
def remove_category(request):
    if request.method == 'POST':
        # Ответ из select
        answer = request.POST.get('answer')
        # Если delete то берем все айдишки постов где мы поставили галочки и запихиваем в массив
        if answer =='delete':
            # get()- принимает одну информацию через name(типа querrySelector)
            # getlist() - принимает несколько информаций через name(типа querrySelectorAll)
            items = request.POST.getlist('items')
            # Через цикл for удяляем постов по его id
            for item_id in items:
                category = Category.objects.get(id=item_id)
                category.delete()
            return redirect('categories')
        else:
            return redirect('categories')

# Поиск
def search(request):
    # То что мы написали в инпуте 
    query = request.GET.get('search')
    # Фильтуем посты по загаловку и тексту
    posts = Post.objects.filter(
        Q(title__icontains=query) |Q(body__icontains=query)
    )
    return render(request, 'blog/search.html', {'posts':posts, 'query':query})



# Регистрация

# Дальше сами. Я много раз объяснял

def signin(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse('Такого пользователя не существует, лох.')
    else:
        return render(request, 'auth/signin.html')


def signout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('index')


def signup(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('index')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():  
            user = form.save()
            profile = Profile()
            profile.user = user
            profile.save()
            login(request, user)
            # messages.success(request, 'Account created successfully')
            return redirect('index')
        else:
            messages = ValidationError(list(form.errors.values()))
            return render(request, 'auth/register.html', {'form':form, 'messages':messages})
           
    else:
        form = RegisterForm()
        return render(request, 'auth/register.html', {'form':form})

               
def add_favourite(request, postId):
    user = request.user
    post = Post.objects.get(id=postId)
    favourite = Favourite()
    favourite.user = user
    favourite.post = post
    favourite.save()
    return redirect(reverse('post_detail', kwargs={'id':postId}))



# Лайки Дизлайки

def like(request, id):
    user = request.user
    post = Post.objects.get(id=id)

    if Like.objects.filter(user=user).filter(post=post).exists():
        like = Like.objects.filter(user=user).filter(post=post)
        like.delete()
        return redirect(reverse('post_detail', kwargs={'id':post.id}))
    else:
        if Dislike.objects.filter(user=user).filter(post=post).exists():
            dislike = Dislike.objects.filter(user=user).filter(post=post)
            dislike.delete()

        like = Like()
        like.user = user
        like.post = post
        like.save()
        return redirect(reverse('post_detail', kwargs={'id':post.id}))


def dislike(request, id):
    user = request.user
    post = Post.objects.get(id=id)

    if Dislike.objects.filter(user=user).filter(post=post).exists():
        dislike = Dislike.objects.filter(user=user).filter(post=post)
        dislike.delete()
        return redirect(reverse('post_detail', kwargs={'id':post.id}))
    else:
        if Like.objects.filter(user=user).filter(post=post).exists():
            like = Like.objects.filter(user=user).filter(post=post)
            like.delete()

        dislike = Dislike()
        dislike.user = user
        dislike.post = post
        dislike.save()
        return redirect(reverse('post_detail', kwargs={'id':post.id}))