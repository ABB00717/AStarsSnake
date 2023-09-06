import pygame
import random
from queue import PriorityQueue

# 定義螢幕寬高和每個方塊的尺寸
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BLOCK_SIZE = 20

# 定義顏色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 定義方向
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

# 定義貪吃蛇類別
class Snake:
    def __init__(self):
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.food = self.generate_food()

    # 生成食物的座標
    def generate_food(self):
        while True:
            x = random.randint(0, SCREEN_WIDTH // BLOCK_SIZE - 1) * BLOCK_SIZE
            y = random.randint(0, SCREEN_HEIGHT // BLOCK_SIZE - 1) * BLOCK_SIZE
            if (x, y) not in self.body:
                return x, y

    # 更新貪吃蛇位置和得分
    def update(self):
        x, y = self.body[0]
        if self.direction == UP:
            y -= BLOCK_SIZE
        elif self.direction == DOWN:
            y += BLOCK_SIZE
        elif self.direction == LEFT:
            x -= BLOCK_SIZE
        elif self.direction == RIGHT:
            x += BLOCK_SIZE

        if x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT or (x, y) in self.body[1:]:
            return False

        self.body.insert(0, (x, y))
        if self.body[0] == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            self.body.pop()

        return True

    # 改變貪吃蛇的方向
    def change_direction(self, direction):
        if direction == UP and self.direction != DOWN:
            self.direction = direction
        elif direction == DOWN and self.direction != UP:
            self.direction = direction
        elif direction == LEFT and self.direction != RIGHT:
            self.direction = direction
        elif direction == RIGHT and self.direction != LEFT:
            self.direction = direction

    # 繪製貪吃蛇和食物
    def draw(self, screen):
        for x, y in self.body:
            pygame.draw.rect(screen, GREEN, (x, y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, RED, (self.food[0], self.food[1], BLOCK_SIZE, BLOCK_SIZE))

# 定義A*算法的節點類別
class Node:
    def __init__(self, position, g_cost, h_cost, parent=None):
        self.position = position
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost
        self.parent = parent

    def __lt__(self, other):
        return self.f_cost < other.f_cost

# 使用A*算法尋找最短路徑
def find_path(snake, target):
    start = Node(snake.body[0], 0, manhattan_distance(snake.body[0], target))
    open_list = PriorityQueue()
    open_list.put(start)
    closed_list = set()

    while not open_list.empty():
        current_node = open_list.get()
        current_position = current_node.position

        if current_position == target:
            path = []
            while current_node.parent:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        closed_list.add(current_position)

        for direction in [UP, DOWN, LEFT, RIGHT]:
            new_position = get_new_position(current_position, direction)
            if new_position[0] < 0 or new_position[0] >= SCREEN_WIDTH or new_position[1] < 0 or new_position[1] >= SCREEN_HEIGHT:
                continue
            if new_position in snake.body[1:]:
                continue
            if new_position in closed_list:
                continue

            new_g_cost = current_node.g_cost + 1
            new_h_cost = manhattan_distance(new_position, target)
            new_f_cost = new_g_cost + new_h_cost
            new_node = Node(new_position, new_g_cost, new_h_cost, parent=current_node)

            open_list.put(new_node)

    return []

# 計算兩點間的曼哈頓距離
def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# 獲取新的位置
def get_new_position(position, direction):
    x, y = position
    if direction == UP:
        return x, y - BLOCK_SIZE
    elif direction == DOWN:
        return x, y + BLOCK_SIZE
    elif direction == LEFT:
        return x - BLOCK_SIZE, y
    elif direction == RIGHT:
        return x + BLOCK_SIZE, y

# 獲取下一個方向
def get_direction(current_position, next_position):
    if next_position[0] < current_position[0]:
        return LEFT
    elif next_position[0] > current_position[0]:
        return RIGHT
    elif next_position[1] < current_position[1]:
        return UP
    elif next_position[1] > current_position[1]:
        return DOWN

# 初始化 pygame
pygame.init()

# 建立螢幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake AI")

# 初始化貪吃蛇
snake = Snake()

# 遊戲迴圈
running = True
clock = pygame.time.Clock()

while running:
    # 檢查事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 使用A*算法找到最短路徑
    path = find_path(snake, snake.food)

    if len(path) > 0:
        next_position = path[0]
        next_direction = get_direction(snake.body[0], next_position)
        snake.change_direction(next_direction)

    # 更新貪吃蛇
    if not snake.update():
        running = False

    # 繪製遊戲畫面
    screen.fill(BLACK)
    snake.draw(screen)
    pygame.display.flip()

    # 控制遊戲速度
    clock.tick(10)

# 關閉 pygame
pygame.quit()
