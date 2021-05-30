from django.shortcuts import render ,redirect
from django.http import HttpResponse
import json
from profiles.models import users
from .models import MatchList, MatchRequest


# Create your views here.


def match_requests(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        id = kwargs.get("userId")
        account = users.objects.get(userId=id)
        if account == user:
            match_requests = MatchRequest.objects.filter(receiver=account, is_active=True)
            context['match_requests'] = match_requests
        else:
            return HttpResponse("You can't view another users friend requests.")
    else:
        redirect("login")
    return render(request, "matchsystem/match_requests.html", context)


def send_match_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            receiver = users.objects.get(pk=user_id)
            try:
                # Get any friend requests (active and not-active)
                match_requests = MatchRequest.objects.filter(sender=user, receiver=receiver)
                # find if any of them are active (pending)
                try:
                    for request in match_requests:
                        if request.is_active:
                            raise Exception("You already sent them a Match request.")
                    # If none are active create a new friend request
                    match_request = MatchRequest(sender=user, receiver=receiver)
                    match_request.save()
                    payload['response'] = "Match request sent."
                except Exception as e:
                    payload['response'] = str(e)
            except MatchRequest.DoesNotExist:
                # There are no friend requests so create one.
                friend_request = MatchRequest(sender=user, receiver=receiver)
                friend_request.save()
                payload['response'] = "Match request sent."

            if payload['response'] is None:
                payload['response'] = "Something went wrong."
        else:
            payload['response'] = "Unable to send a Match request."
    else:
        payload['response'] = "You must be authenticated to send a Match request."

    return HttpResponse(json.dumps(payload), content_type="application/json")


def accept_match_request(request, *args, **kwargs):
    user = request.user
    print(user)
    payload = {}
    if request.method == "GET" and user.is_authenticated:
        match_request_id = kwargs.get("match_request_id")
        if match_request_id:
            match_request = MatchRequest.objects.get(id=match_request_id)
            # confirm that is the correct request
            if match_request.receiver == user:
                print(match_request)
                if match_request:
                    # found the request. Now accept it
                    match_request.accept()
                    payload['response'] = "Match request accepted."
                else:
                    payload['response'] = "Something went wrong."
            else:
                payload['response'] = "That is not your request to accept."
        else:
            payload['response'] = "Unable to accept that Match request."
    else:
        # should never happen
        payload['response'] = "You must be authenticated to accept a Match request."
    return HttpResponse(json.dumps(payload), content_type="application/json")

#
# def remove_match(request, *args, **kwargs):
#     user = request.user
#     payload = {}
#     if request.method == "POST" and user.is_authenticated:
#         user_id = request.POST.get("receiver_user_id")
#         if user_id:
#             try:
#                 removee = users.objects.get(pk=user_id)
#                 match_list = MatchList.objects.get(user=user)
#                 match_list.unmatch(removee)
#                 payload['response'] = "Successfully removed that friend."
#             except Exception as e:
#                 payload['response'] = f"Something went wrong: {str(e)}"
#         else:
#             payload['response'] = "There was an error. Unable to remove that friend."
#     else:
#         # should never happen
#         payload['response'] = "You must be authenticated to remove a friend."
#     return HttpResponse(json.dumps(payload), content_type="application/json")
#
#
# def decline_friend_request(request, *args, **kwargs):
#     user = request.user
#     payload = {}
#     if request.method == "GET" and user.is_authenticated:
#         friend_request_id = kwargs.get("friend_request_id")
#         if friend_request_id:
#             friend_request = FriendRequest.objects.get(pk=friend_request_id)
#             # confirm that is the correct request
#             if friend_request.receiver == user:
#                 if friend_request:
#                     # found the request. Now decline it
#                     updated_notification = friend_request.decline()
#                     payload['response'] = "Friend request declined."
#                 else:
#                     payload['response'] = "Something went wrong."
#             else:
#                 payload['response'] = "That is not your friend request to decline."
#         else:
#             payload['response'] = "Unable to decline that friend request."
#     else:
#         # should never happen
#         payload['response'] = "You must be authenticated to decline a friend request."
#     return HttpResponse(json.dumps(payload), content_type="application/json")
#
#
# def cancel_friend_request(request, *args, **kwargs):
#     user = request.user
#     payload = {}
#     if request.method == "POST" and user.is_authenticated:
#         user_id = request.POST.get("receiver_user_id")
#         if user_id:
#             receiver = Account.objects.get(pk=user_id)
#             try:
#                 friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver, is_active=True)
#             except FriendRequest.DoesNotExist:
#                 payload['response'] = "Nothing to cancel. Friend request does not exist."
#
#             # There should only ever be ONE active friend request at any given time. Cancel them all just in case.
#             if len(friend_requests) > 1:
#                 for request in friend_requests:
#                     request.cance()
#                 payload['response'] = "Friend request canceled."
#             else:
#                 # found the request. Now cancel it
#                 friend_requests.first().cancel()
#                 payload['response'] = "Friend request canceled."
#         else:
#             payload['response'] = "Unable to cancel that friend request."
#     else:
#         # should never happen
#         payload['response'] = "You must be authenticated to cancel a friend request."
#     return HttpResponse(json.dumps(payload), content_type="application/json")
