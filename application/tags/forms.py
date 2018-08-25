from application.forms import BaseForm, length_validators, MultiCheckboxField
from wtforms import validators, StringField
from application.tags.models import Tag, GameTag

class TagSelectionForm(BaseForm):
    # HUOM! Täytyy asettaa vaihtoehdot ennen kun käytetään templaatissa
    # Koska haetaan tietyn käyttäjän tagit, kutstutaan luontevammasta paikkasta missä käsitellään kirjautuneen käytättäjän tietoja
    tag_ids = MultiCheckboxField("Valitse tagit", coerce = int)

    def set_choices_for_user(self, user): 
        self.tag_ids.choices = [(tag.id, tag.name) for tag in user.tags()]

    def select_users_tags_for_game(self, user, game):
        tags = Tag.query.join(Tag.game_tags).filter(Tag.account_id==user.id, GameTag.game_id==game.id)
        self.tag_ids.data = map(lambda t: t.id, tags)


class TagCreationForm(BaseForm):
    name = StringField("Tagin nimi ", length_validators(max=100))