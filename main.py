import pygame
import pygame.freetype
import sys
from constants import * 
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.freetype.Font("AsteroidFont.ttf", 30)
    clock = pygame.time.Clock()
    dt = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    score = 0
    
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroidfield = AsteroidField()

    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        for object in updatable:
            object.update(dt)

        for object in asteroids:
            if object.check_collision(player):
                print("Game over!")
                print(f"Final Score: {score}")
                sys.exit()
        
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.check_collision(shot):
                    asteroid.split()
                    if asteroid.radius <= ASTEROID_MIN_RADIUS:
                        score += 200
                    elif asteroid.radius == ASTEROID_MAX_RADIUS:
                        score += 100
                    else:
                        score += 150
                    shot.kill()

        screen.fill((0, 0, 0))
        font.render_to(screen, (40, 40), f"{score}", (255, 255, 255))
        
        for object in drawable:
            object.draw(screen)

        pygame.display.flip()

        # limit fps to 60
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()