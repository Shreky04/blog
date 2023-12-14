from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=40, verbose_name="Назва", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

class Tag(models.Model):
    tagname = models.CharField(max_length=40, verbose_name="Tag", unique=True)

    def __str__(self):
        return self.tagname

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

class Comments(models.Model):
    text = models.TextField(max_length=400, verbose_name="Коментар")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    published_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата та час")

    def __str__(self):
        return f"{self.author} {self.published_date}"

    class Meta:
        verbose_name = "Коментар"
        verbose_name_plural = "Коментарі"

class Post(models.Model):
    title = models.CharField(max_length=40, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Опис")
    published_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата та час")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="категорія")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    poster = models.URLField(default="http://placehold.it/900x300", verbose_name="Постер")
    tag = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name="Tags")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Пости"

class Subscribe(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    dateofbirth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Профіль"
        verbose_name_plural = "Профілі"