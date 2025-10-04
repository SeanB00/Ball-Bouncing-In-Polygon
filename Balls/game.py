# Example file showing a circle moving on screen
import math
import time

import pygame

W = 1280
H = 720
GAP = 8
actual_height = 15
g = 9.8 * H / actual_height
# pygame setup
pygame.init()
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
running = True
dt = 0
num_collisions = 0

class ball:
    def __init__(self, pos, v, color, r):
        self.pos = pos
        self.v = v
        self.color = color
        self.r = r

    def movement(self):
        self.pos += self.v * dt
        self.v.y += g * dt


def is_to_the_left(v1, v2):
    # use built in cross
    return v1.x * v2.y - v1.y * v2.x > 0


class polygon:
    def __init__(self, center_pos, num_sides, r):
        self.center_pos = center_pos
        self.num_sides = num_sides
        self.alpha = 2 * math.pi / num_sides
        self.starting_angle = self.alpha / 2
        self.r = r
        self.points = self.get_points()
        self.collision_vec = None
        self.inside = True

    def get_points(self):
        points = []
        for i in range(self.num_sides):
            theta = self.starting_angle + self.alpha * i
            # use built in rotation
            x = self.center_pos.x + self.r * math.cos(theta)
            y = self.center_pos.y + self.r * math.sin(theta)
            points.append(pygame.Vector2(x, y))
        return points

    def is_point_inside(self, point):
        for i in range(self.num_sides):
            p = self.points[(i + 1) % self.num_sides] - self.points[i]
            q = point - self.points[i]
            if not is_to_the_left(p, q):
                self.collision_vec = p
                return False
        return True

    def is_ball_inside(self, b):
        points_to_check = 8
        vec = pygame.Vector2(b.r + GAP, 0)
        angle = 2 * math.pi / points_to_check
        for i in range(points_to_check):
            if not self.is_point_inside(b.pos + vec):
                return False
            vec = vec.rotate_rad(angle)
        return True

    def flip_ball_vel(self, b):

        # orthogonal projection

        if self.collision_vec is None:
            return
        pv = (b.v.dot(self.collision_vec.normalize())) * self.collision_vec.normalize()
        rv = 2 * pv - b.v
        b.v = rv

    def handle_movement(self, b):
        b.movement()
        if not self.is_ball_inside(b):
            self.flip_ball_vel(b)
            while not self.is_ball_inside(b):
                b.pos += b.v * dt
            global num_collisions
            self.grow()
            num_collisions += 1


    def grow(self):
        self.num_sides = self.num_sides + 1
        self.alpha = 2 * math.pi / self.num_sides
        self.points = self.get_points()


b = ball(pygame.Vector2(W / 2, H / 2), pygame.Vector2(0, 0), "green", 30)

p = polygon(pygame.Vector2(W / 2, H / 2), 3, 300)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    p.handle_movement(b)
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    keys = pygame.key.get_pressed()

    pygame.draw.circle(screen, b.color, b.pos, b.r)
    print(p.points)
    pygame.draw.polygon(screen, "blue", p.points, 3)

    # Define font and text
    font = pygame.font.Font(None, 50)  # None uses the default font, 50 is the size
    text_surface = font.render(f"Number of collisions: {num_collisions}", True, (255, 255, 255))  # White color
    screen.blit(text_surface, (W/10, H/10))


    # flip() the display to put your work on screen
    pygame.display.flip()
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
