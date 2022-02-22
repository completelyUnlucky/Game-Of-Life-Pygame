import pygame

pygame.init()
width = 1600
height = 900
screen = pygame.display.set_mode((width, height))
x, y = 0, 0
running = True


class Cell:
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.alive = False
        self.colors = [(0, 0, 0), (255, 255, 255)]

    def show(self):
        if self.alive:
            pygame.draw.rect(screen, self.colors[self.alive], (self.x, self.y, self.width, self.height))

    def dying(self):
        self.alive = not self.alive


class Background:
    def __init__(self, width, height):
        self.cells = []
        self.width = width
        self.height = height
        self.square_size = 20
        for i in range(self.height // self.square_size):
            self.cells.append([])
            for j in range(self.width // self.square_size):
                self.cells[-1].append(Cell(j * 20, i * 20, self.square_size, self.square_size))

    def draw_cells(self):
        for i in range(self.height // self.square_size):
            for j in range(self.width // self.square_size):
                self.cells[i][j].show()

    def neighbors_alive(self, x, y):
        check = 0
        neighbourhood = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1),
                         (x, y + 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]
        for i, j in neighbourhood:
            if 0 <= i < self.width // self.square_size and 0 <= j < self.height // self.square_size:
                if self.cells[j][i].alive:
                    check += 1
        return check

    def rules(self, neighbours, x, y):
        if self.cells[y][x].alive and 3 >= neighbours >= 2:
            return True
        if neighbours == 3:
            return True

    def next_step(self):
        new_cells = []
        for i in range(self.height // self.square_size):
            new_cells.append([])
            for j in range(self.width // self.square_size):
                new_cells[-1].append(Cell(j * 20, i * 20, self.square_size, self.square_size))
                if self.rules(self.neighbors_alive(j, i), j, i):
                    new_cells[i][j].dying()
        self.cells = new_cells.copy()


b = Background(width, height)
pause = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            screen.fill((0, 0, 0))
            b.cells[y // 20][x // 20].dying()
            b.draw_cells()
            pygame.display.flip()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause = not pause
    if not pause:
        screen.fill((0, 0, 0))
        b.next_step()
        b.draw_cells()
        pygame.display.flip()
