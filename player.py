import pygame
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y, forward_angle):
        super().__init__()
        self.width = 100
        self.height = 50
        self.forward_angle = forward_angle  # y -  x +
        self.image_source = pygame.image.load("static/images/car.png").convert()
        self.image = pygame.transform.scale(self.image_source, (self.width, self.height))
        self.image = pygame.transform.rotate(self.image, -self.forward_angle)
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.center = (center_x, center_y)
        self.last_time = pygame.time.get_ticks()  # return tick  /ms
        self.delta_time = 0  # time range
        self.move_velocity_limit = 220  # max velocity
        self.move_velocity = 0  # move speed
        self.move_acc = 600  # acceleration 600
        self.rotate_velocity_limit = 140
        self.rotate_velocity = 0
        self.friction = 0.9

        self.crash_sound = pygame.mixer.Sound("static/sounds/crash.mp3")
        self.crash_sound.set_volume(0.1)

        self.move_sound = pygame.mixer.Sound("static/sounds/move.mp3")
        self.move_sound.set_volume(0.1)
        self.move_voice_channel = pygame.mixer.Channel(7)

    def update_delta_time(self):
        cur_time = pygame.time.get_ticks()
        self.delta_time = (cur_time - self.last_time) / 1000  # ms to s
        self.last_time = cur_time

    def input(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
            self.move_velocity += self.move_acc * self.delta_time
            self.move_velocity = min(self.move_velocity, self.move_velocity_limit)
            if not self.move_voice_channel.get_busy():
                self.move_voice_channel.play(self.move_sound)
        elif key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
            self.move_velocity -= self.move_acc * self.delta_time
            if not self.move_voice_channel.get_busy():
                self.move_voice_channel.play(self.move_sound)
            self.move_velocity = max(self.move_velocity, -self.move_velocity_limit)
        else:
            self.move_velocity = int(self.move_velocity * self.friction)
            if self.move_voice_channel.get_busy():
                self.move_voice_channel.stop()
        sign = 1
        if self.move_velocity < 0:
            sign = -1
        if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
            self.rotate_velocity = self.rotate_velocity_limit * sign
        elif key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
            self.rotate_velocity = -self.rotate_velocity_limit * sign
        else:
            self.rotate_velocity = 0

    def rotate(self, direction=1):
        self.forward_angle += self.rotate_velocity * self.delta_time * direction
        self.image = pygame.transform.scale(self.image_source, (self.width, self.height))
        self.image = pygame.transform.rotate(self.image, -self.forward_angle)
        self.image.set_colorkey("black")
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def move(self, direction=1):
        if direction == 1 and abs(self.move_velocity) > 50:
            self.rotate(direction)
        vx = self.move_velocity * math.cos(math.pi * self.forward_angle / 180) * direction
        vy = self.move_velocity * math.sin(math.pi * self.forward_angle / 180) * direction
        self.rect.x += vx * self.delta_time
        self.rect.y += vy * self.delta_time
        if direction == -1 and abs(self.move_velocity) > 50:
            self.rotate(direction)

    def crashed(self):
        self.crash_sound.play()
        self.move(-1) # crash back
        if self.move_velocity >= 0:
            self.move_velocity = max(-self.move_velocity, -100)
        else:
            self.move_velocity = max(self.move_velocity, 100)
        self.rotate_velocity *= -1

    def update(self):
        self.update_delta_time()
        self.input()
        self.move()
