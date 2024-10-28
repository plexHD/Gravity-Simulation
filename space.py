import pygame
import math
import os

window_width = 800
window_height = 600
origin = (window_width / 2, window_height / 2)
path = os.path.dirname(__file__)

planets = []

# 1 distance unit >> 1.000.000 km >> 1.000.000.000 m
distance_factor = 10**9

# contants:
G = 6.6743 * 10**-11

# ui elements
buttons = []
in_menu = []
text_inputs = []

class Button():
    def __init__(self, input_dimensions, input_position, input_text):
        self.dimensions = input_dimensions
        self.position = input_position
        self.text = input_text

        self.idle_color = (30, 30, 30)
        self.hovered_color = (50, 50, 50)
        self.pressed_color = (70, 70, 100)
        self.text_color = (255, 255, 255)
        self.color = self.idle_color

        self.state = "idle" # "hovered, pressed"
        self.button_rect = pygame.Rect(self.position, self.dimensions)

        self.action_function = None

        buttons.append(self)

    def checkActivity(self):
        if self.position[0] <= pygame.mouse.get_pos()[0] <= self.position[0] + self.dimensions[0] and self.position[1] <= pygame.mouse.get_pos()[1] <= self.position[1] + self.dimensions[1]:
            self.state = "hovered"
            self.color = self.hovered_color
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    self.state = "pressed"
                    self.color = self.pressed_color
                    self.action_function()
                    try:
                        pass
                    except:
                        print("Error: No actionfunction assigned to button")
        else:
            self.state = "idle"
            self.color = self.idle_color

    def assign_function(self, action_function):
        self.action_function = action_function

class Text_input():
    def __init__(self, input_dimensions, input_position, input_placeholder, input_max_content_len):
        self.dimensions = input_dimensions
        self.position = input_position
        self.placeholder = input_placeholder

        self.content = ""
        self.max_content_len = input_max_content_len

        self.idle_color = (30, 30, 30)
        self.hovered_color = (50, 50, 50)
        self.selected_color = (70, 70, 100)
        self.text_color = (255, 255, 255)
        self.color = self.idle_color

        self.input_rect = pygame.Rect(self.position, self.dimensions)

        self.state = "idle"
        text_inputs.append(self)

    def checkActivity(self):
        if self.position[0] <= pygame.mouse.get_pos()[0] <= self.position[0] + self.dimensions[0] and self.position[1] <= pygame.mouse.get_pos()[1] <= self.position[1] + self.dimensions[1]:
            if self.state == "idle":
                self.state = "hovered"
            if pygame.mouse.get_just_released()[0] == True:
                self.state = "selected"
                for element in text_inputs:
                    if element == self: continue
                    element.state = "idle"
        elif self.state == "hovered":
            self.state = "idle"
        elif pygame.mouse.get_just_released()[0] == True and self.state == "selected":
            self.state = "idle"
        
        if self.state == "selected":
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        self.state = "idle"
                    elif event.key == pygame.K_BACKSPACE:
                        self.content = self.content[:-1]
                    elif event.key == pygame.K_SPACE and len(self.content) <= self.max_content_len:
                        self.content += " "
                    elif len(self.content) <= self.max_content_len:
                        self.content += event.unicode 

        if self.state == "idle":
            self.color = self.idle_color
        elif self.state == "hovered":
            self.color = self.hovered_color
        else:
            self.color = self.selected_color

# initiate UI
def menu():
    global menu_opened
    if menu_opened == False:
        menu_opened = True
    else: 
        menu_opened = False

menu_opened = False

menu_button = Button((80, 30), (window_width -100, 20), "Menu")
menu_button.assign_function(menu)

load_default_button = Button((80, 30), (window_width -200, 20), "Load Default")

name_input = Text_input((150, 30), (20, 150), "Planet Name", 25)
in_menu.append(name_input)

mass_input = Text_input((150, 30), (190, 150), "Mass", 25)
in_menu.append(mass_input)

pos_x_input = Text_input((50, 30), (360, 150), "X", 10)
pos_y_input = Text_input((50, 30), (420, 150), "Y", 10)
in_menu.append(pos_x_input)
in_menu.append(pos_y_input)

radius_input = Text_input((50, 30), (490, 150), "Radius", 10)
in_menu.append(radius_input)

color_r_input = Text_input((50, 30), (560, 150), "R", 3)
color_g_input = Text_input((50, 30), (620, 150), "G", 3)
color_b_input = Text_input((50, 30), (680, 150), "B", 3)
in_menu.append(color_r_input)
in_menu.append(color_g_input)
in_menu.append(color_b_input)

create_button = Button((100, 30), (630, 200), "Create Object")
in_menu.append(create_button)

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
    font = pygame.font.Font(path + "/data/fonts/Oxanium-VariableFont_wght.ttf", 12)

    clock = pygame.time.Clock()
    tickTimer = 0

    def load_default():
        planets.append(Planet(2 * 10**30, (0, 0), 50, "sun", (255, 255, 0), True))
        planets.append(Planet(6 * 10**24, (50, 0), 10, "earth", (0, 0, 255), True))
        planets.append(Planet(6.4 * 10**23, (231, 0), 9, "mars", (240, 0, 0), True))

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

    load_default_button.assign_function(load_default)

    def load_new_planet():
        try:
            planets.append(Planet(eval(mass_input.content), (eval(pos_x_input.content), eval(pos_y_input.content)), eval(radius_input.content), name_input.content, (int(color_r_input.content), int(color_g_input.content), int(color_b_input.content)), True))
            print("Object successfully loaded")
        except:
            print("Error: Planet could not be created with given attributes")

    create_button.assign_function(load_new_planet)

    last_update = 0
    running = True
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
            if menu_opened:
                pygame.draw.rect(screen, (100, 100, 100, 100), pygame.Rect((10, 10), (window_width -20, window_height -20)))

            for element in buttons:
                element.checkActivity()
                if element in in_menu and menu_opened == False: continue
                pygame.draw.rect(screen, element.color, element.button_rect)
                button_content = font.render(element.text, True, element.text_color)
                screen.blit(button_content, (element.position[0] + (element.dimensions[0] / 2 - button_content.width / 2), element.position[1] + (element.dimensions[1] / 2 - button_content.height / 2)))

            for element in text_inputs:
                element.checkActivity()
                if element in in_menu and menu_opened == False: continue
                pygame.draw.rect(screen, element.color, element.input_rect)
                if element.content != "":
                    text_content = font.render(element.content, True, element.text_color)
                else:
                    text_content = font.render(element.placeholder, True, element.text_color)
                screen.blit(text_content, (element.position[0] + element.dimensions[0] / 2 - text_content.width / 2, element.position[1] + element.dimensions[1] / 2 - text_content.height / 2))

            pygame.display.update()

        for element in buttons:
            element.checkActivity()
        for element in text_inputs:
            element.checkActivity()
main()