from django.shortcuts import render, redirect
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required

from flashcards.forms import AddCardForm
from flashcards.learn_utils import get_next_card
from .models import Card, Bin

# Home page, shows number of total cards
@login_required
def index(request):
    cards_count = Card.objects.filter(user=request.user).count()
    context = dict(cards_count=cards_count)
    return render(request, 'flashcards/index.html', context)

# Page to add new cards and to see all cards
@login_required
def admin(request):
    cards = Card.objects.filter(user=request.user).order_by('-id')

    if request.method == 'POST':
        form = AddCardForm(request.POST)
        if form.is_valid():
            card = Card()
            card.word = request.POST['word']
            card.definition = request.POST['definition']
            card.user = request.user
            card.bin = Bin.objects.all().order_by('order')[0]
            card.save()
            return redirect('/cardadmin')
    else:
        form = AddCardForm()

    context = dict(
        cards=cards,
        form=form
    )

    return render(request, 'flashcards/admin.html', context)

# show next best card
@login_required
def learn(request):
    # logic for best next card in testable function
    card, message = get_next_card(request.user)
    context = dict(
        card=card,
        message=message
    )
    return render(request, 'flashcards/learn.html', context)

# records the answers and updates the current card
@login_required
def answer(request, card_id, result):
    # this can set set to 11 (or pre-calculated to not have to query it at every request
    max_bin = Bin.objects.all().order_by('-order')[0].order

    # get current card
    cards = Card.objects.filter(user=request.user, id=card_id)

    # if no card was found for that id and user, just return to the users learn url
    if not cards:
        return redirect('/learn')

    card = cards[0]

    # if incorrect, increment total wrong and move back to bin 1
    if result == 'incorrect':
        card.total_wrong += 1
        card.bin = Bin.objects.get(order=1)

    # if correct, move to next bin in order (if not already in last bin)
    else:
        card.bin = Bin.objects.get(order=card.bin.order+1 if card.bin.order < max_bin else max_bin)

    # increase time to review by time delta of current bin
    if card.bin.order < max_bin:
        card.next_review = timezone.now() + relativedelta(**{card.bin.unit: card.bin.amount})

    card.save()
    return redirect('/learn')
