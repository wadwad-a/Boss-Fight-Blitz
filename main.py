# imports
import pygame, random, time

# initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Boss Fight Blitz")
clock = pygame.time.Clock()

# create assets
# icons
kraken_icon = pygame.image.load("assets/icons/KRAKEN-ICON.png")
kraken_icon = pygame.transform.scale(kraken_icon, (200, 200))
robot_icon = pygame.image.load("assets/icons/ROBOT-ICON.png")
robot_icon = pygame.transform.scale(robot_icon, (200, 200))
wizard_icon = pygame.image.load("assets/icons/WIZARD-ICON.png")
wizard_icon = pygame.transform.scale(wizard_icon, (200, 200))
smiley_icon = pygame.image.load("assets/icons/smiley.png")
smiley_icon = pygame.transform.scale(smiley_icon, (50, 50))
# fonts
ithaca_level = pygame.font.Font("assets/fonts/ithaca-LVB75.ttf", 128)
ithaca_player = pygame.font.Font("assets/fonts/ithaca-LVB75.ttf", 92)
# backgrounds
robot_background = pygame.image.load("assets/backgrounds/robot-bg.png")
robot_background = pygame.transform.scale(robot_background, (800, 600))
# weapons
laser = pygame.image.load("assets/weapons/laser.png")
laser = pygame.transform.scale(laser, (50, 600))
laser_blink = pygame.image.load("assets/weapons/blink-laser.png")
laser_blink = pygame.transform.scale(laser_blink, (50, 600))

# laser class
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = laser
        self.rect = self.image.get_rect(midleft=(x, y))

    def update(self):
        pass

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = smiley_icon
        self.rect = self.image.get_rect(center=(100, 300))
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
        self.rect.clamp_ip(screen.get_rect())

# hover effect

menu = True
current_battle = None
kraken_rect = kraken_icon.get_rect(topleft=(100, 200))
robot_rect = robot_icon.get_rect(topleft=(300, 200))
wizard_rect = wizard_icon.get_rect(topleft=(500, 200))

def hover(icon):
    dark = icon.copy()
    dark.fill((int(255 * 0.7), int(255 * 0.7), int(255 * 0.7)), special_flags=pygame.BLEND_RGB_MULT)
    return dark

kraken_dark = hover(kraken_icon)
robot_dark = hover(robot_icon)
wizard_dark = hover(wizard_icon)

laser_group = pygame.sprite.Group()
player = Player()
robot_fight_start_time = None
laser_cycle_time = 2
blink_duration = 0.15
blink_times_needed = 4
blink_times_done = 0
blinking = False
blink_on = False
last_blink_switch = 0
laser_active = False
laser_show_start_time = 0

blink_positions = []
laser_positions = []

# BOSS FIGHTS

# Kraken

def kraken_battle():
    global counter
    global menu, current_battle
    menu = False
    counter = 60
    current_battle = "kraken"
    pygame.display.flip()

# Robot

def robot_battle():
    global counter
    global menu, current_battle, robot_fight_start_time, laser_group
    global blink_times_done, blinking, blink_on, laser_active, laser_show_start_time
    global blink_times_needed, blink_positions, laser_positions
    menu = False
    counter = 60
    current_battle = "robot"
    robot_fight_start_time = time.time()
    laser_group.empty()
    player.rect.center = (100, 300)
    blink_times_done = 0
    blinking = False
    blink_on = False
    laser_active = False
    laser_show_start_time = 0
    blink_times_needed = 4
    blink_positions = []
    laser_positions = []
    pygame.display.flip()

# Wizard

def wizard_battle():
    global counter
    global menu, current_battle
    menu = False
    counter = 60
    current_battle = "wizard"
    pygame.display.flip()

# game loop

running = True
counter = 60
while running:
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if menu and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = pygame.mouse.get_pos()
            if kraken_rect.collidepoint(mouse):
                kraken_battle()
            elif robot_rect.collidepoint(mouse):
                robot_battle()
            elif wizard_rect.collidepoint(mouse):
                wizard_battle()

    if menu:
        if counter % 60 == 0:
            pygame.Surface.fill(screen, (r, g, b))
            if r < 75 and g < 75:
                screen.blit(ithaca_level.render("Level Select", True, (255, 255, 255)), (153, 25))
                screen.blit(ithaca_player.render("Player Select", True, (255, 255, 255)), (200, 350))
            else:
                screen.blit(ithaca_level.render("Level Select", True, (0, 0, 0)), (153, 25))
                screen.blit(ithaca_player.render("Player Select", True, (0, 0, 0)), (200, 350))
        counter += 1

        # menu hover
        mouse = pygame.mouse.get_pos()
        if kraken_rect.collidepoint(mouse):
            screen.blit(kraken_dark, (100, 150))
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                kraken_battle()
        else:
            screen.blit(kraken_icon, (100, 150))
        if robot_rect.collidepoint(mouse):
            screen.blit(robot_dark, (300, 150))
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                robot_battle()
        else:
            screen.blit(robot_icon, (300, 150))
        if wizard_rect.collidepoint(mouse):
            screen.blit(wizard_dark, (500, 150))
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                wizard_battle()
        else:
            screen.blit(wizard_icon, (500, 150))
    else:
        if current_battle == "robot":
            elapsed = time.time() - robot_fight_start_time

            if elapsed > 60:
                menu = True
                current_battle = None
                laser_group.empty()
            else:
                now = time.time()

                if not blinking and not laser_active and (elapsed // laser_cycle_time) > blink_times_done:
                    blinking = True
                    blink_on = True
                    last_blink_switch = now
                    blink_times_done += 1

                    blink_positions = []
                    attempts = 0
                    max_attempts = 100
                    count = 1
                    if 5 <= blink_times_done <= 11:
                        count = 2
                    elif blink_times_done >= 12:
                        count = 3
                    while len(blink_positions) < count and attempts < max_attempts:
                        x = random.randint(0, 750)
                        if all(abs(x - px) >= 50 for px in blink_positions):
                            blink_positions.append(x)
                        attempts += 1

                if blinking:
                    if now - last_blink_switch > blink_duration:
                        blink_on = not blink_on
                        last_blink_switch = now
                        if not blink_on:
                            blink_times_needed -= 1
                        if blink_times_needed <= 0:
                            blinking = False
                            laser_active = True
                            laser_group.empty()

                            laser_positions = blink_positions.copy()

                            for x in laser_positions:
                                new_laser = Laser(x, 300)
                                laser_group.add(new_laser)

                            laser_show_start_time = now
                            blink_times_needed = 4

                if laser_active and now - laser_show_start_time > 1:
                    laser_active = False
                    laser_group.empty()

                laser_group.update()
                keys = pygame.key.get_pressed()
                player.update(keys)

                screen.blit(robot_background, (0, 0))

                if blinking and blink_on:
                    for pos in blink_positions:
                        screen.blit(laser_blink, (pos, 0))
                elif laser_active:
                    laser_group.draw(screen)

                screen.blit(player.image, player.rect)

                if laser_active:
                    if pygame.sprite.spritecollideany(player, laser_group):
                        menu = True
                        current_battle = None
                        laser_group.empty()

        elif current_battle == "kraken":
            screen.fill((0, 0, 128))
        elif current_battle == "wizard":
            screen.fill((128, 0, 128))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()