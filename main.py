import pygame, random

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Boss Fight Blitz")
clock = pygame.time.Clock()

# create assets

kraken_icon = pygame.image.load("assets/KRAKEN-ICON.png")
kraken_icon = pygame.transform.scale(kraken_icon, (200, 200))
robot_icon = pygame.image.load("assets/ROBOT-ICON.png")
robot_icon = pygame.transform.scale(robot_icon, (200, 200))
wizard_icon = pygame.image.load("assets/WIZARD-ICON.png")
wizard_icon = pygame.transform.scale(wizard_icon, (200, 200))
ithaca = pygame.font.Font("assets/ithaca-LVB75.ttf", 128)

# hover effect

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

# BOSS FIGHTS

# Kraken

def kraken_battle():
    pass

# Robot

def robot_battle():
    pass

# Wizard

def wizard_battle():
    pass


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
# menu create
    if counter % 60 == 0:
        pygame.Surface.fill(screen, (r, g, b))
        if r < 75 and g < 75:
            screen.blit(ithaca.render("Level Select", True, (255, 255, 255)), (153, 75))
        else:
            screen.blit(ithaca.render("Level Select", True, (0, 0, 0)), (153, 75))
    counter += 1
    

# menu hover
    mouse = pygame.mouse.get_pos()
    if kraken_rect.collidepoint(mouse):
        screen.blit(kraken_dark, (100, 200))
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            kraken_battle()
    else:
        screen.blit(kraken_icon, (100, 200))
    if robot_rect.collidepoint(mouse):
        screen.blit(robot_dark, (300, 200))
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            robot_battle()
    else:
        screen.blit(robot_icon, (300, 200))
    if wizard_rect.collidepoint(mouse):
        screen.blit(wizard_dark, (500, 200))
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            wizard_battle()
    else:
        screen.blit(wizard_icon, (500, 200))

    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()