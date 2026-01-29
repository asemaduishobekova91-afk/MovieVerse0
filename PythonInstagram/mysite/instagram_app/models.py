from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    user_photo = models.ImageField(null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(16), MaxValueValidator(70)],
                                           null=True, blank=True)
    is_official = models.BooleanField(default=False)
    user_network = models.URLField(null=True, blank=True)
    description = models.TextField()
    date_registered = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class Follow(models.Model):
    following = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user1')
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user2')
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.following}'


class City(models.Model):
    city_name = models.CharField()

    def __str__(self):
        return self.city_name

class HashTag(models.Model):
    hashtag_name = models.CharField()

    def __str__(self):
        return self.hashtag_name


class Post(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='users')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='post_city',
                             null=True, blank=True)
    hashtag = models.ManyToManyField(HashTag)
    description = models.TextField()
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'


class PostContent(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='content')
    content = models.FileField()

    def __str__(self):
        return f'{self.post}'

class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'post')


    def __str__(self):
        return f'{self.post}'

class Review(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.post}, {self.user}'


class ReviewLike(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'review')


    def __str__(self):
        return f'{self.review}, {self.user}'


class Chat(models.Model):
    person = models.ManyToManyField(UserProfile)
    created_date = models.DateField(auto_now_add=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    auther = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='image', null=True, blank=True)
    video = models.FileField(upload_to='video', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)