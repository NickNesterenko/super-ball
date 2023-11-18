import pygame
from random import randrange, randint
import time
import pygame_menu

pygame.init()
surface = pygame.display.set_mode((500, 500))


pygame.init()
win = pygame.display.set_mode((500, 500))
bg_color = (255, 255, 255)
image3 = pygame.font.SysFont('Arial', 40).render("BUT DONT GIVE UP!", True, (0, 0, 0))


# Створюю класс Area
class Area():
    # Конструктор
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    # Колізія по кліку
    def collide_point(self, x, y):
        return self.rect.collidepoint(x, y)

    def collide_rect(self, rect):
        return self.rect.colliderect(rect)


# Клас картинка
class Picture(Area):
    def __init__(self, pict, x, y, width, height, xx, yy):
        Area.__init__(self, x, y, width, height)
        self.sh_x = xx
        self.sh_y = yy
        self.pict = pygame.image.load(pict)

    # Відображення спрайта
    def draw(self):
        self.rect = pygame.Rect(self.x + self.sh_x, self.y + self.sh_y, self.width, self.height)
        win.blit(self.pict, (self.x, self.y))

    def collision(self):
        global moving, move_type, monsters, point
        for i in monsters:
            if self.collide_rect(i.rect):
                if move_type == 'up_right' or move_type == 'down_right':
                    move_type = 'down_left'
                elif move_type == 'up_left' or move_type == 'down_left':
                    move_type = 'down_right'
                monsters.remove(i)
                point += 1


# Змінні для роботи програми
monsters = []
#ball1 = Picture('enemy.png', 200, 340, 92, 20, 40, 2)
ball = Picture('больно-в-ноге.jpg', 200, 300, 56, 45, -40, 2)
player = Picture('палочка.png', 150, 350, 92, 20, 4, 2)

# Об'єкти границі ігрового поля
up = pygame.Rect(0, 1, 500, 1)
left = pygame.Rect(1, 0, 1, 500)
right = pygame.Rect(499, 0, 1, 500)

point = 0

level1_xy = [[140, 0], [195, 25], [250, 0], [80, 50], [300, 50], [135, 100], [245, 100], [190, 150]]
level2_xy = [[140, 0], [290, 0], [90, 50], [140, 50], [190, 75], [240, 75], [290, 50], [340, 50], [90, 100], [140, 100], [290, 100], [90, 150], [340, 150]]
level3_xy = [[165, 0], [215, 0], [265, 0], [315, 0], [365, 0], [265, 50], [165, 100], [15, 150]]

moving = ['down_left', 'down_right', 'up_left', 'up_right']
move_type = ''
level = 0
Game_end_result = 0

righ = False
lef = False


# рух м'ячика
if ball.collide_rect(up):
    if move_type == 'up_left':
        move_type = 'down_left'
    if move_type == 'up_right':
        move_type = 'down_right'
    if ball.collide_rect(left):
        if move_type == 'up_left':
            move_type = 'up_right'
        if move_type == 'down_left':
            move_type = 'down_right'
        if ball.collide_rect(right):
            if move_type == 'up_right':
                move_type = 'up_left'
        if move_type == 'down_right':
            move_type = 'down_left'
        if ball.collide_rect(player.rect):
            if move_type == 'down_left':
                move_type = 'up_left'
        if move_type == 'down_right':
            move_type = 'up_right'
            
        if ball.rect.y > player.y + 40:
            Game_end_result = 2 # end game
        if move_type == 'up_right':
            ball.x += 10
            ball.y -= 10
        if move_type == 'up_left':
            ball.x -= 10
            ball.y -= 10
        if move_type == 'down_right':
            ball.x += 10
            ball.y += 10
        if move_type == 'down_left':
            ball.x -= 10
            ball.y += 10
            ball.draw()

def movement():
    global lef, righ, Game_end_result
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player.x - 7 > -8:
        player.x -= 8
    if keys[pygame.K_RIGHT] and player.x + 7 < 408:
        player.x += 8
    if keys[pygame.K_a] and player.x - 7 > -8:
        player.x -= 8
    if keys[pygame.K_d] and player.x + 7 < 408:
        player.x += 8
    if keys[pygame.K_q]:
        Game_end_result = 2 # end game


def pause():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                k = False
                text_ = pygame.font.SysFont('Arial', 100).render('PAUSE', True, (0, 0, 0))
                while k == False:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                k = True

                    win.blit(text_, (150, 150))
                    pygame.display.update()
                    clock = pygame.time.Clock()
                    clock.tick(60)


def main(leve):
    global win, lef, righ, point, ball, player, monsters, Game_end_result, num, level, move_type, bg_color

    Game_end_result = 0
    q = 3.9

    while q >= 1:
        t1 = time.time()
        hf = pygame.font.SysFont('Arial', 80).render(str(int(q)), True, (0, 0, 0))
        win.fill(bg_color)
        for i in monsters:
            i.draw()
        player.draw()
        ball.draw()
        #ball1.draw()
        win.blit(hf, (240, 230))
        t2 = time.time()
        q -= (t2 - t1) * 10
        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(60)
        pause()
    
    move_type = moving[randrange(2, 4)]

    while Game_end_result == 0:  #game over
        points = pygame.font.SysFont('Arial', 40).render(f'{point}/{monsters}', True, (0, 0, 0))
        lev = pygame.font.SysFont('Arial', 40).render(str(leve), True, (0, 0, 0))
    
        win.fill(bg_color)
        win.blit(points, (400, 400))
        win.blit(lev, (0, 400))
        for i in monsters:
            i.draw()
        player.draw()
        # рух м'ячика
        ball.collision()

        if monsters == []:
            Game_end_result = 1  # Win

        movement()
        pause()
        pygame.display.update()

        clock.tick(60)

    if Game_end_result == 1:
        image = pygame.font.SysFont('Arial', 40).render('ТИ ВИГРАВ!', True, (0, 0, 0))
        image2 = pygame.font.SysFont('Arial', 40).render('      ПОЗДРАВЛЯЕМ!', True, (0, 0, 0))
        level += 1
    if Game_end_result == 2:
        image = pygame.font.SysFont('Arial', 40).render('ТИ ПРОГРАВ!', True, (0, 0, 0))
        image2 = pygame.font.SysFont('Arial', 40).render("      НО НЕ СДАВАЙСЯ!", True, (0, 0, 0))
    pause()
    keys = pygame.key.get_pressed()

    win.fill(bg_color)
    win.blit(image, (180, 120))
    win.blit(image2, (100, 155))
    pygame.display.update()        
    
game_difficulty = 1

def set_difficulty(value, difficulty):
    global game_difficulty
    game_difficulty = difficulty
    return game_difficulty


def main_game():
    global game_difficulty, level, Game_end_result

    level = 1
    Game_end_result = 0

    while Game_end_result != 2 and level <= game_difficulty: # game over
        keys = pygame.key.get_pressed()
        if keys[pygame.QUIT] == 1:
            break

        point = 0
        player.x = 150
        ball.x = 200
        ball.y = 300
        
        def ball_collision():
            global move_type, Game_end_result

        # random_monster = ["милий-монстр.jpg", "слаймовий-монстр.png", "трол фейс.png", "камений монстр.jpg", "язичник.jpg", "18333.png", "зефирный монстр.jpg", "адовий-монстр.jpg"][randint(0, 6)]
        
    if level == 1:
        for i in range(len(level1_xy)):
            random_monster = ["милий-монстр.jpg", "слаймовий-монстр.png", "трол фейс.png", "камений монстр.jpg", "язичник.jpg", "18333.png", "зефирный монстр.jpg", "адовий-монстр.jpg"][randint(0, 7)]
            m = Picture(random_monster, level1_xy[i][0], level1_xy[i][1], 48, 42, 1, 4)
            monsters.append(m)
            
    if level == 2:
        for i in range(len(level2_xy)):
            random_monster = ["милий-монстр.jpg", "слаймовий-монстр.png", "трол фейс.png", "камений монстр.jpg", "язичник.jpg", "18333.png", "зефирный монстр.jpg", "адовий-монстр.jpg"][randint(0, 7)]
            m = Picture(random_monster, level2_xy[i][0], level2_xy[i][1], 48, 42, 1, 4)
            monsters.append(m)

    if level == 3:
        for i in range(len(level3_xy)):
            random_monster = ["милий-монстр.jpg", "слаймовий-монстр.png", "трол фейс.png","камений монстр.jpg", "язичник.jpg",  "18333.png", "зефирный монстр.jpg", "адовий-монстр.jpg"][randint(0, 7)]
            m = Picture(random_monster, level3_xy[i][0], level3_xy[i][1], 48, 42, 1, 4)
            monsters.append(m)
            
    main('LEVEL : ' + str(level))

    print("level: " + str(level))
    print("dif: " + str(game_difficulty))
    print("res: " + str(Game_end_result))
    time.sleep(3)

    image = pygame.font.SysFont('Arial', 40).render('ТИ ВИГРАВ!', True, (0, 0, 0))
    image2 = pygame.font.SysFont('Arial', 40).render('      ПОЗДРАВЛЯЕМ!', True, (0, 0, 0))


menu = pygame_menu.Menu('Welcome in arkanoid', 500, 500, theme=pygame_menu.themes.THEME_BLUE)
menu.add.text_input('Name :', default='Arkanoid')
menu.add.selector('Difficulty :', [('Easy', 1), ('Medium', 2), ('Hard', 3)], onchange=set_difficulty)
menu.add.button('Play', main_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface)


