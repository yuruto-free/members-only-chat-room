from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy
import operator
from functools import reduce

User = get_user_model()

class RoomQueryset(models.QuerySet):
    def filtering(self, keywords='', order='-created_at'):
        words = keywords.split()

        if words:
            condition = reduce(operator.or_, (models.Q(name__icontains=word) for word in words))
            queryset = self.filter(condition)
        else:
            queryset = self

        return queryset.order_by(order).distinct()

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(gettext_lazy('Room name'), max_length=64)
    description = models.TextField(gettext_lazy('Description'), max_length=128)
    created_at = models.DateTimeField(gettext_lazy('Created time'), default=timezone.now)

    objects = RoomQueryset.as_manager()

    def __str__(self):
        return self.__unicode__()
    def __unicode__(self):
        return self.name

    def set_host(self, user=None):
        if user is not None:
            self.host = user

    def is_host(self, user=None):
        return user is not None and self.host.pk == user.pk

class MessageManager(models.Manager):
    def ordering(self, order='created_at'):
        return self.get_queryset().order_by(order)

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField(gettext_lazy('Content'))
    created_at = models.DateTimeField(gettext_lazy('Created time'), default=timezone.now)

    objects = MessageManager()

    def __str__(self):
        return self.__unicode__()
    def __unicode__(self):
        name = str(self.owner)
        text = self.content[:32]

        return f'{name}:{text}'