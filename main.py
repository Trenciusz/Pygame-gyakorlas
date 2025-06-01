import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kasa Paint")
FONT = pygame.font.SysFont("Arial", 16)

preset_colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (0, 0, 0),
]
current_color = preset_colors[0]

shapes = []
shape_buttons = []
shape_types = [
    ("Kitöltött téglalap", 'rect', True),
    ("Körvonalas téglalap", 'rect', False),
    ("Kitöltött ovális", 'oval', True),
    ("Körvonalas ovális", 'oval', False),
]
current_shape = 'rect'
fill_shape = True
outline_width = 2

drawing = False
start_pos = None
temp_rect = None

toolbar_height = 60
button_width = 150
button_height = 30
padding = 10

for i, (label, shape, filled) in enumerate(shape_types):
    rect = pygame.Rect(10 + i * (button_width + padding), 10, button_width, button_height)
    shape_buttons.append((rect, label, shape, filled))

color_buttons = []
for i, color in enumerate(preset_colors):
    rect = pygame.Rect(10 + i * 40, toolbar_height, 30, 30)
    color_buttons.append((rect, color))

running = True
while running:
    screen.fill((255, 255, 255))

    for shape_type, rect, color, filled, o_width in shapes:
        width = 0 if filled else o_width
        if shape_type == 'rect':
            pygame.draw.rect(screen, color, rect, width)
        else:
            pygame.draw.ellipse(screen, color, rect, width)

    if drawing and temp_rect:
        width = 0 if fill_shape else outline_width
        if current_shape == 'rect':
            pygame.draw.rect(screen, current_color, temp_rect, width)
        else:
            pygame.draw.ellipse(screen, current_color, temp_rect, width)

    pygame.draw.rect(screen, (230, 230, 230), (0, 0, WIDTH, toolbar_height + 50))

    for rect, label, shape, filled in shape_buttons:
        pygame.draw.rect(screen, (200, 200, 255) if (current_shape == shape and fill_shape == filled) else (180, 180, 180), rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)
        screen.blit(FONT.render(label, True, (0, 0, 0)), (rect.x + 5, rect.y + 7))

    for rect, color in color_buttons:
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)
        if current_color == color:
            pygame.draw.rect(screen, (255, 255, 255), rect, 3)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for rect, label, shape, filled in shape_buttons:
                if rect.collidepoint(event.pos):
                    current_shape = shape
                    fill_shape = filled
                    break
            for rect, color in color_buttons:
                if rect.collidepoint(event.pos):
                    current_color = color
                    break
            else:
                if event.pos[1] > toolbar_height + 50:
                    start_pos = event.pos
                    drawing = True

        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                end_pos = event.pos
                temp_rect = pygame.Rect(start_pos, (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
                temp_rect.normalize()

        elif event.type == pygame.MOUSEBUTTONUP:
            if drawing and temp_rect:
                shapes.append((current_shape, temp_rect, current_color, fill_shape, outline_width))
            drawing = False
            temp_rect = None

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                if shapes:
                    shapes.pop()

    pygame.display.flip()

pygame.quit()
sys.exit()
