from LabyrinthObjects.Vanilla.consts import *
from LabyrinthEngine import Item


class Health(Item):
    # def __init__(self):
    #     def hurtself():
    #         self.hurt(self.labyrinth.get_active_player())
    #     self.new_at(hurtself, lambda: True, 'Ранить себя')
    #     def healself():
    #         self.heal(self.labyrinth.get_active_player())
    #     self.new_at(healself, lambda: True, 'Вылечиться')

    def set_settings(self, settings, locations, items, npcs, players):
        self.MAX_PLAYER_HEALTH = settings.get('max_player_health') or MAX_PLAYER_HEALTH
        self.MAX_NPC_HEALTH = settings.get('max_npc_health') or MAX_NPC_HEALTH

        self.hp = {player: self.MAX_NPC_HEALTH for player in players}
        self.npc_hp = {npc: self.MAX_NPC_HEALTH for npc in npcs}

        self.labyrinth.set_unique_key(self, 'health')

        self.set_name(settings['name'])

        self.DEATH_MSG = settings.get('consts', {}).get('death_msg') or DEATH_MSG


    def hurt(self, body):
        if body.lrtype == 'npc':
            self.npc_hp[body] -= 1
            self.labyrinth.NPCs.discard(body)

        elif body.lrtype == 'player':
            self.hp[body] -= 1

            if self.hp[body] == 0:
                index = self.labyrinth.players_list.index(body)
                del self.labyrinth.players_list[index]

                self.labyrinth.send_msg(self.DEATH_MSG, body)

    def heal(self, body):
        if body.lrtype == 'npc':
            self.npc_hp[body] = self.MAX_NPC_HEALTH
        elif body.lrtype == 'player':
            self.hp[body] = self.MAX_PLAYER_HEALTH