import pygame
from entities import playerEntity, enemyEntity

pygame.init()
pygame.display.set_caption("pygame")

clock = pygame.time.Clock()
resolution = (640,480)
scale = 10
screen = pygame.display.set_mode(resolution)
floor = resolution[1] * 3 / 4

player = playerEntity(resolution[0]/2,floor, 10, 20, 5, (255,0,255), resolution, floor)

enemies = [
    enemyEntity(resolution[0]*3/4,floor, 10, 20, 5, (255,0,0), resolution),
    enemyEntity(resolution[0]*7/8,floor, 10, 20, 5, (255,0,0), resolution)
]

def checkCollisions():
    enemyRects = []
    for enemy in enemies:
        enemyRects.append(enemy.rect())

    return player.rect().collidelist(enemyRects)

def redrawGameWindow():
    screen.fill((0,0,0))

    for enemy in enemies:
        enemy.draw(screen)

    player.draw(screen)

    pygame.display.update()


running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_h]:
        player.moveLeft()
    if keys[pygame.K_RIGHT] or keys[pygame.K_l]:
        player.moveRight()
    if keys[pygame.K_DOWN] or keys[pygame.K_j]:
        player.duck()
    if keys[pygame.K_UP] or keys[pygame.K_k]:
        player.jump()
    if keys[pygame.K_SPACE]:
        player.jump()

    # let gravity do it's thing
    player.fall()

    # enemies wander
    for enemy in enemies:
        enemy.wander()

    if checkCollisions() > -1:
        running = False

    # render
    redrawGameWindow()

pygame.quit()
# # while True:
# pygame.display.update()
# screen.blit(cup.image, cup.rect)
