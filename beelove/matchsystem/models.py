from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.datetime_safe import datetime


class MatchList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
    matches = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="matches")

    class Meta:
        app_label = "matchsystem"

    def __str__(self):
        return str(self.user.userId)

    def add_match(self, user):
        """
        Add a new friend.
        """
        if not user in self.matches.all():
            self.friends.add(user)
            self.save()

    def remove_match(self, user):
        """
        Remove a friend.
        """
        if user in self.matches.all():
            self.friends.remove(user)

    def unmatch(self, removee):
        """
        Initiate the action of unfriending someone.
        """
        remover_matches_list = self  # person terminating the friendship

        # Remove friend from remover friend list
        remover_matches_list.remove_match(removee)

        # Remove friend from removee friend list
        matches_list = MatchList.objects.get(user=removee)
        matches_list.remove_match(remover_matches_list.user)


class MatchRequest(models.Model):
    """
    A friend request consists of two main parts:
    1. SENDER
        - Person sending/initiating the friend request
    2. RECIVER
        - Person receiving the friend friend
        """

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")
    is_active = models.BooleanField(blank=False, null=False, default=True)
    times_tamp = models.DateTimeField(auto_now_add=True,blank=False, null=False)

    class Meta:
        app_label = "matchsystem"

    def __str__(self):
        return str(self.sender.userId)

    def accept(self):
        """
        Accept a friend request.
        Update both SENDER and RECEIVER friend lists.
        """
        receiver_matches_list = MatchList.objects.get(user=self.receiver)
        if receiver_matches_list:
            receiver_matches_list.add_match(self.sender)
            sender_matches_list = MatchList.objects.get(user=self.sender)
            if sender_matches_list:
                sender_matches_list.add_match(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        self.is_active = False
        self.save()

    def cancel(self):
        self.is_active = False
        self.save()
