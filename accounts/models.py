from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", null=False)
    date_of_birth = models.DateField(null=True, blank=True)
    biography = models.TextField(default='Awaiting users story', blank=True)
    avatar = models.FilePathField(blank=True, null=True)

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={
            'pk': self.user.pk
        })

    def generate_file_path(self):
        user_path = 'images\\user_avatars' + '\\{}-{}.jpeg'.format(
            self.user.first_name, self.user.last_name
        )
        return user_path
