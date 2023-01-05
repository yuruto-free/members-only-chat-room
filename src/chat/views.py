from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from . import models, forms

class Index(LoginRequiredMixin, ListView):
    model = models.Room
    template_name = 'chat/index.html'
    context_object_name = 'rooms'
    pagenate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        form = forms.SearchForm(self.request.GET or None)
        keywords = form.get_keywords()

        return queryset.filtering(user=self.request.user, keywords=keywords)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = forms.SearchForm(self.request.GET or None)

        return context

class CreateRoom(LoginRequiredMixin, CreateView):
    model = models.Room
    template_name = 'chat/room_form.html'
    form_class = forms.RoomForm
    success_url = reverse_lazy('chat:index')

    def form_valid(self, form):
        form.instance.set_host(self.request.user)
 
        return super().form_valid(form)

class OnlyRoomHostMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        room = self.get_object()

        return room.is_host(self.request.user)

class UpdateRoom(LoginRequiredMixin, OnlyRoomHostMixin, UpdateView):
    model = models.Room
    template_name = 'chat/room_form.html'
    form_class = forms.RoomForm
    success_url = reverse_lazy('chat:index')

class DeleteRoom(LoginRequiredMixin, OnlyRoomHostMixin, DeleteView):
    model = models.Room
    success_url = reverse_lazy('chat:index')

    def get(self, request, *args, **kwargs):
        # ignore direct access
        return self.handle_no_permission()

class OnlyAssignedUserMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        room = self.get_object()

        return room.is_assigned(self.request.user)

class EnterRoom(LoginRequiredMixin, OnlyAssignedUserMixin, DetailView):
    model = models.Room
    template_name = 'chat/chat_room.html'
    context_object_name = 'room'