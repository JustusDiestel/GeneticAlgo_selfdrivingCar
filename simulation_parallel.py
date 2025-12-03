import pygame
import math
from sprites import CarSprite, PadSprite, Trophy

# Level-Konfiguration wie in deinem Spiel
pad_positions = [
    (0, 10),(600, 10),(1100, 10),
    (100,150),(600,150),
    (100,300),(800,300),
    (400,450),(700,450),
    (200,600),(900,600),
    (400,750),(800,750)
]

TROPHY_POS = (285, 0)
MAX_FRAMES = 2000


def dist_to_goal(car):
    cx, cy = car.position
    tx, ty = TROPHY_POS
    return math.dist((cx, cy), (tx, ty))


def simulate_population(population, visualise=False):
    pygame.init()

    if visualise:
        screen = pygame.display.set_mode((1024, 768))
    else:
        # headless = keine Anzeige
        screen = pygame.display.set_mode((1, 1))

    clock = pygame.time.Clock()

    # Sprites erzeugen für gesamte Population
    pads = pygame.sprite.Group(*[PadSprite(pos) for pos in pad_positions])
    trophy = pygame.sprite.Group(Trophy(TROPHY_POS))

    cars = []
    car_groups = []
    done = [False] * len(population)

    results = [None] * len(population)

    for _ in population:
        car = CarSprite('images/car.png', (10, 730))
        cars.append(car)
        car_groups.append(pygame.sprite.Group(car))

    frame = 0

    while frame < MAX_FRAMES and not all(done):
        frame += 1
        clock.tick(60)

        for i, individual in enumerate(population):
            if done[i]:
                continue

            ku, kd, kl, kr = individual[frame % len(individual)]
            car = cars[i]

            car.k_up, car.k_down = ku, kd
            car.k_left, car.k_right = kl, kr

            car.update(1)

            # Crash
            if pygame.sprite.groupcollide(car_groups[i], pads, False, False):
                results[i] = (frame, True, False, dist_to_goal(car))
                done[i] = True
                continue

            # Goal
            if pygame.sprite.groupcollide(car_groups[i], trophy, False, True):
                results[i] = (frame, False, True, 0)
                done[i] = True
                continue

        if visualise:
            screen.fill((0, 0, 0))
            pads.draw(screen)
            trophy.draw(screen)
            for grp in car_groups:
                grp.draw(screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return results

    # Alle, die noch leben → Distanz berechnen
    for i, car in enumerate(cars):
        if results[i] is None:
            results[i] = (frame, False, False, dist_to_goal(car))

    pygame.quit()
    return results