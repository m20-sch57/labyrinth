from LabyrinthObjects.Vanilla.consts import *
from LabyrinthEngine import Item


class Health(Item):
    def __init__(self):
        # def hurtself():
        #     self.hurt(self.labyrinth.get_active_player())
        # self.new_at(hurtself, lambda: True, 'Ранить себя')
        # def healself():
        #     self.heal(self.labyrinth.get_active_player())
        # self.new_at(healself, lambda: True, 'Вылечиться')
        self.health_bar = self.new_status_bar('Здоровье', None)

    def update_health_bar(self):
        self.health_bar.set_all_values(self.hp)

    def set_settings(self, settings, locations, items, creatures, players):
        self.MAX_PLAYER_HEALTH = settings.get('max_player_health') or MAX_PLAYER_HEALTH
        self.MAX_CREATURE_HEALTH = settings.get('max_creature_health') or MAX_CREATURE_HEALTH

        self.hp = {player: self.MAX_CREATURE_HEALTH for player in players}
        self.creature_hp = {creature: self.MAX_CREATURE_HEALTH for creature in creatures}

        self.labyrinth.set_unique_key(self, 'health')

        self.set_name(settings['name'])

        self.update_health_bar()

    def hurt(self, body, death_msg=None):
        if body.lrtype == 'creature':
            self.creature_hp[body] -= 1
            if self.creature_hp[body] == 0:
                self.labyrinth.get_unique('death').kill(body)

        elif body.lrtype == 'player':
            self.hp[body] -= 1

            if body.have_flag('drop_items_when_injured'):
                location = body.get_parent()
                for item in body.get_children('item'):
                    item.set_parent(location)

            if self.hp[body] == 0:
                self.labyrinth.get_unique('death').kill(body, death_msg)
            self.update_health_bar()

    def heal(self, body):
        if body.lrtype == 'creature':
            self.creature_hp[body] = self.MAX_CREATURE_HEALTH
        elif body.lrtype == 'player':
            self.hp[body] = self.MAX_PLAYER_HEALTH
            self.update_health_bar()
