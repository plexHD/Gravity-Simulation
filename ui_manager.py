import pygame
import os

pygame.init()

path = os.path.dirname(__file__)
font = pygame.font.Font(path + "\Oxanium-VariableFont_wght.ttf", 12)

# ui elements
groups = []
buttons = []
text_inputs = []
checkboxes = []

def create_group(input_group_id, input_state=True):
    groups.append(Group(input_group_id, input_state))
def get_group(input_id):
    for group in groups:
        if group.id == input_id:
            return group
    return None

def create_button(input_id, input_dimensions, input_position, input_text):
    buttons.append(Button(input_id, input_dimensions, input_position, input_text))
def get_button(input_id):
    for element in buttons:
        if element.id == input_id:
            return element
    return None

def create_text_input(input_id, input_dimensions, input_position, input_text, input_max_content_len, input_description=""):
    text_inputs.append(Text_input(input_id, input_dimensions, input_position, input_text, input_max_content_len, input_description))
def get_text_input(input_id):
    for element in text_inputs:
        if element.id == input_id:
            return element
    return None

def create_checkbox(input_id, input_position, input_description="", input_default_value=False, input_size=30):
    checkboxes.append(Checkbox(input_id, input_position, input_description, input_default_value, input_size))
def get_checkbox(input_id):
    for element in checkboxes:
        if element.id == input_id:
            return element
    return None

class Group():
    def __init__(self, input_group_id, input_state):
        self.id = input_group_id
        self.elements = []
        self.state = input_state
    
    def add_element(self, input_element):
        self.elements.append(input_element)
    
    def set_state(self, new_state=True):
        self.state = new_state

class Button():
    def __init__(self, input_id, input_dimensions, input_position, input_text):
        self.id = input_id

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
    def __init__(self, input_id, input_dimensions, input_position, input_placeholder, input_max_content_len, input_description):
        self.id = input_id

        self.dimensions = input_dimensions
        self.position = input_position
        self.placeholder = input_placeholder
        self.description = input_description

        self.content = ""
        self.max_content_len = input_max_content_len

        self.idle_color = (30, 30, 30)
        self.hovered_color = (50, 50, 50)
        self.selected_color = (70, 70, 100)
        self.text_color = (255, 255, 255)
        self.color = self.idle_color

        self.input_rect = pygame.Rect(self.position, self.dimensions)

        self.state = "idle"

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
                    elif event.key == pygame.K_TAB:
                        self.state = "idle"
                        index = text_inputs.index(self)
                        if index != len(text_inputs) -1: 
                            text_inputs[index +1].state = "selected"
                        else:
                            text_inputs[0].state = "selected"
                    elif len(self.content) <= self.max_content_len:
                        self.content += event.unicode 

        if self.state == "idle":
            self.color = self.idle_color
        elif self.state == "hovered":
            self.color = self.hovered_color
        else:
            self.color = self.selected_color

class Checkbox():
    def __init__(self, input_id, input_position, input_description, input_default_value, input_size):
        self.id = input_id
        self.position = input_position

        self.state = "idle" # "hovered", "pressed"
        self.value = input_default_value
        self.description = input_description

        self.idle_color = (30, 30, 30)
        self.hovered_color = (70, 70, 70)
        self.check_color = (170, 170, 255)
        self.text_color = (255, 255, 255)
        self.color = self.idle_color

        self.size = input_size
        self.base_rect = pygame.Rect(self.position, (self.size, self.size))
        self.check_rect = pygame.Rect((self.position[0] + 8, self.position[1] + 8), (self.size - 16, self.size - 16))

    def checkActivity(self):
        if self.position[0] <= pygame.mouse.get_pos()[0] <= self.position[0] + self.size and self.position[1] <= pygame.mouse.get_pos()[1] <= self.position[1] + self.size:
            self.state = "hovered"
            self.color = self.hovered_color
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    self.value = not self.value
        else:
            self.state = "idle"
            self.color = self.idle_color
        
def render(screen_dimensions):
    surfaces = []
    for group in groups:
        if group.state == False: continue

        for element in group.elements:
            if element in buttons:
                new_surface = pygame.Surface(screen_dimensions, pygame.SRCALPHA)
                element.checkActivity()
                pygame.draw.rect(new_surface, element.color, element.button_rect)
                button_content = font.render(element.text, True, element.text_color)
                new_surface.blit(button_content, (element.position[0] + (element.dimensions[0] / 2 - button_content.width / 2), element.position[1] + (element.dimensions[1] / 2 - button_content.height / 2)))
                surfaces.append(new_surface)

            elif element in text_inputs:
                element.checkActivity()
                new_surface = pygame.Surface(screen_dimensions, pygame.SRCALPHA)
                pygame.draw.rect(new_surface, element.color, element.input_rect)
                if element.content != "":
                    text_content = font.render(element.content, True, element.text_color)
                else:
                    text_content = font.render(element.placeholder, True, element.text_color)
                new_surface.blit(text_content, (element.position[0] + element.dimensions[0] / 2 - text_content.width / 2, element.position[1] + element.dimensions[1] / 2 - text_content.height / 2))
                description = font.render(element.description, True, element.text_color)
                new_surface.blit(description, (element.position[0], element.position[1] - description.height))
                surfaces.append(new_surface)

            elif element in checkboxes:
                element.checkActivity()
                new_surface = pygame.Surface(screen_dimensions, pygame.SRCALPHA)
                pygame.draw.rect(new_surface, element.color, element.base_rect)
                if element.value == True:
                    pygame.draw.rect(new_surface, element.check_color, element.check_rect)
                description = font.render(element.description, True, element.text_color)
                new_surface.blit(description, (element.position[0], element.position[1] - description.height))
                surfaces.append(new_surface)
    return surfaces