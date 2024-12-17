import numpy as np
import random as rd
import testmicropythonBackEnd as be

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy_garden.matplotlib import FigureCanvasKivyAgg
from kivy.uix.slider import Slider

import time

from kivy.clock import Clock

n = be.n 
r_dict = be.r_dict
n_dict = be.n_dict
reset_function = be.initialize_pop
#grid = reset_function(n)
function = be.population_growth
graphfunc = be.Draw_pop_dynamics
invasionfunc = be.pathogene_spawn
plt = be.plt

color_dict = {
    0: (0, 0, 0, 1), # Gris pour l'instant, mais par la suite on va garder gris pour le pathogène, et noir pour "vide"
    1: (0.5, 0, 1, 1),
    2: (0, 0.65, 1, 1),
    3: (0.25, 1, 0.25, 1),
    4: (1, 0.65, 0, 1),
    5: (1, 0, 0, 1),
    6: (0.5, 0.5, 0.5, 1)
}

# Essayer de réecrire la fonction de tracé des points pour qu'elle trace juste 
# les cercles sans leur donner une position initiale fixe puisque de toutes les façons
# la position des points va être modifiée.

# Séparer un "initial draw function" d'un "redraw with updated grid function"

class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Circles_drawings(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.grid = None
        self.app = App.get_running_app()

    def draw_circles(self):
        self.grid = self.reset_grid()
        dim_choice = min(self.width, self.height)
        total_size = dim_choice * 0.9
        cellsize = total_size / n

        x0, y0 = (self.x + (self.width - total_size) / 2,\
                  self.y + (self.height - total_size) / 2)

        positions = [[x0 + (r + 0.5) * cellsize, y0 + (c + 0.5) * cellsize] for r in range(n) for c in range(n)]

        frame_positions = [[x0, y0], [x0, y0], [x0, y0 + total_size], [x0 + total_size, y0]]
        line_width = 1 / 100 * dim_choice
        frame_sizes = [[total_size + line_width, line_width], 
            [line_width, total_size],
            [total_size + line_width, line_width],
            [line_width, total_size]]

        self.circles = []
        self.frame = []

        line_grid = self.grid.flatten()

        self.canvas.before.clear()

        with self.canvas.before:
            
            Color(1, 1, 1, 1)
            for _, (posi, sizes) in enumerate(zip(frame_positions, frame_sizes)):
                self.frame.append(Rectangle(pos = posi, size = sizes))
            
            for _, (position, bact) in enumerate(zip(positions, line_grid)):
                if bact:
                    Color(*color_dict[bact])
                else:
                    Color(0, 0, 0, 0)
                
                self.circles.append(Ellipse(pos = position, size_hint = (None, None), size = (cellsize * 0.6, cellsize * 0.6)))

        self.bind(size = self.update_circles)

    def redraw_circles(self, dt):
        dim_choice = min(self.width, self.height)
        total_size = dim_choice * 0.9
        cellsize = total_size / n

        x0, y0 = (self.x + (self.width - total_size) / 2,\
                  self.y + (self.height - total_size) / 2)

        positions = [[x0 + (r + 0.5) * cellsize, y0 + (c + 0.5) * cellsize] for r in range(n) for c in range(n)]

        frame_positions = [[x0, y0], [x0, y0], [x0, y0 + total_size], [x0 + total_size, y0]]
        line_width = 1 / 100 * dim_choice
        frame_sizes = [[total_size + line_width, line_width], 
            [line_width, total_size],
            [total_size + line_width, line_width],
            [line_width, total_size]]

        self.circles = []
        self.frame = []

        s = [self.app.root.protslider.value, 
             self.app.root.glutslider.value,
             self.app.root.lipslider.value]

        self.grid = function(self.grid, r_dict, n_dict, s)
        line_grid = self.grid.flatten()

        self.canvas.before.clear()   

        with self.canvas.before:
            Color(1, 1, 1, 1)
            for _, (posi, sizes) in enumerate(zip(frame_positions, frame_sizes)):
                self.frame.append(Rectangle(pos = posi, size = sizes))
            
            for _, (position, bact) in enumerate(zip(positions, line_grid)):
                if bact:
                    Color(*color_dict[bact])
                else:
                    Color(0, 0, 0, 0)
                
                self.circles.append(Ellipse(pos = position, size_hint = (None, None), size = (cellsize * 0.6, cellsize * 0.6)))

        self.bind(size = self.update_circles)

    def update_circles(self, instance, value):
        dim_choice = min(self.width, self.height)
        total_size = dim_choice * 0.9
        cellsize = total_size / n

        x0, y0 = (self.x + (self.width - total_size) / 2,\
                  self.y + (self.height - total_size) / 2)

        positions = [[x0 + (r + 0.5) * cellsize, y0 + (c + 0.5) * cellsize] for r in range(n) for c in range(n)]

        frame_positions = [[x0, y0], [x0, y0], [x0, y0 + total_size], [x0 + total_size, y0]]
        line_width = 1 / 100 * dim_choice
        frame_sizes = [[total_size + line_width, line_width], 
            [line_width, total_size],
            [total_size + line_width, line_width],
            [line_width, total_size]]

        for side, (posi, sizes) in enumerate(zip(frame_positions, frame_sizes)):
                self.frame[side].pos = posi
                self.frame[side].size = sizes
        
        for i, position in enumerate(positions):
            self.circles[i].pos = position
            self.circles[i].size = (cellsize * 0.6, cellsize * 0.6)
    
    def reset_grid(self):
        self.grid = reset_function(n)
        return self.grid

    def bact_attack(self):

        dim_choice = min(self.width, self.height)
        total_size = dim_choice * 0.9
        cellsize = total_size / n

        x0, y0 = (self.x + (self.width - total_size) / 2,\
                  self.y + (self.height - total_size) / 2)

        positions = [[x0 + (r + 0.5) * cellsize, y0 + (c + 0.5) * cellsize] for r in range(n) for c in range(n)]

        frame_positions = [[x0, y0], [x0, y0], [x0, y0 + total_size], [x0 + total_size, y0]]
        line_width = 1 / 100 * dim_choice
        frame_sizes = [[total_size + line_width, line_width], 
            [line_width, total_size],
            [total_size + line_width, line_width],
            [line_width, total_size]]

        self.circles = []
        self.frame = []


        self.grid = invasionfunc(self.grid)
        line_grid = self.grid.flatten()

        self.canvas.before.clear()   

        with self.canvas.before:
            Color(1, 1, 1, 1)
            for _, (posi, sizes) in enumerate(zip(frame_positions, frame_sizes)):
                self.frame.append(Rectangle(pos = posi, size = sizes))
            
            for _, (position, bact) in enumerate(zip(positions, line_grid)):
                if bact:
                    Color(*color_dict[bact])
                else:
                    Color(0, 0, 0, 0)
                
                self.circles.append(Ellipse(pos = position, size_hint = (None, None), size = (cellsize * 0.6, cellsize * 0.6)))

        self.bind(size = self.update_circles)


class GridSpace(BoxLayout):
    pass

class SideBar(BoxLayout):
    pass

class LeftBar(BoxLayout):
    pass

class SubBar(BoxLayout):
    pass

class UpBar(BoxLayout):
    pass

class LeftGridSpace(BoxLayout):
    pass

class RightGridSpace(BoxLayout):
    pass

class GraphLeft(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class GraphRight(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class ProtSlider(Slider):
    # We have to change the image for the slider, and put something that make
    # think of proteins = viande + bonbon + beurre
    # Faire les 3 images en pixel art 32px
    pass

class GlutSlider(Slider):
    pass

class LipSlider(Slider):
    pass

class GraphWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.graph = None

    def initgraph(self):
        print(min(self.size))
        image_size = (min(self.size), min(self.size))
        fig, axes = graphfunc(self.app.root.specialwidget.grid, image_size, color_dict)
        self.graph = fig
        self.clear_widgets()
        self.add_widget(FigureCanvasKivyAgg(self.graph))
        self.children[0].x = self.center_x
        self.children[0].y = self.center_y
        self.children[0].size = (min(self.size), min(self.size))

    def updategraph(self, dt):
        image_size = (min(self.size), min(self.size))
        plt.close(self.graph)
        fig, axes = graphfunc(self.app.root.specialwidget.grid, image_size, color_dict)
        self.graph = fig
        self.clear_widgets()
        self.add_widget(FigureCanvasKivyAgg(self.graph))
        self.children[0].x = self.top
        self.children[0].y = self.center_y
        self.children[0].size = (min(self.size), min(self.size))

class SlidingButtons(BoxLayout):
    pass

class ResetSimulation(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        # self.memory = self.app.root.startstopbutton.memory

    def on_press(self):
        # 
        # Clock.unschedule(self.app.root.specialwidget.redraw_circles)
        self.app.root.specialwidget.draw_circles()
        self.app.root.graphwidget.initgraph() # Pas exacetement, il ne faut pas "ajouter un nouveau graph"
        self.app.root.protslider.value = 0.5
        self.app.root.glutslider.value = 0.5
        self.app.root.lipslider.value = 0.5

class StartStop(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.memory = False

    def on_press(self):
        if not self.memory:
            Clock.schedule_interval(self.app.root.specialwidget.redraw_circles, 1/20)
            Clock.schedule_interval(self.app.root.graphwidget.updategraph, 1/20)
            self.memory = True
        elif self.memory:
            Clock.unschedule(self.app.root.specialwidget.redraw_circles)
            Clock.unschedule(self.app.root.graphwidget.updategraph)
            self.memory = False

class Attack(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

    def on_press(self):
        self.app.root.specialwidget.bact_attack()
    pass

class testmicropythonApp(App):
    # Regarde un petit peu

    def build(self):
        self.root = RootWidget()
        # self.startstop = StartStop()
        # self.resetbutton = ResetSimulation()
        self.root.specialwidget.draw_circles()
        self.root.graphwidget.initgraph()

        # self.root.graphleftspace.resize()
        # sself.root.graphrightspace.resize()

        protvalue = self.root.protslider.value
        self.root.protslider.cursor_image = 'meat_cubes.png'
        self.root.glutslider.cursor_image = 'sugar_cubes.png'
        self.root.lipslider.cursor_image = 'olive_oil.png'
        # glutvalue = self.root.glutslider.value
        # lipvalue = self.root.lipslider.value
        #Clock.schedule_interval(self.root.specialwidget.redraw_circles, 1/10)

        return self.root

if __name__ == "__main__":
    testmicropythonApp().run()





