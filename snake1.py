# Ctrl + Shift + P, then select interpreter
# Choose an interpreter that works
import pygame
import random

# Game settings
GAME_SIZE = 800
BLOCK_SIZE = GAME_SIZE / 40
GAP_SIZE = GAME_SIZE * 0.002
APPLE_COLOR = (255, 28, 202)
BACKGROUND_COLOR = (19, 19, 158)
COLOR1 = (106, 255, 77)
COLOR2 = (77, 255, 136)
COLOR3 = (77, 255, 225)
COLOR4 = (77, 225, 255)
COLOR5 = (77, 195, 255)
COLOR6 = (77, 136, 255)
FRAMES_PER_SECOND = 10
SNAKE_SPEED = 7

pygame.init()
clock = pygame.time.Clock()
game_display = pygame.display.set_mode((GAME_SIZE, GAME_SIZE))
score_font = pygame.font.SysFont('Arial', int(GAME_SIZE * 0.065), True)
title_font = pygame.font.SysFont('Arial', int(GAME_SIZE * 0.3), True)
pygame.display.set_caption('SNAKE!')

class Color_Cycler():
    def __init__ (self, *colors):
        self.colors = []
        for color in colors:
            self.colors.append(color)
        self.cycle_count = 1
        self.color_change_frequency = 3
    def get_next_color(self):
        if self.cycle_count == self.color_change_frequency:
            self.cycle_count = 0
        else:
            self.cycle_count += 1
            
        if self.cycle_count == 0:
            next_color = self.color.pop()
            self.colors.insert(0, next_color)
            return next_color
        else:
            return self.color[0]
   
class Game_Object():
    def __init__(self, xcor,ycor, color):
        self.xcor = xcor
        self.ycor = ycor
        self.color = color
    def show_as_circle(self):
       pygame.draw.circle(game_display, self.color, (int(self.xcor + BLOCK_SIZE/ 2,), int(self.ycor + BLOCK_SIZE/2)), int(BLOCK_SIZE / 2))
    def show_as_square(self):  
        pygame.draw.rect(game_display, self.color, pygame.Rect(self.xcor + GAP_SIZE, self.ycor + GAP_SIZE, BLOCK_SIZE - GAP_SIZE * 2, BLOCK_SIZE - GAP_SIZE * 2))

class Snake():
    # This is the constructor
    def __init__(self, xcor, ycor):
        self.is_alive = True
        self.score = 0
        self.direction = "RIGHT"
        self.body = [ Game_Object(xcor, ycor, COLOR3),
                     Game_Object(xcor - BLOCK_SIZE, ycor, COLOR1),
                     Game_Object(xcor - BLOCK_SIZE* 2, ycor, COLOR5)]
        self.previous_last_tail = self.body[len(self.body) -1]
        self.color_counter = 0
    def grow(self):
        self.body.append(self.previous_last_tail)
    def show(self):
        for body_part in self.body:
            body_part.show_as_square()
    def set_direction_right(self):
        if self.direction != "LEFT":
            self.direction = "RIGHT"
    def set_direction_left(self):
        if self.direction != "RIGHT":
            self.direction = "LEFT"
    def set_direction_up(self):
        if self.direction != "DOWN":
            self.direction = "UP"
    def set_direction_down(self):
        if self.direction != "UP":
            self.direction = "DOWN"
    def move(self, color_cycler):
        head_xcor = self.body[0].xcor
        head_ycor = self.body[0].ycor
        if self.direction == "RIGHT":
            head_xcor = head_xcor + BLOCK_SIZE
        elif self.direction == "LEFT":
            head_xcor = head_xcor - BLOCK_SIZE
        elif self.direction == "UP":
            head_ycor = head_ycor - BLOCK_SIZE
        elif self.direction == "DOWN":
            head_ycor = head_ycor + BLOCK_SIZE
            
        self.body.insert(0, Game_Object(head_xcor, head_ycor, color_cycler.get_next_color()))
        self.previous_last_tail = self.body.pop()
    def cycle_colors(self, color_cycler):
        for i in range(len(self.body)-1, 0, -1):
            self.body[i].color = self.body[i-1].color
        self.body[0].color = color_cycler.get_next_color()
    def has_collided_with_wall(self):
        head = self.body[0]
        if head.xcor < 0 or head.ycor < 0 or head.xcor + BLOCK_SIZE > GAME_SIZE or head.ycor + BLOCK_SIZE > GAME_SIZE:
            return True
        return False
    def has_eaten_apple(self, apple_in_question):
        head = self.body[0]
        if head.xcor == apple_in_question.body.xcor and head.ycor == apple_in_question.body.ycor:
            return True
        return False
    def has_collided_with_itself(self):
        head = self.body[0]
        for i in range(1, len(self.body)):
            if head.xcor == self.body[i].xcor and head.ycor == self.body[i].ycor:
                return True
        return False

class Apple():
    def __init__(self, snake_body):
        self.body = self.get_randomly_positioned_game_object()

        while self.apple_is_on_snake(snake_body):
            self.body = self.get_randomly_positioned_game_object()

    def get_randomly_positioned_game_object(self):
        xcor = random.randrange(0, GAME_SIZE / BLOCK_SIZE) * BLOCK_SIZE
        ycor = random.randrange(0, GAME_SIZE / BLOCK_SIZE) * BLOCK_SIZE
        return Game_Object(xcor, ycor, APPLE_COLOR) 
    def apple_is_on_snake(self, snake_body):
        for snake_part in snake_body:
            if snake_part.xcor == self.body.xcor and snake_part.ycor == self.body.ycor:
                return True
        return False 
    def show(self):
        self.body.show_as_circle()

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            snake.is_alive = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake.set_direction_left()
            elif event.key == pygame.K_RIGHT:
                snake.set_direction_right()
            elif event.key == pygame.K_UP:
                snake.set_direction_up()
            elif event.key == pygame.K_DOWN:
                snake.set_direction_down()
            elif event.key == pygame.K_SPACE:
                pause_game()

def pause_game():
    game_is_paused = True
    while game_is_paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                snake.is_alive = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_is_paused = False
        pygame.display.update()
        clock.tick(5)

color_cycler = Color_Cycler(COLOR1, COLOR2, COLOR3, COLOR4, COLOR5, COLOR6)
snake = Snake(BLOCK_SIZE * 5, BLOCK_SIZE * 5)
apple = Apple(snake.body)

#Title screen
show_title_screen = True
while show_title_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            snake.is_alive = False
            show_title_screen = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                show_title_screen = False
   
    title_text = title_font.render('SNAKE',False,(APPLE_COLOR))
    game_display.blit(title_text, (GAME_SIZE / 2 - title_text.get_width() / 2,GAME_SIZE / 2 - title_text.get_height()/ 2))
    pygame.display.flip()
    clock.tick(FRAMES_PER_SECOND)


# Main Game Loop
frame_counter = 0
while snake.is_alive:

    handle_events()

    game_display.blit(game_display, (0, 0))

    if frame_counter % max(1, FRAMES_PER_SECOND // SNAKE_SPEED) == 0:
        snake.move(color_cycler)
        if snake.has_collided_with_wall() or snake.has_collided_with_itself():
            snake.is_alive = False

        if snake.has_eaten_apple(apple):
            snake.score += 1
            snake.grow()
            apple = Apple(snake.body)
            SNAKE_SPEED += 0.2
            
    game_display.fill(BACKGROUND_COLOR)
    snake.show()
    apple.show()
    frame_counter += 1
    snake.cycle_colors(color_cycler)

    score_text = score_font.render(str(snake.score),False,(255,255,255))
    game_display.blit(score_text, (0,0))
    pygame.display.set_caption('SNAKE! Score = ' + str(snake.score))

    pygame.display.flip()
    clock.tick(FRAMES_PER_SECOND)
    
    if snake.is_alive == False:
        FRAMES_PER_SECOND = 0.5
    
pygame.display.quit()
pygame.quit()