from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy
import operator
from functools import reduce

User = get_user_model()

class RoomQueryset(models.QuerySet):
    def _related_user(self, user=None):
        try:
            queryset = self.filter(models.Q(host=user) | models.Q(participants__in=[user.pk]))
        except:
            queryset = self

        return queryset

    def filtering(self, user=None, keywords='', order='-created_at'):
        words = keywords.split()
        queryset = self._related_user(user=user)

        if words:
            condition = reduce(operator.or_, (models.Q(name__icontains=word) for word in words))
            queryset = queryset.filter(condition)

        return queryset.order_by(order).distinct()

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(gettext_lazy('Room name'), max_length=64)
    description = models.TextField(gettext_lazy('Description'), max_length=128)
    participants = models.ManyToManyField(User, related_name='rooms', verbose_name=gettext_lazy('Participants'), blank=True)
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

    def is_assigned(self, user=None):
        try:
            _ = self.participants.all().get(pk=user.pk)
            return True
        except User.DoesNotExist:
            return self.host == user
        except Exception:
            return False

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