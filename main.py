# imports
import pygame, random, time, math

# initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Boss Fight Blitz")
clock = pygame.time.Clock()
show_death_popup = False
show_win_popup = False
pygame.mixer.music.set_volume(0.45)
popup_dismissed_time = 0
click_immunity_duration = 1

# create assets
# icons
# level select
kraken_icon = pygame.image.load("assets/icons/KRAKEN-ICON.png")
kraken_icon = pygame.transform.scale(kraken_icon, (200, 200))
robot_icon = pygame.image.load("assets/icons/ROBOT-ICON.png")
robot_icon = pygame.transform.scale(robot_icon, (200, 200))
wizard_icon = pygame.image.load("assets/icons/WIZARD-ICON.png")
wizard_icon = pygame.transform.scale(wizard_icon, (200, 200))

# create masks for pixel-perfect collision
kraken_mask = pygame.mask.from_surface(kraken_icon)
robot_mask = pygame.mask.from_surface(robot_icon)
wizard_mask = pygame.mask.from_surface(wizard_icon)

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
unknown_icon = pygame.image.load("assets/icons/unknown.png")
unknown_icon = pygame.transform.scale(unknown_icon, (50, 50))
raspberry_icon = pygame.image.load("assets/icons/raspberry.png")
raspberry_icon = pygame.transform.scale(raspberry_icon, (50, 50))
orb_icon = pygame.image.load("assets/icons/orb.png")
orb_icon = pygame.transform.scale(orb_icon, (50, 50))
treasure_icon = pygame.image.load("assets/icons/treasure.png")
treasure_icon = pygame.transform.scale(treasure_icon, (50, 50))
chicken_icon = pygame.image.load("assets/icons/chicken.png")
chicken_icon = pygame.transform.scale(chicken_icon, (50, 50))
gold_icon = pygame.image.load("assets/icons/gold.png")
gold_icon = pygame.transform.scale(gold_icon, (50, 50))

# fonts
ithaca_level = pygame.font.Font("assets/fonts/ithaca-LVB75.ttf", 128)
ithaca_player = pygame.font.Font("assets/fonts/ithaca-LVB75.ttf", 92)
ithaca_hover = pygame.font.Font("assets/fonts/ithaca-LVB75.ttf", 30)
ithaca_desc = pygame.font.Font("assets/fonts/ithaca-LVB75.ttf", 20)

# music
cyberblade = pygame.mixer.music.load("assets/music/cyberblade.mp3")

# backgrounds
robot_background_1 = pygame.image.load("assets/backgrounds/robot-bg-1.png")
robot_background_1 = pygame.transform.scale(robot_background_1, (800, 600))
robot_background_2 = pygame.image.load("assets/backgrounds/robot-bg-2.png")
robot_background_2 = pygame.transform.scale(robot_background_2, (800, 600))
wizard_background_1 = pygame.image.load("assets/backgrounds/wizard-bg-1.png")
wizard_background_1 = pygame.transform.scale(wizard_background_1, (800, 600))
wizard_background_2 = pygame.image.load("assets/backgrounds/wizard-bg-2.png")
wizard_background_2 = pygame.transform.scale(wizard_background_2, (800, 600))
kraken_background_1 = pygame.image.load("assets/backgrounds/kraken-bg-1.png")
kraken_background_1 = pygame.transform.scale(kraken_background_1, (800, 600))
kraken_background_2 = pygame.image.load("assets/backgrounds/kraken-bg-2.png")
kraken_background_2 = pygame.transform.scale(kraken_background_2, (800, 600))
kraken_background_3 = pygame.image.load("assets/backgrounds/kraken-bg-3.png")
kraken_background_3 = pygame.transform.scale(kraken_background_3, (800, 600))
kraken_background_4 = pygame.image.load("assets/backgrounds/kraken-bg-4.png")
kraken_background_4 = pygame.transform.scale(kraken_background_4, (800, 600))
kraken_background_5 = pygame.image.load("assets/backgrounds/kraken-bg-5.png")
kraken_background_5 = pygame.transform.scale(kraken_background_5, (800, 600))
kraken_background_6 = pygame.image.load("assets/backgrounds/kraken-bg-6.png")
kraken_background_6 = pygame.transform.scale(kraken_background_6, (800, 600))
kraken_background_7 = pygame.image.load("assets/backgrounds/kraken-bg-7.png")
kraken_background_7 = pygame.transform.scale(kraken_background_7, (800, 600))
kraken_background_8 = pygame.image.load("assets/backgrounds/kraken-bg-8.png")
kraken_background_8 = pygame.transform.scale(kraken_background_8, (800, 600))
kraken_background_9 = pygame.image.load("assets/backgrounds/kraken-bg-9.png")
kraken_background_9 = pygame.transform.scale(kraken_background_9, (800, 600))
kraken_background_10 = pygame.image.load("assets/backgrounds/kraken-bg-10.png")
kraken_background_10 = pygame.transform.scale(kraken_background_10, (800, 600))

# weapons
laser = pygame.image.load("assets/weapons/laser.png")
laser = pygame.transform.scale(laser, (50, 800))
laser_blink = pygame.image.load("assets/weapons/blink-laser.png")
laser_blink = pygame.transform.scale(laser_blink, (50, 600))
wand_img = pygame.image.load("assets/weapons/wand.png").convert_alpha()
wand_img = pygame.transform.scale(wand_img, (25, 160))
jellyfish = pygame.image.load("assets/weapons/jellyfish.png")
jellyfish = pygame.transform.scale(jellyfish, (50, 120))
boat = pygame.image.load("assets/weapons/boat.png")
boat = pygame.transform.scale(boat, (200, 150))
water_hb = pygame.image.load("assets/weapons/water.png")
water_hb = pygame.transform.scale(water_hb, (800, 600))
water_mask = pygame.mask.from_surface(water_hb)
water_rect = water_hb.get_rect(topleft=(0, 0))

# laser class
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, orientation='vertical'):
        super().__init__()
        length = 600
        width = 50
        self.orientation = orientation
        self.original_image = pygame.Surface((width, length), pygame.SRCALPHA)
        pygame.draw.rect(self.original_image, (255, 0, 0), self.original_image.get_rect())
        if orientation == 'vertical':
            self.image = self.original_image
            self.rect = self.image.get_rect(midtop=(x, 0))
        else:
            self.image = pygame.transform.rotate(self.original_image, 90)
            self.image = pygame.transform.scale(self.image, (800, 50))
            self.rect = self.image.get_rect(topleft=(0, y - 25))

    def update(self):
        pass

class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(100, 300))
        self.mask = pygame.mask.from_surface(self.image)
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
kraken_rect = kraken_icon.get_rect(topleft=(500, 200))
robot_rect = robot_icon.get_rect(topleft=(100, 200))
wizard_rect = wizard_icon.get_rect(topleft=(300, 200))

player_icons = [smiley_icon, cookie_icon, crazy_icon, heart_icon, penny_icon, unknown_icon, unknown_icon, unknown_icon, unknown_icon, unknown_icon]
player_names = ["Smiley", "Cookie", "Crazy", "Heart", "Penny", "???", "???", "???", "???", "???"]
player_descs = ["default", "yum", "what", "quite lovely", "woah i'm rich", "power down robot", "steal wizard\'s magic", "send kraken back to cave", "turn into a flaming chicken", "get every player"]
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

# Wand and projectile classes (unchanged)
class Wand(pygame.sprite.Sprite):
    def __init__(self, pivot_pos, angle, side):
        super().__init__()
        self.original_image = wand_img
        self.angle = angle
        self.pivot = pygame.math.Vector2(pivot_pos)
        self.offset = pygame.math.Vector2(0, -self.original_image.get_height() / 2)
        self.image, self.rect = self.rotate()
        self.mask = pygame.mask.from_surface(self.image)
        self.spawn_time = time.time()
        self.has_fired = False
        self.side = side

    def rotate(self):
        rotated_image = pygame.transform.rotate(self.original_image, -self.angle)
        rotated_offset = self.offset.rotate(-self.angle)
        rect = rotated_image.get_rect(center=self.pivot + rotated_offset)
        return rotated_image, rect

    def update(self):
        pass

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        length = 800
        width = 20
        self.original_image = pygame.Surface((length, width), pygame.SRCALPHA)
        pygame.draw.rect(self.original_image, (255, 255, 0), self.original_image.get_rect())
        self.image = pygame.transform.rotate(self.original_image, -(angle - 90))
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = angle - 90
        self.speed = 20
        self.spawn_time = time.time()
        self.pos_x = float(x)
        self.pos_y = float(y)

    def update(self):
        dx = self.speed * math.cos(math.radians(self.angle))
        dy = self.speed * math.sin(math.radians(self.angle))
        self.pos_x += dx
        self.pos_y += dy
        self.rect.centerx = int(self.pos_x)
        self.rect.centery = int(self.pos_y)
        if (self.rect.right < 0 or self.rect.left > 800 or
            self.rect.bottom < 0 or self.rect.top > 600):
            self.kill()

    def can_collide(self):
        return (time.time() - self.spawn_time) > 0.15
    

class Boat(pygame.sprite.Sprite):
    def __init__(self, direction, y_start, duration):
        super().__init__()
        self.image = boat
        self.rect = self.image.get_rect()
        self.start_time = time.time()
        self.duration = duration
        self.y_start = y_start
        self.y_peak = y_start - 200
        self.direction = direction
        if direction == "right":
            self.rect.left = 800
            self.x_start = 800
            self.x_end = -self.rect.width
        else:
            self.rect.right = 0
            self.x_start = -self.rect.width
            self.x_end = 800

    def update(self):
        elapsed = time.time() - self.start_time
        t = min(elapsed / self.duration, 1)
        self.rect.centerx = self.x_start + (self.x_end - self.x_start) * t
        self.rect.centery = self.y_start - 4 * (self.y_start - self.y_peak) * t * (1 - t)
        if t >= 1:
            self.kill()


class Jellyfish(pygame.sprite.Sprite):
    def __init__(self, x, start_time):
        super().__init__()
        self.image = jellyfish
        self.rect = self.image.get_rect(midbottom=(x, 800))
        self.start_time = start_time  # now this is an absolute timestamp
        self.y_start = 800
        self.y_peak = self.y_start - 450
        self.finished = False

    def update(self):
        now = time.time()
        if now < self.start_time:
            return
        elapsed = now - self.start_time
        duration = 1.0  # 1 second to reach top and back
        t = min(elapsed / duration, 1)
        self.rect.centery = self.y_start - 4 * (self.y_start - self.y_peak) * t * (1 - t)
        if t >= 1 and not self.finished:
            self.kill()
            self.finished = True

# Pixel-perfect collision helper
def is_mouse_over_icon(mouse_pos, icon_rect, icon_mask):
    rel_x = mouse_pos[0] - icon_rect.left
    rel_y = mouse_pos[1] - icon_rect.top
    if 0 <= rel_x < icon_rect.width and 0 <= rel_y < icon_rect.height:
        return icon_mask.get_at((rel_x, rel_y))
    return False

# Boss fight functions (unchanged)
def kraken_battle():
    global counter, boss, lobby, menu, current_battle
    global kraken_fight_start_time, kraken_backgrounds, boats_group, jellyfish_group, jellyfish_pending
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    pygame.mixer.music.load("assets/music/stormcall.mp3")
    pygame.mixer.music.play(start=45)
    menu = False
    boss = True
    lobby = False
    counter = 57
    current_battle = "kraken"
    kraken_fight_start_time = time.time()
    boats_group = pygame.sprite.Group()
    jellyfish_group = pygame.sprite.Group()
    jellyfish_pending = []
    kraken_backgrounds = [
        kraken_background_1, kraken_background_2, kraken_background_3,
        kraken_background_4, kraken_background_5, kraken_background_6,
        kraken_background_7, kraken_background_8, kraken_background_9, kraken_background_10
    ]
    player.rect.center = (100, 300)
    pygame.display.flip()

def robot_battle():
    global counter, boss, lobby, robocount, menu, current_battle, robot_fight_start_time, laser_group
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
    robocount = 0
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

def wizard_battle():
    global counter, boss, lobby, wizcount, menu, current_battle
    global wizard_fight_start_time, wizard_wands, wizard_projectiles, wizard_wand_phase, last_wand_spawn_time
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    pygame.mixer.music.load("assets/music/cyberblade.mp3")
    pygame.mixer.music.play()
    menu = False
    boss = True
    lobby = False
    counter = 60
    wizcount = 0
    current_battle = "wizard"
    wizard_fight_start_time = time.time()
    wizard_wands = pygame.sprite.Group()
    wizard_projectiles = pygame.sprite.Group()
    wizard_wand_phase = 0
    last_wand_spawn_time = 0
    player.rect.center = (100, 300)
    pygame.display.flip()

# Initialize wizard groups and variables
wizard_wands = pygame.sprite.Group()
wizard_projectiles = pygame.sprite.Group()
wizard_wand_phase = 0
wizard_wand_timer = 0
wizard_fight_start_time = None

# Initialize kraken groups and variables
kraken_fight_start_time = None
last_kraken_frame_change = 0
kraken_backgrounds = [
    kraken_background_1, kraken_background_2, kraken_background_3,
    kraken_background_4, kraken_background_5, kraken_background_6,
    kraken_background_7, kraken_background_8, kraken_background_9,
    kraken_background_10
]
kraken_bg = kraken_backgrounds[0]
boats_group = pygame.sprite.Group()
jellyfish_group = pygame.sprite.Group()
jellyfish_sequence_active = False

# game loop
boss = False
lobby = False
running = True
counter = 60
text_die = ""

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if menu and (show_death_popup or show_win_popup):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                show_death_popup = False
                show_win_popup = False
                popup_dismissed_time = time.time()
            continue

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and menu:
            if time.time() - popup_dismissed_time < click_immunity_duration:
                continue
            mouse = pygame.mouse.get_pos()
            if is_mouse_over_icon(mouse, kraken_rect, kraken_mask):
                kraken_battle()
            elif is_mouse_over_icon(mouse, robot_rect, robot_mask):
                robot_battle()
            elif is_mouse_over_icon(mouse, wizard_rect, wizard_mask):
                wizard_battle()
            else:
                for i, rect in enumerate(player_rects):
                    if rect.collidepoint(mouse):
                        if player_names[i] == "???":
                            deny_sound = pygame.mixer.Sound("assets/music/deny.mp3")
                            deny_sound.set_volume(0.4)
                            deny_sound.play()
                            break
                        else:
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
        if (player_icons[5] == raspberry_icon and player_icons[6] == orb_icon and player_icons[7] == treasure_icon and player_icons[8] == chicken_icon):
            player_icons[9] = gold_icon
            player_names[9] = "Gold Medal"

        if r < 128 and g < 128:
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
        if is_mouse_over_icon(mouse, kraken_rect, kraken_mask):
            screen.blit(kraken_dark, (500, 150))
        else:
            screen.blit(kraken_icon, (500, 150))

        if is_mouse_over_icon(mouse, robot_rect, robot_mask):
            screen.blit(robot_dark, (100, 150))
        else:
            screen.blit(robot_icon, (100, 150))

        if is_mouse_over_icon(mouse, wizard_rect, wizard_mask):
            screen.blit(wizard_dark, (300, 150))
        else:
            screen.blit(wizard_icon, (300, 150))

        # Player select icons
        for i, icon in enumerate(player_icons):
            pos = player_rects[i].topleft
            if i == selected_player:
                center = (pos[0] + 25, pos[1] + 25)
                pygame.draw.circle(screen, (255-r, 255-g, 255-b), center, 35)
            screen.blit(icon, pos)

        # Show hovered player name and description
        hovered_index = None
        for i, rect in enumerate(player_rects):
            if rect.collidepoint(mouse):
                hovered_index = i
                break

        if hovered_index is not None:
            text_area_rect = pygame.Rect(0, 500, 800, 80)
            screen.fill((r, g, b), text_area_rect)
            color = (255, 255, 255) if r < 75 and g < 75 else (0, 0, 0)
            name_surf = ithaca_hover.render(player_names[hovered_index], True, color)
            desc_surf = ithaca_desc.render(player_descs[hovered_index], True, color)
            name_rect = name_surf.get_rect(center=(400, 510))
            desc_rect = desc_surf.get_rect(center=(400, 545))
            screen.blit(name_surf, name_rect)
            screen.blit(desc_surf, desc_rect)

        if show_death_popup or show_win_popup:
            overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            text_str = "You Died" if show_death_popup else "You Won"
            text_color = (255, 0, 0) if show_death_popup else (0, 255, 0)
            text_surf = ithaca_player.render(text_str, True, text_color)
            text_rect = text_surf.get_rect(center=(400, 300))
            screen.blit(text_surf, text_rect)
            if show_death_popup:
                text_desc = ithaca_hover.render(text_die, True, text_color)
                text_rect1 = text_desc.get_rect(center=(400, 400))
                screen.blit(text_desc, text_rect1)
    else:
        if current_battle == "robot":
            robocount += 0.05
            elapsed = time.time() - robot_fight_start_time

            if elapsed > 63:
                menu = True
                current_battle = None
                show_win_popup = True
                show_death_popup = False
                player_icons[5] = raspberry_icon
                player_names[5] = "Raspberry Pi(e)"
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
                    elif 12 <= blink_times_done <= 21:
                        count = 3
                    elif blink_times_done >= 22:
                        count = 4

                    while len(blink_positions) < count and attempts < max_attempts:
                        x = random.randint(50, 750)
                        if all(abs(x - px) >= 50 for px in blink_positions):
                            blink_positions.append(x)
                        attempts += 1

                    # Horizontal blink positions - random y, same count rules as vertical lasers
                    horizontal_blink_positions = []
                    attempts = 0
                    while len(horizontal_blink_positions) < (1 if count == 2 else 2 if count == 3 else 3 if count == 4 else 0) and attempts < max_attempts:
                        y = random.randint(50, 550)
                        if all(abs(y - py) >= 50 for py in horizontal_blink_positions):
                            horizontal_blink_positions.append(y)
                        attempts += 1

                if blinking:
                    laser_ex = False
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

                            # Add vertical lasers
                            for x in laser_positions:
                                new_laser = Laser(x, 300, orientation='vertical')
                                laser_group.add(new_laser)

                            # Add horizontal lasers based on count of vertical lasers
                            horizontal_count = 1 if len(laser_positions) == 2 else 2 if len(laser_positions) == 3 else 3 if len(laser_positions) == 4 else 0
                            for i in range(horizontal_count):
                                y = horizontal_blink_positions[i]
                                new_laser = Laser(400, y, orientation='horizontal')
                                laser_group.add(new_laser)

                            laser_show_start_time = now
                            blink_times_needed = 4

                if laser_active and now - laser_show_start_time > 1:
                    laser_active = False
                    laser_group.empty()

                laser_group.update()
                keys = pygame.key.get_pressed()
                player.update(keys)

                if robocount % 2 >= 0 and robocount % 2 < 1:
                    screen.blit(robot_background_2, (0, 0))
                else:
                    screen.blit(robot_background_1, (0, 0))

                if blinking and blink_on:
                    # Blink vertical lasers (full height)
                    for x in blink_positions:
                        screen.blit(laser_blink, (x - laser_blink.get_width() // 2, 0))

                    # Blink horizontal lasers (full width)
                    horizontal_blink_image = pygame.transform.rotate(laser_blink, 90)
                    horizontal_blink_image = pygame.transform.scale(horizontal_blink_image, (800, 50))
                    for y in horizontal_blink_positions:
                        screen.blit(horizontal_blink_image, (0, y - 25))

                elif laser_active:
                    laser_group.draw(screen)
                    if not laser_ex:
                        laser_sound = pygame.mixer.Sound("assets/music/laser.mp3")
                        laser_sound.set_volume(1.0)
                        laser_sound.play()
                    laser_ex = True

                screen.blit(player.image, player.rect)

                if laser_active:
                    if pygame.sprite.spritecollideany(player, laser_group):
                        menu = True
                        current_battle = None
                        show_death_popup = True
                        show_win_popup = False
                        laser_group.empty()
                        laserChoice = ["very hot Laser", "inconsiderate Laser", "powerful Light Source"]
                        laserChoice2 = ["bullied", "fried", "cooked", "deep-fried", "ended", "scalded", "obliterated"]
                        text_die = f"Player was {random.choice(laserChoice2)} by {random.choice(laserChoice)}."

        elif current_battle == "kraken":
            elapsed = time.time() - kraken_fight_start_time
            now = time.time()

            if elapsed > 57:
                menu = True
                current_battle = None
                show_win_popup = True
                show_death_popup = False
                player_icons[7] = treasure_icon
                player_names[7] = "Treasure Chest"
                boats_group.empty()
                jellyfish_group.empty()
                
            else:
                # Update background every ~1 seconds
                if now - last_kraken_frame_change > 1:
                    kraken_bg = random.choice(kraken_backgrounds)
                    last_kraken_frame_change = now

                screen.blit(kraken_bg, (0, 0))
                screen.blit(water_hb, (0, 0))

                # Chance to launch boat
                if len(boats_group) < 3 and random.random() < 0.007:
                    direction = random.choice(["left", "right"])
                    y_start = random.randint(150, 500)
                    duration = random.uniform(2, 4)
                    boat_sprite = Boat(direction, y_start, duration)
                    boats_group.add(boat_sprite)

                # Chance to launch jellyfish sequence
                if not jellyfish_sequence_active and random.random() < 0.007:
                    sequence = list(range(6))
                    random.shuffle(sequence)
                    jellyfish_sequence_active = True
                    launch_times = [now + i * 0.5 for i in range(6)]
                    for idx, launch_time in zip(sequence, launch_times):
                        x_pos = 65 + idx * ((800 - 130) / 5)
                        jellyfish_sprite = Jellyfish(x_pos, launch_time)
                        jellyfish_group.add(jellyfish_sprite)
                if jellyfish_sequence_active and len(jellyfish_group) == 0:
                    jellyfish_sequence_active = False

                boats_group.update()
                jellyfish_group.update()

                boats_group.draw(screen)
                jellyfish_group.draw(screen)

                keys = pygame.key.get_pressed()
                player.update(keys)
                screen.blit(player.image, player.rect)

                # Check collisions
                if pygame.sprite.spritecollideany(player, boats_group, collided=pygame.sprite.collide_mask):
                    menu = True
                    current_battle = None
                    show_death_popup = True
                    show_win_popup = False
                    boats_group.empty()
                    jellyfish_group.empty()
                    hitKraken = ["was hit by", "was struck by", "was crushed by", "collided with", "drowned under", "was knocked out by"]
                    adjKraken = ["large", "massive", "formidable", "unforgiving", "rude"]
                    boatKraken = ["Boat", "Ship", "Vessel", "Sailboat"]
                    text_die = f"Player {random.choice(hitKraken)} {random.choice(adjKraken)} {random.choice(boatKraken)}."

                if pygame.sprite.spritecollideany(player, jellyfish_group, collided=pygame.sprite.collide_mask):
                    menu = True
                    current_battle = None
                    show_death_popup = True
                    show_win_popup = False
                    boats_group.empty()
                    jellyfish_group.empty()
                    actionKraken = ["was stung by", "was mauled by", "was crushed by", "was poisoned by", "was hugged too hard by"]
                    jellyKraken = ["rude", "unkind", "mean", "angry", "irritated", "annoyed", "confused", "malicious"]
                    text_die = f"Player {random.choice(actionKraken)} {random.choice(jellyKraken)} Jellyfish."
                
                offset = (int(player.rect.x - water_rect.x), int(player.rect.y - water_rect.y))
                if water_mask.overlap(player.mask, offset):
                    if not hasattr(player, "water_touch_start"):
                        player.water_touch_start = time.time()
                    elif time.time() - player.water_touch_start >= 1.5:
                        menu = True
                        current_battle = None
                        show_death_popup = True
                        show_win_popup = False
                        boats_group.empty()
                        jellyfish_group.empty()
                        drownText = ["Player was drowned in the water by Kraken.", "Player was taken under the waves by Kraken.", "Player could not breathe underwater.", "Player forgot how to swim.", "Player got swept away by a rip current.", "Player couldn't tread water.", "Player was lost at sea."]
                        text_die = random.choice(drownText)
                else:
                    if hasattr(player, "water_touch_start"):
                        del player.water_touch_start

        elif current_battle == "wizard":
            wizcount += 0.05
            elapsed = time.time() - wizard_fight_start_time
            now = time.time()

            if elapsed > 51:
                menu = True
                current_battle = None
                wizard_wands.empty()
                wizard_projectiles.empty()
                show_win_popup = True
                show_death_popup = False
                player_icons[6] = orb_icon
                player_names[6] = "Magic Orb"
            else:
                # Spawn new wands every 3 seconds only if no projectiles on screen
                if now - last_wand_spawn_time > 3 and len(wizard_projectiles) == 0:
                    wizard_wands.empty()  # Remove old wands before spawning new ones
                    wizard_wand_phase += 1
                    if wizard_wand_phase > 17:
                        wizard_wand_phase = 1  # Loop phases

                    # Determine count of wands based on phase
                    if 1 <= wizard_wand_phase <= 4:
                        count = 1
                    elif 5 <= wizard_wand_phase <= 9:
                        count = 2
                    elif 10 <= wizard_wand_phase <= 14:
                        count = 3
                    else:
                        count = 4

                    offset = 10
                    wand_length = wand_img.get_height()  # 150

                    sides = ["bottom", "left", "top", "right"]
                    for _ in range(count):
                        side = random.choice(sides)

                        if side == "bottom":
                            angle = random.uniform(-75, 75)
                            pivot_x = random.randint(int(wand_length / 2), 800 - int(wand_length / 2))
                            pivot_y = 625
                        elif side == "left":
                            angle = random.uniform(30, 150)
                            if angle < 45 or angle > 135:
                                pivot_x = 25
                            else:
                                pivot_x = 50
                            pivot_y = random.randint(int(wand_length / 2), 600 - int(wand_length / 2))
                        elif side == "top":
                            angle = random.uniform(105, 255)
                            pivot_x = random.randint(int(wand_length / 2), 800 - int(wand_length / 2))
                            pivot_y = -25
                        else:  # right
                            angle = random.uniform(210, 330)
                            if angle < 225 or angle > 315:
                                pivot_x = 750
                            else:
                                pivot_x = 725
                            pivot_y = random.randint(int(wand_length / 2), 600 - int(wand_length / 2))

                        wand_sprite = Wand((pivot_x, pivot_y), angle, side)
                        wizard_wands.add(wand_sprite)

                    last_wand_spawn_time = now

                # Fire projectiles after 1 second from wand spawn
                wand_length = 150  # fixed length of wand image before rotation
                for wand_sprite in wizard_wands:
                    if not wand_sprite.has_fired and now - wand_sprite.spawn_time > 1:
                        proj_ex = False
                        wand_length = wand_sprite.original_image.get_height()
                        if not proj_ex:
                            laser_sound = pygame.mixer.Sound("assets/music/spell.mp3")
                            laser_sound.set_volume(1.0)
                            laser_sound.play()
                        proj_ex = True
                        
                        # Vector pointing from pivot to tip (wand points upward initially)
                        local_tip = pygame.math.Vector2(0, -wand_length / 2)
                        
                        # Rotate tip vector by wand angle (clockwise rotation)
                        rotated_tip = local_tip.rotate(-wand_sprite.angle)
                        
                        # Global position of wand tip
                        tip_pos = wand_sprite.pivot + rotated_tip
                        
                        # Spawn projectile slightly behind tip, along wand axis
                        back_offset = 0
                        angle_rad = math.radians(wand_sprite.angle)
                        
                        # Direction vector of wand (pointing toward tip)
                        wand_dir = pygame.math.Vector2(math.cos(angle_rad), math.sin(angle_rad))
                        
                        # Spawn point = tip_pos - back_offset * wand_dir
                        spawn_pos = tip_pos - wand_dir * back_offset
                        
                        projectile = Projectile(spawn_pos.x, spawn_pos.y, wand_sprite.angle)
                        wizard_projectiles.add(projectile)
                        wand_sprite.has_fired = True
                        

                wizard_wands.update()
                wizard_projectiles.update()

                if wizcount % 2 >= 0 and wizcount % 2 < 1:
                    screen.blit(wizard_background_2, (0, 0))
                else:
                    screen.blit(wizard_background_1, (0, 0))

                for proj in wizard_projectiles:
                    screen.blit(proj.image, proj.rect)
                for wand_sprite in wizard_wands:
                    screen.blit(wand_sprite.image, wand_sprite.rect)

                

                keys = pygame.key.get_pressed()
                player.update(keys)
                screen.blit(player.image, player.rect)

                # Collision with wands ends the battle
                if pygame.sprite.spritecollideany(player, wizard_wands, collided=pygame.sprite.collide_mask):
                    menu = True
                    current_battle = None
                    show_death_popup = True
                    show_win_popup = False
                    wizard_wands.empty()
                    wizard_projectiles.empty()
                    wandChoice = ["smacked", "bopped", "whacked", "bonked", "knocked out", "hit", "slapped", "dinked"]
                    text_die = f"Player was {random.choice(wandChoice)} by Wand."

                # Collision with projectiles (only after 0.15s) ends battle
                for proj in wizard_projectiles:
                    if proj.can_collide() and pygame.sprite.collide_mask(proj, player):
                        menu = True
                        current_battle = None
                        show_death_popup = True
                        show_win_popup = False
                        wizard_wands.empty()
                        wizard_projectiles.empty()
                        magicText = ["Table", "Chair", "Week-old Sandwich", "Swimming Pool","Boat", "Cheeseburger", "Water Bottle", "Abandoned Shopping Cart"]
                        chickenchance = random.randint(1, 50)
                        if chickenchance == 23:
                            randomText = "Flaming Chicken"
                            player_names[8] = "Flaming Chicken"
                            player_icons[8] = chicken_icon
                            pygame.mixer.Sound("assets/music/chicken.mp3").play()
                        else:
                            randomText = random.choice(magicText)
                        transformText = ["was magically transformed into", "was turned into", "somehow became"]
                        text_die = f"Player {random.choice(transformText)} {randomText}."
                        break


    pygame.display.flip()
    clock.tick(60)

pygame.quit()