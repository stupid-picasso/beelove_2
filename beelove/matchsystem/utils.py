from .models import MatchRequest


def get_match_request_or_false(sender, receiver):
    try:
        return MatchRequest.objects.get(sender=sender, receiver=receiver, is_active=True)
    except MatchRequest.DoesNotExist:
        return False