from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts", null=True)
    content = models.CharField(max_length=500, null=True)
    time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.poster}: {self.time}"

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.username,
            "content": self.content,
            "time": self.time
        }

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following", null=True)
    account = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers", null=True)
    is_following = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.follower} follows {self.account}"

    def serialize(self):
        return {
            "id": self.id,
            "follower": self.follower.username,
            "account": self.account.username,
            "is_following": self.is_following
        }

class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likedPosts", null=True)
    postId = models.CharField(max_length=1000, null=True)
    is_liked = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.liker} likes Post: {self.postId}"

    def serialize(self):
        return {
            "id": self.id,
            "liker": self.liker.username,
            "postId": self.postId,
            "is_liked": self.is_liked
        }