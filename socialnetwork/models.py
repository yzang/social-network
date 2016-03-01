from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create a proxy model as customed user

class Profile(models.Model):
    account = models.OneToOneField(User, on_delete=models.CASCADE,related_name='account')
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    age = models.IntegerField(null=True,blank=True)
    biography = models.CharField(max_length=430,null=True,blank=True)
    # avatar=models.FileField(upload_to='user_avatars',null=True,blank=True)
    followee = models.ManyToManyField(User,related_name='followee')
    picture_url=models.CharField(blank=True,max_length=200)
    # avatar_content_type=models.CharField(max_length=50)
    def __unicode__(self):
        return self.account.username
    def __str__(self):
        return self.__unicode__()



# One use have many posts, one post belongs to only one user
class Post(models.Model):
    content = models.CharField(max_length=160)
    owner = models.ForeignKey(Profile,null=True)
    post_date = models.DateTimeField(auto_now_add=True,)

    def __unicode__(self):
        return "user:" + self.owner.account.username + "\tcontent:" + self.content + "\t" + str(self.post_date)

    def __str__(self):
        return self.__unicode__()


# One use have many posts, one post belongs to only one user
class PostReply(models.Model):
    content = models.CharField(max_length=160)
    owner = models.ForeignKey(Profile,null=True)
    reply_date = models.DateTimeField(auto_now_add=True)
    post=models.ForeignKey(Post)

    def __unicode__(self):
        return "user:" + self.owner.account.username + "\tcontent:" + self.content + "\t" + str(self.reply_date)

    def __str__(self):
        return self.__unicode__()
