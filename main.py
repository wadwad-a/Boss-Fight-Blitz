import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Boss Fight Blitz")
clock = pygame.time.Clock()

# Create assets

kraken_icon = pygame.image.load("assets/KRAKEN-ICON.png")
kraken_icon = pygame.transform.scale(kraken_icon, (200, 200))
robot_icon = pygame.image.load("assets/ROBOT-ICON.png")
robot_icon = pygame.transform.scale(robot_icon, (200, 200))
wizard_icon = pygame.image.load("assets/WIZARD-ICON.png")
wizard_icon = pygame.transform.scale(wizard_icon, (200, 200))

# game loops
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.Surface.fill(screen, (255, 255, 0))
    pygame.Surface.blit(screen, kraken_icon, (100, 200))
    pygame.Surface.blit(screen, robot_icon, (300, 200))
    pygame.Surface.blit(screen, wizard_icon, (500, 200))

    pygame.display.flip()       # Update the window
    clock.tick(60)              # 60 FPS

pygame.quit()