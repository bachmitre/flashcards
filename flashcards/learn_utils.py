from datetime import datetime
import pytz
from .models import Bin, Card

permanently_done_msg = 'You have no more words to review; you are permanently done!'
temporarily_done_msg = 'You are temporarily done; please come back later to review more words.'
max_total_wrong = 10


def get_next_card(user):
    """
    find best next card for user
    :param user:
    :return: card, message tuple
    """
    card = None
    message = None

    # this can set set to 11 (or pre-calculated to not have to query it at every request
    max_bin = Bin.objects.all().order_by('-order')[0].order

    # get all cards that are
    # - from the user
    # - not in last bin and not in bin 0
    # - have less than max_total_wrong total wrongs
    # in the order of next review time
    active_cards = Card.objects.filter(
        user=user,
        total_wrong__lte=max_total_wrong,
        bin__order__lt=max_bin,
        bin__order__gt=0,
    ).order_by('next_review')

    # cards with review time in the past
    due_cards = active_cards.filter(
        next_review__lt=datetime.utcnow().replace(tzinfo=pytz.UTC)
    )

    # if no due cards found, take from bin 0
    if not due_cards:
        new_cards = Card.objects.filter(
            user=user,
            bin__order=0
        )

        # if no cards in bin 0 and no active cards, then permanently done
        if not new_cards and not active_cards:
            message = permanently_done_msg

        # else: no new cards: temporarily done
        elif not new_cards:
            message = temporarily_done_msg

        else:
            card = new_cards[0]

    else:
        card = due_cards[0]

    return card, message