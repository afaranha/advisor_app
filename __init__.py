from otree.api import *


doc = """
Your app description
"""


def creating_session(subsession):
    for player in subsession.get_players():
        if player.role == Constants.ADVISOR_ROLE:
            player.name = "Advisor " + str(player.id)
    for group in subsession.get_groups():
        group.advisor = group.get_player_by_role(Constants.ADVISOR_ROLE).name


class Constants(BaseConstants):
    name_in_url = 'advisor'
    players_per_group = 2
    num_rounds = 2

    ADVISOR_ROLE = "Advisor"
    CLIENT_ROLE = "Client"

    GOOD_OFFER = "GOOD"
    MEDIUM_OFFER = "MEDIUM"
    BAD_OFFER = "BAD"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    sent_offer = models.StringField(
        choices=[Constants.GOOD_OFFER, Constants.MEDIUM_OFFER, Constants.BAD_OFFER],
        widget=widgets.RadioSelect,
        initial=0,
        label="Select an offer to make",
    )
    accept_offer = models.BooleanField(
        choices=[[True, "Accept"], [False, "Reject"]],
        widget=widgets.RadioSelect,
        initial=False,
        label="",
    )
    advisor = models.StringField()


class Player(BasePlayer):
    name = models.StringField()


# PAGES
class Offer(Page):
    form_model = 'group'
    form_fields = ['sent_offer']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == Constants.ADVISOR_ROLE


class AcceptOffer(Page):
    form_model = 'group'
    form_fields = ['accept_offer']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == Constants.CLIENT_ROLE


class AcceptOfferWaitPage(WaitPage):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Offer, AcceptOfferWaitPage, AcceptOffer, ResultsWaitPage, Results]
