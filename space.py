import pygame
import math
import os
import ui_manager as ui

window_width = 800
window_height = 600
origin = (window_width / 2, window_height / 2)
path = os.path.dirname(__file__)

global planets
planets = []

# 1 distance unit >> 1.000.000 km >> 1.000.000.000 m
distance_factor = 10**9

# contants:
G = 6.6743 * 10**-11

# initiate UI
ui.create_group("overlay_group", True)
overlay_group = ui.get_group("overlay_group")
ui.create_button("menu_button", (80, 30), (window_width -100, 20), "Menu")
overlay_group.add_element(ui.get_button("menu_button"))

ui.create_group("menu_group", False)
menu_group = ui.get_group("menu_group")

ui.create_button("load_sun_button", (80, 30), (20, 400), "Load Sun")
menu_group.add_element(ui.get_button("load_sun_button"))

ui.create_button("load_earth_button", (80, 30), (120, 400), "Load Earth")
menu_group.add_element(ui.get_button("load_earth_button"))

ui.create_button("load_mars_button", (80, 30), (220, 400), "Load Mars")
menu_group.add_element(ui.get_button("load_mars_button"))

ui.create_text_input("name_input", (150, 30), (20, 150), "e.g. Mars", 25, "Name")
menu_group.add_element(ui.get_text_input("name_input"))

ui.create_text_input("mass_input", (150, 30), (190, 150), "e.g. 6.39*10**23", 25, "Mass in kg")
menu_group.add_element(ui.get_text_input("mass_input"))

ui.create_text_input("pos_x_input", (150, 30), (360, 150), "e.g. 232*10**9", 10, "Position in m")
ui.create_text_input("pos_y_input", (150, 30), (520, 150), "e.g. 0", 10)
menu_group.add_element(ui.get_text_input("pos_x_input"))
menu_group.add_element(ui.get_text_input("pos_y_input"))

ui.create_text_input("radius_input", (50, 30), (690, 150), "e.g. 20", 10, "Radius (display)")
menu_group.add_element(ui.get_text_input("radius_input"))

ui.create_text_input("color_r_input", (50, 30), (20, 220), "e.g. 235", 3, "Color")
ui.create_text_input("color_g_input", (50, 30), (80, 220), "e.g. 97", 3)
ui.create_text_input("color_b_input", (50, 30), (140, 220), "e.g. 52", 3)
menu_group.add_element(ui.get_text_input("color_r_input"))
menu_group.add_element(ui.get_text_input("color_g_input"))
menu_group.add_element(ui.get_text_input("color_b_input"))

ui.create_checkbox("trajectory_toggle", (210, 220), "Show Trajectory", True)
menu_group.add_element(ui.get_checkbox("trajectory_toggle"))

# orbit
ui.create_checkbox("orbit_toggle", (20, 310), "Orbit")
menu_group.add_element(ui.get_checkbox("orbit_toggle"))

ui.create_text_input("orbit_radius_input", (150, 30), (70, 310), "e.g. 231*10**9", 25, "Orbit Radius in m")
menu_group.add_element(ui.get_text_input("orbit_radius_input"))

ui.create_text_input("orbit_primary_input", (150, 30), (240, 310), "e.g. sun", 25, "Orbit Primary (exact name)")
menu_group.add_element(ui.get_text_input("orbit_primary_input"))

ui.create_button("create_button", (100, 30), (420, 310), "Create Object")
menu_group.add_element(ui.get_button("create_button"))

def menu_toggle():
    menu_group.state = not menu_group.state
ui.get_button("menu_button").assign_function(menu_toggle)

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
    font = pygame.font.Font(path + "\Oxanium-VariableFont_wght.ttf", 12)

    clock = pygame.time.Clock()
    tickTimer = 0
    planets.append(Planet(1*10**-100, (10**100, 0), 0, "dummy"))
    planets.append(Planet(1*10**-100, (-10**100, 0), 0, "dummy"))

    def load_sun():
        planets.pop(0)
        planets.append(Planet(2 * 10**30, (0, 0), 50, "sun", (255, 255, 0), True))
    ui.get_button("load_sun_button").assign_function(load_sun)

    def load_earth():
        primary = None
        for planet in planets:
            if planet.name == "sun":
                primary = planet 
        if primary != None:
            planets.append(Planet(6 * 10**24, (50, 0), 10, "earth", (0, 0, 255), True))
            orbit_radius = 150 * distance_factor
            orbital_speed = math.sqrt((G * primary.mass) / orbit_radius)
            print(orbital_speed)
            orbit_duration = 2 * math.pi * math.sqrt(orbit_radius**3 / G * primary.mass)
            theta = (2 * math.pi * time) / orbit_duration

            planets[-1].position = (orbit_radius, 0)
            planets[-1].velocity = (0, orbital_speed)
        else:
            print("Error: Cannot load earth without objext called 'sun'")
    ui.get_button("load_earth_button").assign_function(load_earth)

    def load_mars():
        primary = None
        for planet in planets:
            if planet.name == "sun":
                primary = planet 
        if primary != None:
            planets.append(Planet(6.4 * 10**23, (231, 0), 9, "mars", (240, 0, 0), True))

            orbit_radius = 240 * distance_factor
            orbital_speed = math.sqrt((G * primary.mass) / orbit_radius)
            orbit_duration = 2 * math.pi * math.sqrt(orbit_radius**3 / G * primary.mass)
            theta = (2 * math.pi * time) / orbit_duration

            planets[-1].position = (orbit_radius, 0)
            planets[-1].velocity = (0, orbital_speed)
        else:
            print("Error: Cannot load mars without objext called 'sun'")
    ui.get_button("load_mars_button").assign_function(load_mars)


    def load_new_planet():
        try:
            planets.append(Planet(eval(ui.get_text_input("mass_input").content),
                                    (eval(ui.get_text_input("pos_x_input").content), 
                                    eval(ui.get_text_input("pos_y_input").content)), 
                                    eval(ui.get_text_input("radius_input").content), 
                                    ui.get_text_input("name_input").content, 
                                    (int(ui.get_text_input("color_r_input").content), 
                                    int(ui.get_text_input("color_g_input").content), 
                                    int(ui.get_text_input("color_b_input").content)), 
                                    ui.get_checkbox("trajectory_toggle").value))
            print("Object successfully loaded")
            if ui.get_checkbox("orbit_toggle").value == True:
                primary = None
                for planet in planets:
                    if planet.name == ui.get_text_input("orbit_primary_input").content:
                        primary = planet
                if primary != None:
                    orbit_radius = eval(ui.get_text_input("orbit_radius_input").content)
                    orbital_speed = math.sqrt((G * primary.mass) / orbit_radius)
                    print(orbital_speed)
                    orbit_duration = 2 * math.pi * math.sqrt(orbit_radius**3 / G * primary.mass)

                    planets[-1].position = (primary.position[0] + orbit_radius, primary.position[1])
                    planets[-1].velocity = (primary.velocity[0], primary.velocity[1] + orbital_speed)
                else:
                    print("Orbit parameters could not be calculated")
            for element in ui.text_inputs:
                element.content = ""
            if len(planets) > 2:
                if planets[0].name == "dummy":
                    planets.pop(0)
        except:
            print("Error: Planet could not be created with given attributes")

    ui.get_button("create_button").assign_function(load_new_planet)

    last_update = 0
    running = True
    print(overlay_group.elements)
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
                elif event.key == pygame.K_TAB:
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
                # print(planet.name, "| Pos: ", planet.position)
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

            # interactables
            if menu_group.state == True:
                menu_surface = pygame.Surface((window_width, window_height))
                menu_surface.set_alpha(200)
                pygame.draw.rect(menu_surface, (0, 0, 0), pygame.Rect((10, 10), (window_width -20, window_height -20)))
                screen.blit(menu_surface, (0, 0))
            else:
                for element in menu_group.elements:
                    element.state = "idle"

            for surface in ui.render((window_width, window_height)):
                screen.blit(surface, (0, 0))
            pygame.display.update()

        for element in ui.buttons:
            element.checkActivity()
        for element in ui.text_inputs:
            element.checkActivity()
        for element in ui.checkboxes:
            element.checkActivity()
main()