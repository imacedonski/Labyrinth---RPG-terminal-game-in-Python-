class NPC:
    def __init__(self, name, quest):
        self.name = name
        self.quest = quest

    def text(self):
        if self.name == 'Diego':
            print(
                f'I need you to kill 3 wolves! Good luck!\nReward: {self.quest.reward.name}')
        if self.name == 'Xardas':
            print(f'I need you to find my ring! Good luck!\nReward: {self.quest.reward.name}')
        if self.name == 'Lester':
            print(f'I need you to kill 3 goblins! Good luck!\nReward: {self.quest.reward.name}')

    def set_none(self):
        self.quest = None



