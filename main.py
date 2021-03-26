import pygame
from entities import playerEntity, enemyEntity, terrainEntity

pygame.init()
pygame.display.set_caption("pygame")

clock = pygame.time.Clock()
area = pygame.Rect(0,0,640,480)
screen = pygame.display.set_mode((area.right, area.bottom))

# colour palette
purple = (153,0,153)
green = (0,204,0)
brown = (101, 51, 0)
gold = (255,255,102)
red = (200,0,0)

# player
player = playerEntity((area.right,0, 10, 20), purple)

entities = [
    enemyEntity((area.right*0.1,0, 10, 20)),
    enemyEntity((area.right*0.2,0, 10, 20)),
    enemyEntity((area.right*0.3,0, 10, 20)),
    enemyEntity((area.right*0.5,0, 10, 20)),
]

# terrain
terrain = [
    terrainEntity((50, 50, 100, 5), brown),
    terrainEntity((100, 100, 200, 5), brown),
    terrainEntity((150, 150, 200, 5), brown),
    terrainEntity((250, 250, 100, 5), brown),
    terrainEntity((150, 400, 100, 5), brown),
    terrainEntity((50, 450, 100, 5), brown),
]


def main():
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

        # update entities for the frame
        allRects = []
        for entity in entities:
            allRects.append(entity.rect)
        
        for entity in entities:
            if entity.isMobile:
                entity.tick(area, allRects)
        
        player.tick(area)
        collidedRectIndexes = player.checkForCollisions(allRects)
        if collidedRectIndexes:
            for collidedRectIndex in collidedRectIndexes:
                entities.pop(collidedRectIndex)
            for collidedRectIndex in collidedRectIndexes:
                entities.append(enemyEntity((area.right*0.1,0, 10, 20)))
            player.damaged()

        if not(player.alive()):
            running = False

        # render
        screen.fill((0,0,0))

        for entity in terrain + entities + [player]:
            entity.draw(screen)
            
        font = pygame.font.SysFont(None, 24)
        img = font.render('Health', True, red)
        screen.blit(img, (20, 20))
        font = pygame.font.SysFont(None, 24)
        img = font.render("*" * player.health, True, red)
        screen.blit(img, (20, 40))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
