from LabyrinthObjects.Vanilla.consts import *
from LabyrinthEngine import Item


class Ammo(Item):
    def __init__(self):
        # def resetallself():
        #     self.reset_all(self.labyrinth.get_active_player())
        # self.new_at(resetallself, lambda: True, 'Восстановить патроны')

        self.bullet_counter_bar = self.new_status_bar('Пули', None) 
        self.bomb_counter_bar = self.new_status_bar('Бомбы', None)

    def update_bars(self):
        self.bullet_counter_bar.set_all_values(self.bullets)
        self.bomb_counter_bar.set_all_values(self.bombs)

    def set_settings(self, settings, locations, items, creatures, players):
        self.MAX_BULLETS_COUNT = settings.get('max_bullets_count') or MAX_BULLETS_COUNT
        self.MAX_BOMBS_COUNT = settings.get('max_bombs_count') or MAX_BOMBS_COUNT

        self.INIT_BULLETS_COUNT = settings.get('init_bullets_count') or self.MAX_BULLETS_COUNT
        self.INIT_BOMBS_COUNT = settings.get('init_bombs_count') or self.MAX_BOMBS_COUNT

        self.bullets = {player: self.INIT_BULLETS_COUNT for player in players}
        self.bombs = {player: self.INIT_BOMBS_COUNT for player in players}
        self.update_bars()

        self.labyrinth.set_unique_key(self, 'ammo')

    def spend(self, ammo_type, player):
        if ammo_type == 'bullet':
            self.bullets[player] -= 1
            return self.bullets[player]
        elif ammo_type == 'bomb':
            self.bombs[player] -= 1
            return self.bombs[player]
        self.update_bars()

    def have(self, ammo_type, player):
        if ammo_type == 'bullet':
            return self.bullets[player] > 0
        elif ammo_type == 'bomb':
            return self.bombs[player] > 0

    def reset(self, ammo_type, player):
        if ammo_type == 'bullet':
            self.bullets[player] = self.MAX_BULLETS_COUNT
        elif ammo_type == 'bomb':
            self.bombs[player] = self.MAX_BOMBS_COUNT
        self.update_bars()

    def reset_all(self, player):
        self.bullets[player] = self.MAX_BULLETS_COUNT
        self.bombs[player] = self.MAX_BOMBS_COUNT
        self.update_bars()
