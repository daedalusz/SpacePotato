from GameWindow import GameWindow
from GameObjects import PlayerShip
from pyglet.text import HTMLLabel

class HUD:

    font = 'Times New Roman'
    font_size = 20
    font_color = '#FFFF'

    def __init__(self, player, window):
        self.player = player
        self.window = window

        health_label_coord = (window.width * .03, window.height*.97)
        score_label_coord = (window.width * .03, (window.height*.97)-20 )

        self._health_label = HTMLLabel('<font face="'+self.font+'" size="'+str(self.font_size)+'" color="'+
                                       self.font_color+'"><b>Health:</b></font> '+str(window.player.hp),
                          x=health_label_coord[0], y=health_label_coord[1],
                          anchor_x='left', anchor_y='center')

        self._score_label =HTMLLabel('<font face="'+self.font+'" size="'+str(self.font_size)+'" color="'+
                                     self.font_color+'"><b>Chips:</b></font> '+str(window.player.score),
                          x=score_label_coord[0], y=score_label_coord[1],
                          anchor_x='left', anchor_y='center')

        self._health_label.batch = window.hud_batch
        self._score_label.batch = window.hud_batch
        self.window.register_for_update(self)


    def update(self, dt):
        self._health_label.text = '<font face="'+self.font+'" size="'+str(self.font_size)+'" color="'+\
                                  self.font_color+'"><b>Health:</b>'+str(self.window.player.hp)+"</font>"
        self._score_label.text = '<font face="'+self.font+'" size="'+str(self.font_size)+'" color="'+\
                                 self.font_color+'"><b>Chips:</b>'+str(self.window.player.score)+"</font>"
