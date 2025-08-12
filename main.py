# imports
import pygame, random, time, math

# initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Boss Fight Blitz")
clock = pygame.time.Clock()

# create assets
# icons
# level select
kraken_icon = pygame.image.load("assets/icons/KRAKEN-ICON.png")
kraken_icon = pygame.transform.scale(kraken_icon, (200, 200))
robot_icon = pygame.image.load("assets/icons/ROBOT-ICON.png")
robot_icon = pygame.transform.scale(robot_icon, (200, 200))
wizard_icon = pygame.image.load("assets/icons/WIZARD-ICON.png")
wizard_icon = pygame.transform.scale(wizard_icon, (200, 200))
# player select
smiley_icon = pygame.image.load("assets/icons/smiley.png")
smiley_icon = pygame.transform.scale(smiley_icon, (50, 50))
cookie_icon = pygame.image.load("assets/icons/cookie.png")
cookie_icon = pygame.transform.scale(cookie_icon, (50, 50))
crazy_icon = pygame.image.load("assets/icons/crazy.png")
crazy_icon = pygame.transform.scale(crazy_icon, (50, 50))
heart_icon = pygame.image.load("assets/icons/heart.png")
heart_icon = pygame.transform.scale(heart_icon, (50, 50))
penny_icon = pygame.image.load("assets/icons/penny.png")
penny_icon = pygame.transform.scale(penny_icon, (50, 50))
# fonts
ithaca_level = pygame.font.Font("assets/fonts/ithaca-LVB75.ttf", 128)
ithaca_player = pygame.font.Font("assets/fonts/ithaca-LVB75.ttf", 92)
ithaca_hover = pygame.font.Font("assets/fonts/ithaca-LVB75.ttf", 30)
ithaca_desc = pygame.font.Font("assets/fonts/ithaca-LVB75.ttf", 20)
# music
cyberblade = pygame.mixer.music.load("assets/music/cyberblade.mp3")
# backgrounds
robot_background = pygame.image.load("assets/backgrounds/robot-bg.png")
robot_background = pygame.transform.scale(robot_background, (800, 600))
wizard_background = pygame.image.load("assets/backgrounds/wizard-bg.png")
wizard_background = pygame.transform.scale(wizard_background, (800, 600))
# weapons
laser = pygame.image.load("assets/weapons/laser.png")
laser = pygame.transform.scale(laser, (50, 600))
laser_blink = pygame.image.load("assets/weapons/blink-laser.png")
laser_blink = pygame.transform.scale(laser_blink, (50, 600))
wand_img = pygame.image.load("assets/weapons/wand.png").convert_alpha()
wand_img = pygame.transform.scale(wand_img, (25, 150))

# laser class
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = laser
        self.rect = self.image.get_rect(midleft=(x, y))

    def update(self):
        pass

class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
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

player_icons = [smiley_icon, cookie_icon, crazy_icon, heart_icon, penny_icon]
player_names = ["Smiley", "Cookie", "Crazy", "Heart", "Penny"]
player_descs = ["default", "yum", "what", "quite lovely", "woah i'm rich"]
icon_size = 50
spacing = 30  # space between icons
num_icons = len(player_icons)
total_width = num_icons * icon_size + (num_icons - 1) * spacing
start_x = (800 - total_width) // 2  # 800 is the screen width

player_rects = []
for i in range(num_icons):
    x = start_x + i * (icon_size + spacing)
    player_rects.append(player_icons[i].get_rect(topleft=(x, 420)))

def hover(icon):
    dark = icon.copy()
    dark.fill((int(255 * 0.7), int(255 * 0.7), int(255 * 0.7)), special_flags=pygame.BLEND_RGB_MULT)
    return dark

kraken_dark = hover(kraken_icon)
robot_dark = hover(robot_icon)
wizard_dark = hover(wizard_icon)

laser_group = pygame.sprite.Group()

selected_player = 0
player = Player(player_icons[selected_player])
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

# WAND AND PROJECTILE CLASSES FOR WIZARD FIGHT

class Wand(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, side):
        super().__init__()
        self.original_image = wand_img
        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.rect = self.image.get_rect()
        self.angle = angle
        self.spawn_time = time.time()
        self.has_fired = False
        self.side = side

        # Position wand partially embedded offscreen based on side
        if side == "left":
            self.rect.center = (-self.rect.width // 2, y)
        elif side == "right":
            self.rect.center = (800 + self.rect.width // 2, y)
        elif side == "top":
            self.rect.center = (x, -self.rect.height // 2)
        elif side == "bottom":
            self.rect.center = (x, 600 + self.rect.height // 2)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        length = 800
        width = 20
        self.original_image = pygame.Surface((length, width), pygame.SRCALPHA)
        pygame.draw.rect(self.original_image, (255, 255, 0), self.original_image.get_rect())
        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = angle
        self.speed = 20
        self.spawn_time = time.time()

    def update(self):
        dx = self.speed * math.cos(math.radians(self.angle))
        dy = self.speed * math.sin(math.radians(self.angle))
        self.rect.x += dx
        self.rect.y += dy

        # Remove projectile if it goes offscreen
        if (self.rect.right < 0 or self.rect.left > 800 or
            self.rect.bottom < 0 or self.rect.top > 600):
            self.kill()

    def can_collide(self):
        return (time.time() - self.spawn_time) > 0.15
# BOSS FIGHTS

# Kraken

def kraken_battle():
    global counter, boss, lobby
    global menu, current_battle
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    pygame.mixer.music.load("assets/music/stormcall.mp3")
    pygame.mixer.music.play(start=45)
    menu = False
    boss = True
    lobby = False
    counter = 60
    current_battle = "kraken"
    pygame.display.flip()

# Robot

def robot_battle():
    global counter, boss, lobby
    global menu, current_battle, robot_fight_start_time, laser_group
    global blink_times_done, blinking, blink_on, laser_active, laser_show_start_time
    global blink_times_needed, blink_positions, laser_positions
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    pygame.mixer.music.load("assets/music/marcheur.mp3")
    pygame.mixer.music.play(start=89)
    menu = False
    boss = True
    lobby = False
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
    global counter, boss, lobby
    global menu, current_battle
    global wizard_fight_start_time, wizard_wands, wizard_projectiles, wizard_wand_phase, last_wand_spawn_time
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    pygame.mixer.music.load("assets/music/cyberblade.mp3")
    pygame.mixer.music.play()
    menu = False
    boss = True
    lobby = False
    counter = 60
    current_battle = "wizard"
    wizard_fight_start_time = time.time()
    wizard_wands = pygame.sprite.Group()
    wizard_projectiles = pygame.sprite.Group()
    wizard_wand_phase = 0
    last_wand_spawn_time = 0
    player.rect.center = (100, 300)  # Reset player position
    pygame.display.flip()

# Initialize wizard groups and variables
wizard_wands = pygame.sprite.Group()
wizard_projectiles = pygame.sprite.Group()
wizard_wand_phase = 0
wizard_wand_timer = 0
wizard_fight_start_time = None

# game loop
boss = False
lobby = False
running = True
counter = 60

while running:
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
            else:
                # Check player select icons
                for i, rect in enumerate(player_rects):
                    if rect.collidepoint(mouse):
                        select_sound = pygame.mixer.Sound("assets/music/select.mp3")
                        select_sound.play()
                        selected_player = i
                        player.image = player_icons[selected_player]
                        player.rect = player.image.get_rect(center=player.rect.center)
                        break

    if menu:
        if boss:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            boss = False
        if not lobby:
            pygame.mixer.music.load("assets/music/miffy_cafe.mp3")
            pygame.mixer.music.play(loops=-1)
        lobby = True
        if counter % 60 == 0:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)

        screen.fill((r, g, b))

        if r < 75 and g < 75:
            level_text = ithaca_level.render("Level Select", True, (255, 255, 255))
            player_text = ithaca_player.render("Player Select", True, (255, 255, 255))
        else:
            level_text = ithaca_level.render("Level Select", True, (0, 0, 0))
            player_text = ithaca_player.render("Player Select", True, (0, 0, 0))

        screen.blit(level_text, (153, 25))
        screen.blit(player_text, (200, 320))

        counter += 1

        # menu hover
        mouse = pygame.mouse.get_pos()

        # Level select icons and hover
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

        # Player select icons
        for i, icon in enumerate(player_icons):
            pos = player_rects[i].topleft
            if i == selected_player:
                pygame.draw.rect(screen, (100, 100, 100), (*pos, 50, 50))
            screen.blit(icon, pos)

        # Show hovered player name and description
        hovered_index = None
        for i, rect in enumerate(player_rects):
            if rect.collidepoint(mouse):
                hovered_index = i
                break
        if hovered_index is not None:
            # clear text area before drawing text to avoid overlap
            text_area_rect = pygame.Rect(0, 500, 800, 80)
            screen.fill((r, g, b), text_area_rect)
            color = (255, 255, 255) if r < 75 and g < 75 else (0, 0, 0)
            name_surf = ithaca_hover.render(player_names[hovered_index], True, color)
            desc_surf = ithaca_desc.render(player_descs[hovered_index], True, color)
            name_rect = name_surf.get_rect(center=(400, 510))
            desc_rect = desc_surf.get_rect(center=(400, 545))
            screen.blit(name_surf, name_rect)
            screen.blit(desc_surf, desc_rect)

    else:
        if current_battle == "robot":
            elapsed = time.time() - robot_fight_start_time

            if elapsed > 65:
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
            #if elapsed > 57:
                #menu = True
                #current_battle = None

        elif current_battle == "wizard":
            elapsed = time.time() - wizard_fight_start_time
            now = time.time()

            if elapsed > 65:
                menu = True
                current_battle = None
                wizard_wands.empty()
                wizard_projectiles.empty()
            else:
                # Spawn new wands every 3 seconds only if no projectiles on screen
                if now - last_wand_spawn_time > 3 and len(wizard_projectiles) == 0:
                    wizard_wands.empty()  # Remove old wands before spawning new ones
                    wizard_wand_phase += 1
                    if wizard_wand_phase > 14:
                        wizard_wand_phase = 1  # Loop phases

                    # Determine count of wands
                    if 1 <= wizard_wand_phase <= 4:
                        count = 1
                    elif 5 <= wizard_wand_phase <= 11:
                        count = 2
                    else:
                        count = 3

                    sides = ["bottom", "left", "top", "right"]
                    for _ in range(count):
                        side = random.choice(sides)
                        if side == "bottom":
                            x = random.randint(0, 800)
                            y = 600
                            angle = random.uniform(-75, 75)
                        elif side == "left":
                            x = 0
                            y = random.randint(0, 600)
                            angle = random.uniform(15, 165)
                        elif side == "top":
                            x = random.randint(0, 800)
                            y = 0
                            angle = random.uniform(105, 255)
                        else:  # right
                            x = 800
                            y = random.randint(0, 600)
                            angle = random.uniform(195, 345)

                        wand_sprite = Wand(x, y, angle, side)
                        wizard_wands.add(wand_sprite)

                    last_wand_spawn_time = now

                # Fire projectiles after 1 second
                for wand_sprite in wizard_wands:
                    if not wand_sprite.has_fired and now - wand_sprite.spawn_time > 1:
                        # Calculate wand tip position for projectile spawn
                        length = wand_sprite.rect.height  # length of wand image approx 150
                        tip_x = wand_sprite.rect.centerx + length * math.cos(math.radians(wand_sprite.angle))
                        tip_y = wand_sprite.rect.centery + length * math.sin(math.radians(wand_sprite.angle))

                        projectile = Projectile(tip_x, tip_y, wand_sprite.angle)
                        wizard_projectiles.add(projectile)
                        wand_sprite.has_fired = True

                wizard_wands.update()
                wizard_projectiles.update()

                screen.blit(wizard_background, (0, 0))

                for wand_sprite in wizard_wands:
                    screen.blit(wand_sprite.image, wand_sprite.rect)

                for proj in wizard_projectiles:
                    screen.blit(proj.image, proj.rect)

                keys = pygame.key.get_pressed()
                player.update(keys)
                screen.blit(player.image, player.rect)

                if pygame.sprite.spritecollideany(player, wizard_wands):
                    menu = True
                    current_battle = None
                    wizard_wands.empty()
                    wizard_projectiles.empty()

                for proj in wizard_projectiles:
                    if proj.can_collide() and proj.rect.colliderect(player.rect):
                        menu = True
                        current_battle = None
                        wizard_wands.empty()
                        wizard_projectiles.empty()
                        break

    pygame.display.flip()
    clock.tick(60)

pygame.quit()