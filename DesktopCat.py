from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt, QTimer, QPoint, QPropertyAnimation
from PyQt5.QtGui import QMovie
import random

# Creating a Label that will contain the gifs
class DesktopCat(QLabel):
    def __init__(self):
        super().__init__()
        self.direction = 1 # Starting on the right

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint) # Always on top of other tabs
        self.setAttribute(Qt.WA_TranslucentBackground) # Transparent backgroung
        
        self.set_animation() # Start the animation of the cat
        self.set_drag() # Initiates Qpoint
        self.set_actions() # Initiates the action timer

        self.move(100, 200) # Starting pos

        # Action flags
        self.idle = False
        self.standing = False
        self.done = False
        self.walking = False
        self.turn = False
        self.up = False
        self.down = False
        self.a = 1
        self.tired = False
        self.total = 2000
        self.energy = 2000
        self.sleepy = 0
        self.sleep = False
        self.sleeping = False
        self.sleeping_time = 0
        self.wakeup = False
        self.first = False
        self.choose = True

    def set_animation(self):
        if self.direction == 1:
            self.movie = QMovie("assets/idle_right.gif")
            self.setMovie(self.movie)
            self.movie.start()
        if self.direction == -1:
            self.movie = QMovie("assets/idle_left.gif")
            self.setMovie(self.movie)
            self.movie.start()

    def set_drag(self):
        self.drag_pos = QPoint()
        self.draggable = True

    def set_actions(self):
        self.action_timer = QTimer(self)
        self.action_timer.timeout.connect(self.trigger_action)
        self.action_timer.start(3000)


    def mousePressEvent(self, event):
        if self.draggable:
            self.drag_pos = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self.draggable:
            self.move(event.globalPos() - self.drag_pos)

    def trigger_action(self):
        actions = []

        if self.a == 0 or self.tired and self.choose:
            self.down = True
            self.up = False
            self.walking = False
            self.done = False
            self.tired = False
            self.choose = False
        if self.a == 1 and not self.tired and not self.walking and not self.standing and self.choose:
            self.idle = False
            self.up = True
            self.down = False
            self.done = False
            self.choose = False

        if self.idle and not self.done and not self.sleep:
            actions.append(self.idle_anim)
            actions.append(self.lick_anim) 
        elif self.up and not self.done and not self.sleep:
            actions.append(self.get_up_anim)
        elif self.down and  not self.done and not self.sleep:
            actions.append(self.get_down_anim)
        elif self.standing and not self.done and not self.idle and not self.turn and not self.sleep:
            actions.append(self.walk_anim)
        elif self.standing and not self.done and not self.idle and self.turn and not self.sleep:
            actions.append(self.turn_anim)
        elif self.sleep and not self.sleeping and not self.wakeup:
            actions.append(self.sleep_anim)
        elif self.sleeping and not self.wakeup:
            actions.append(self.sleeping_anim)
        elif self.wakeup:
            actions.append(self.wake_up_anim)
        elif self.walking and not self.turn and not self.sleep:
            actions.append(self.set_walk)

        if not self.done or self.walking:
            random.choice(actions)()


# Actions
    def sleep_anim(self):
        self.action_timer.start(1000) # Time interval of the gif

        if self.direction == 1:
            new_movie = QMovie("assets/sleeping_right.gif")
        if self.direction == -1:
            new_movie = QMovie("assets/sleeping_left.gif")

        self.setMovie(new_movie)
        new_movie.start()
        self.sleeping = True

    def sleeping_anim(self):
        self.action_timer.start(6000)

        if self.direction == 1:
            new_movie = QMovie("assets/sleep_right.gif")
        if self.direction == -1:
            new_movie = QMovie("assets/sleep_left.gif")

        if self.sleeping_time >= 6:
            self.wakeup = True
        else:    
            self.sleeping_time += 1

        self.setMovie(new_movie)
        new_movie.start()

    def wake_up_anim(self):
        self.action_timer.start(1000)

        if self.direction == 1:
            new_movie = QMovie("assets/wake_right.gif")
        if self.direction == -1:
            new_movie = QMovie("assets/wake_left.gif")

        self.setMovie(new_movie)
        new_movie.start()

        self.sleepy = 0
        self.sleep = False
        self.sleeping = False
        self.sleeping_time = 0
        self.wakeup = False

    def get_up_anim(self):
        self.action_timer.start(900)

        if self.direction == 1:
            new_movie = QMovie("assets/up_right.gif")
        if self.direction == -1:
            new_movie = QMovie("assets/up_left.gif")

        self.setMovie(new_movie)
        new_movie.start()
        self.standing = True
        self.idle = False
        self.up = False

    def idle_anim(self):
        self.action_timer.start(3000)

        if self.direction == 1:
            new_movie = QMovie("assets/idle_right.gif")
        if self.direction == -1:
            new_movie = QMovie("assets/idle_left.gif")

        self.setMovie(new_movie)
        new_movie.start()
        self.done = True
        if self.energy >= self.total:
            self.a = 1
            self.choose = True
        else:
            self.energy += 100

        if self.sleepy >= 5:
            self.sleep = True

        if self.first:
            self.sleepy += 1
            self.first = False

    def lick_anim(self):
        self.action_timer.start(4000)

        if self.direction == 1:
            new_movie = QMovie("assets/lick_right.gif")
        if self.direction == -1:
            new_movie = QMovie("assets/lick_left.gif")

        self.setMovie(new_movie)
        new_movie.start()

        if self.energy >= self.total:
            self.a = 1
            self.choose = True
        else:
            self.energy += 100

    def get_down_anim(self):
        self.action_timer.start(900)

        if self.direction == 1:
            new_movie = QMovie("assets/down_right.gif")
        if self.direction == -1:
            new_movie = QMovie("assets/down_left.gif")

        self.setMovie(new_movie)
        new_movie.start()
        self.standing = False
        self.idle = True
        self.down = False

    def walk_anim(self):
        self.action_timer.start(400)

        if self.direction == 1:
            new_movie = QMovie("assets/walking_right.gif")
        if self.direction == -1:
            new_movie = QMovie("assets/walking_left.gif")

        self.setMovie(new_movie)
        new_movie.start()
        self.done = True
        self.walking = True

    def turn_anim(self):
        self.action_timer.start(500)

        if self.direction == 1:
            new_movie = QMovie("assets/left_right.gif")
        if self.direction == -1:
            new_movie = QMovie("assets/right_left.gif")

        self.setMovie(new_movie)
        new_movie.start()
        self.walking = True
        self.turn = False       

    def set_walk(self):
        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.update_pos)
        self.move_timer.start(20) # Set a different timer for the update_pos
    def update_pos(self):
        new_x = self.x() + (1 * self.direction) # Calculate the x position every step
        self.energy -= 1
        if self.energy <= 0:
            self.tired = True
            self.first = True
            self.a = 0
            self.choose = True
            self.move_timer.stop()

        screen_width = QApplication.desktop().width()
        if new_x < 0 or new_x > screen_width - self.width(): # Screen boundaries
            self.direction *= -1
            self.done = False
            self.turn = True
            self.walking = False
            self.move_timer.stop()
        self.move(new_x, self.y()) # Update x position

# Note: Since there's no specification of a parent widget, QLabel
# will be interpreted as a independent window.

app = QApplication([])
pet = DesktopCat()
pet.show()
app.exec_()
