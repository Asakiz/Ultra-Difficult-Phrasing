import pygame

pygame.init()

gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('Ultra Difficult Phrasing')

clock = pygame.time.Clock()

test = pygame.image.load('spike.png')
gameDisplay.blit(test, (150, 70))

crashed = False

while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()