import pygame
import math

pygame.init()


WIDTH, HEIGHT = 780, 520
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Мониторинг + Кулер")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (0, 100, 255)
GREEN = (0, 200, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
BG = (30, 30, 30)
YELLOW = (255, 255, 0)


font = pygame.font.SysFont("Arial", 20)
font_big = pygame.font.SysFont("Arial", 30)


temperature = 60
slider_x = 120
slider_width = 300
slider_handle_radius = 12
dragging = False
active_tab = 0


tab_rects = [
    pygame.Rect(10, 10, 140, 40),
    pygame.Rect(160, 10, 140, 40),
    pygame.Rect(310, 10, 140, 40)
]


class CpuCooler:

    def __init__(self, x, y, size=80, color=YELLOW, shape='cross'):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.shape = shape
        self.angle = 0

    def draw(self, surface):

        if self.shape == 'cross':
            self._draw_cross(surface)
        elif self.shape == 'polygon':
            self._draw_polygon(surface)

    def _draw_cross(self, surface):
        half = self.size // 2
        rad = math.radians(self.angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)


        x1 = self.x + half * cos_a
        y1 = self.y + half * sin_a
        x2 = self.x - half * cos_a
        y2 = self.y - half * sin_a
        pygame.draw.line(surface, self.color, (x1, y1), (x2, y2), 6)


        rad2 = rad + math.pi / 2
        x3 = self.x + half * math.cos(rad2)
        y3 = self.y + half * math.sin(rad2)
        x4 = self.x - half * math.cos(rad2)
        y4 = self.y - half * math.sin(rad2)
        pygame.draw.line(surface, self.color, (x3, y3), (x4, y4), 6)

    def _draw_polygon(self, surface):

        points = []
        radius = self.size // 2
        for i in range(6):
            angle_deg = 60 * i + self.angle
            angle_rad = math.radians(angle_deg)
            px = self.x + radius * math.cos(angle_rad)
            py = self.y + radius * math.sin(angle_rad)
            points.append((px, py))

        for i in range(len(points)):
            start = points[i]
            end = points[(i+1) % len(points)]
            pygame.draw.line(surface, self.color, start, end, 4)

    def rotate(self, deg=1):

        self.angle = (self.angle + deg) % 360



cooler = CpuCooler(400, 280, size=100, color=YELLOW, shape='polygon')




def draw_tabs():
    for i, rect in enumerate(tab_rects):
        color = (60, 60, 60) if i != active_tab else (100, 100, 100)
        pygame.draw.rect(screen, color, rect, border_radius=8)
        labels = ["Управление", "Информация", "Кулер"]
        text = font.render(labels[i], True, WHITE)
        screen.blit(text, (rect.x + 20, rect.y + 10))

def draw_slider():
    line_y = 120
    pygame.draw.line(screen, DARK_GRAY, (slider_x, line_y), (slider_x + slider_width, line_y), 6)
    handle_x = slider_x + int((temperature - 30) / 60 * slider_width)
    pygame.draw.circle(screen, BLUE, (handle_x, line_y), slider_handle_radius)
    pygame.draw.circle(screen, WHITE, (handle_x, line_y), slider_handle_radius - 3)
    return handle_x, line_y

def draw_ui():
    screen.fill(BG)
    draw_tabs()

    if active_tab == 0:

        label = font.render("Температура: {} °C".format(temperature), True, WHITE)
        screen.blit(label, (50, 180))
        tip = font.render("Перетащите ползунок", True, GRAY)
        screen.blit(tip, (50, 220))
        draw_slider()

    elif active_tab == 1:

        label_big = font_big.render("Температура процессора:", True, WHITE)
        screen.blit(label_big, (50, 100))
        temp_big = font_big.render("{} °C".format(temperature), True, WHITE)
        screen.blit(temp_big, (50, 150))

        if temperature < 50:
            status_text = "Низкая температура"
            color = BLUE
        elif temperature < 70:
            status_text = "Нормальный режим"
            color = GREEN
        elif temperature < 85:
            status_text = "Повышенная температура"
            color = ORANGE
        else:
            status_text = "КРИТИЧЕСКИЙ ПЕРЕГРЕВ!"
            color = RED
        status = font.render(status_text, True, color)
        screen.blit(status, (50, 220))

    elif active_tab == 2:


        title = font.render("Кулер процессора", True, WHITE)
        screen.blit(title, (50, 80))

        shape_text = font.render("Форма: " + cooler.shape, True, GRAY)
        screen.blit(shape_text, (50, 120))

        btn_cross = pygame.Rect(50, 160, 100, 40)
        btn_poly = pygame.Rect(170, 160, 140, 40)
        pygame.draw.rect(screen, (80, 80, 80), btn_cross, border_radius=5)
        pygame.draw.rect(screen, (80, 80, 80), btn_poly, border_radius=5)
        font_small = pygame.font.SysFont("Arial", 16)
        screen.blit(font_small.render("Крест", True, WHITE), (btn_cross.x + 25, btn_cross.y + 10))
        screen.blit(font_small.render("Многоугольник", True, WHITE), (btn_poly.x + 15, btn_poly.y + 10))

        cooler.draw(screen)

        global btn_cross_rect, btn_poly_rect
        btn_cross_rect = btn_cross
        btn_poly_rect = btn_poly

    pygame.display.flip()


clock = pygame.time.Clock()
running = True
btn_cross_rect = pygame.Rect(0,0,0,0)
btn_poly_rect = pygame.Rect(0,0,0,0)

while running:
    clock.tick(60)
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            for i, rect in enumerate(tab_rects):
                if rect.collidepoint(event.pos):
                    active_tab = i
                    break

            if active_tab == 0:
                handle_x = slider_x + int((temperature - 30) / 60 * slider_width)
                handle_y = 120
                if (mouse_x - handle_x)**2 + (mouse_y - handle_y)**2 <= (slider_handle_radius + 10)**2:
                    dragging = True

            if active_tab == 2:
                if btn_cross_rect.collidepoint(event.pos):
                    cooler.shape = 'cross'
                if btn_poly_rect.collidepoint(event.pos):
                    cooler.shape = 'polygon'

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragging = False

        if event.type == pygame.MOUSEMOTION and dragging:
            rel_x = mouse_x - slider_x
            rel_x = max(0, min(rel_x, slider_width))
            new_temp = int(30 + (rel_x / slider_width) * 60)
            if new_temp != temperature:
                temperature = new_temp


    if active_tab == 2:
        cooler.rotate(2)
    draw_ui()

pygame.quit()