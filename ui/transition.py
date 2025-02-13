import basilisk as bsk


class Transition:
    def __init__(self, ui, duration: float=1.0, callback=None):
        """
        Plays a transition on instantiation
        """
        
        self.engine = ui.game.engine
        self.img = ui.transition_card
        self.clock = 0
        self.duration = duration
        self.callback = callback

    def render(self) -> None:
        """
        
        """

        # Update the transition's time        
        self.clock += self.engine.delta_time

        # Render

        cross_fade_intensity = 3.0
        alpha = .75 * min(cross_fade_intensity * ((self.duration / 2) ** 2 - (self.clock - self.duration / 2) ** 2), 1.0)

        box_h = 200
        win_w, win_h = self.engine.win_size
        rect = (0, win_h // 2 - box_h // 2, win_w, box_h)
        bsk.draw.blit(self.engine, self.img, rect, alpha)

    @property
    def running(self): return self.clock < self.duration