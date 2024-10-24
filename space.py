import pygame
import math
import os

window_width = 800
window_height = 600
origin = (window_width / 2, window_height / 2)

# 1 distance unit >> 1.000.000 km >> 1.000.000.000 m
distance_factor = 10**9

# contants:
G = 6.6743 * 10**-11

path = os.path.dirname(__file__)

def main():
    time = 0 # in seconds
    time_multiplier = 1
    updateDelay = 0.1
    delta_time = updateDelay * time_multiplier

    class Planet():
        def __init__(self, input_mass = 0, input_pos = (0, 0), input_radius = 1, input_name = "unnamed", input_color = (255, 255, 255), input_trajectory = False):
            # properties
            self.mass = input_mass # in kg
            self.velocity = (0, 0) # in m/s
            self.position = input_pos
            self.radius = input_radius

            # asthetics
            self.name = input_name
            self.color = input_color
            self.trajectory = []
            self.draw_trajectory = input_trajectory

        def updatePosition(self):
            self.position = (self.position[0] + ((self.velocity[0] * delta_time)), self.position[1] + ((self.velocity[1] * delta_time)))
            if self.draw_trajectory:
                self.trajectory.append(self.position)

    pygame.init()

    screen = pygame.display.set_mode([window_width, window_height])
    pygame.display.set_caption("space")
    font = pygame.font.Font(path + "\\Oxanium-VariableFont_wght.ttf", 10)

    clock = pygame.time.Clock()
    tickTimer = 0

    planets = []
    planets.append(Planet(2 * 10**30, (0, 0), 50, "sun", (255, 255, 0), True))
    planets.append(Planet(6 * 10**24, (50, 0), 10, "earth", (0, 0, 255), True))
    planets.append(Planet(6.4 * 10**23, (231, 0), 9, "mars", (240, 0, 0), True))
    planets.append(Planet(2 * 10**30, (400e+9, 0), 50, "sun 2", (255, 255, 0), True))

    planets[3].velocity = (0, 10000)
    orbit_radius = 150 * distance_factor
    orbital_speed = math.sqrt((G * planets[0].mass) / orbit_radius)
    orbit_duration = 2 * math.pi * math.sqrt(orbit_radius**3 / G * planets[0].mass)

    theta = (2 * math.pi * time) / orbit_duration
    planets[1].position = (orbit_radius, 0)
    planets[1].velocity = (0, orbital_speed)

    orbit_radius = 231 * distance_factor
    orbital_speed = math.sqrt((G * planets[0].mass) / orbit_radius)
    
    planets[2].position = (orbit_radius, 0)
    planets[2].velocity = (0, orbital_speed)

    running = True
    last_update = 0
    while running:
        tickTimer += clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                print("Program ended")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    print("Program ended")
                elif event.key == pygame.K_SPACE:
                    running = False
                    main()
                elif event.key == pygame.K_RIGHT:
                    time_multiplier = time_multiplier * 10
                    last_update = last_update * 10
                    print("Time increased")
                elif event.key == pygame.K_LEFT:
                    time_multiplier = time_multiplier / 10
                    last_update = last_update / 10

        screen.fill((0, 0, 0))

        time = pygame.time.get_ticks() / 1000 * time_multiplier
        delta_time = time - last_update
        if tickTimer >= updateDelay:
            tickTimer = 0
            # gravity
            for planet in planets:
                summed_force_vector = (0, 0)
                for referencePlanet in planets:
                    if referencePlanet == planet: continue
                    pos1 = planet.position
                    pos2 = referencePlanet.position
                    m1 = planet.mass
                    m2 = referencePlanet.mass
                    distance = abs(math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2))
                    if distance < planet.radius * 2: continue
                    
                    force = (G * m1 * m2) / (distance**2)
                    mag = abs(math.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2))

                    normalized_dir = ((pos2[0] - pos1[0]) / mag, (pos2[1] - pos1[1]) / mag)
                    summed_force_vector = (summed_force_vector[0] + (force * normalized_dir[0]), summed_force_vector[1] + (force * normalized_dir[1]))
                acceleration = ((summed_force_vector[0] / m1), (summed_force_vector[1] / m1))
                planet.velocity = (planet.velocity[0] + (acceleration[0] * delta_time), planet.velocity[1] + (acceleration[1] * delta_time))

                planet.updatePosition()
                last_update = time
            # render
            index_counter = 1
            for planet in planets:
                for i in range(len(planet.trajectory)):
                    line_color = (min(255, planet.color[0] +80), min(255, planet.color[1] +80), min(255, planet.color[2] +80))
                    start_pos = (origin[0] + planet.trajectory[i][0] / distance_factor, origin[1] - planet.trajectory[i][1] / distance_factor)
                    if i == len(planet.trajectory) -1:
                        end_pos = (origin[0] + (planet.position[0] / distance_factor), origin[1] - (planet.position[1]) / distance_factor)
                    else:
                        end_pos = (origin[0] + planet.trajectory[i +1][0] / distance_factor, origin[1] - planet.trajectory[i +1][1] / distance_factor)
                    pygame.draw.line(screen, line_color, start_pos, end_pos, 1)
                pygame.draw.circle(screen, planet.color, (origin[0] + (planet.position[0] / distance_factor), origin[1] - (planet.position[1]) / distance_factor), planet.radius)

                info_content = str(planet.name) + " | V: " + str(round(planet.velocity[0], 9)) + ", " + str(round(planet.velocity[1], 9)) + " | Pos: " + str(round(planet.position[0], 3)) + ", " + str(round(planet.position[1], 3))
                info = font.render(info_content, True, (255, 255, 255))
                screen.blit(info, (20, 0 + index_counter*20))
                
                index_counter += 1

            timeinfo = "Time-multiplier: " + str(time_multiplier)
            text_color = (255, 255, 255)
            if time_multiplier >= 100000000:
                text_color = (255, 50, 50)
                timeinfo += " !!! Simulation may be inaccurate"
            text = font.render(timeinfo, True, text_color)
            screen.blit(text, (20, window_height -40))
            pygame.display.update()
main()