import basilisk as bsk
from .transition import Transition


class UI:
    transitions: list[Transition]
    """"""
    def __init__(self, game):
        self.game = game
        self.transitions = []
        self.transition_card = bsk.Image('images/transition_card.png')

    def render(self):
        # Cross
        bsk.draw.circle(self.game.engine, (225,225,225), tuple((map(lambda x: int(x/2), self.game.engine.win_size))), 2)
        bsk.draw.circle(self.game.engine, (15, 15, 15 ), tuple((map(lambda x: int(x/2), self.game.engine.win_size))), 4)

        # Bullet shoot time
        box_w, box_h = 35, int(200 * min((self.game.player.gun.time / self.game.player.gun.cooldown), 1.0))
        win_w, win_h = self.game.engine.win_size
        rect = (win_w - box_w - 10, win_h - box_h - 10, box_w, box_h)
        max_rect = (win_w - box_w - 10, win_h - 200 - 10, box_w, 200)
        bsk.draw.rect(self.game.engine, (150,150,225), rect)
        bsk.draw.line(self.game.engine, (0, 0, 0, 255), (max_rect[0], max_rect[1]), (max_rect[0] + max_rect[2], max_rect[1]), thickness=2)
        bsk.draw.line(self.game.engine, (0, 0, 0, 255), (max_rect[0], max_rect[1]), (max_rect[0], max_rect[1] + max_rect[3]), thickness=2)
        bsk.draw.line(self.game.engine, (0, 0, 0, 255), (max_rect[0] + max_rect[2], max_rect[1]), (max_rect[0] + max_rect[2], max_rect[1] + max_rect[3]), thickness=2)
        bsk.draw.line(self.game.engine, (0, 0, 0, 255), (max_rect[0], max_rect[1] + max_rect[3]), (max_rect[0] + max_rect[2], max_rect[1] + max_rect[3]), thickness=2)

        # Transitions
        i = 0
        while i < len(self.transitions):
            transition = self.transitions[i]
            transition.render()
            if not transition.running:
                if transition.callback: transition.callback()
                self.transitions.remove(transition)
            i += 1

        

    def add_transition(self, duration: float=1.0, callback=None):
        self.transitions.append(Transition(self, duration, callback))