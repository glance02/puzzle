import pygame, sys, random

# 初始化pygame
pygame.init()

# 窗口尺寸
WIDTH = 1000  # x
HEIGHT = 600  # y
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("坦克游戏")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (5, 5, 5)
RED = (255, 0, 0)
RED_DARKER = (200, 0, 0)
GREEN = (0, 255, 0)
GREEN_DARKER = (0, 200, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 120, 0)
ORANGE_DARKER = (200, 80, 0)

# 定义爆炸半径
explosion_radius = 50

class Tanks_code:
    def __init__(self):
        self.xA, self.yA = WIDTH / 4, HEIGHT / 2  # 坦克A的位置
        self.speed = 5  # 坦克速度
        self.width, self.height = 50, 30  # 坦克大小
        self.bullet_speed = 50  # 子弹速度
        self.bullet_radius = 10  # 子弹大小
        self.bullet_color = ORANGE  # 子弹颜色
        self.bullet_xA, self.bullet_yA = int(self.xA + self.width), int(self.yA + self.height / 2)  # 子弹出发位置
        self.canon_xA, self.canon_yA = int(self.xA + self.width / 2), int(self.yA + self.height / 2)  # 坦克炮管位置
        self.bullet_state_A = False
        self.cooldown_time = 600  # 600毫秒 = 0.6秒
        self.last_shot_time = 0
        self.tank_hitbox = pygame.Rect(0, 0, self.width, self.height)  # 坦克碰撞盒
        self.canon_hitbox = pygame.Rect(int((self.xA + self.width / 2)), int(self.yA + (self.height / 2 - 5)), 30, 10)  # 炮管碰撞盒

    def draw_tank(self):
        pygame.draw.rect(window, GREEN, (self.xA, self.yA, self.width, self.height))  # 绘制坦克
        pygame.draw.circle(window, GREEN_DARKER, (int(self.xA + self.width / 2), int(self.yA + self.height / 2)), 10)  # 绘制坦克圆
        pygame.draw.rect(window, GREEN_DARKER, (int(self.xA + self.width / 2), int(self.yA + (self.height / 2 - 5)), 30, 10))  # 绘制炮管
        self.tank_hitbox = pygame.Rect(self.xA, self.yA, self.width, self.height)  # 更新坦克碰撞盒
        self.canon_hitbox = pygame.Rect(int((self.xA + self.width / 2)), int(self.yA + (self.height / 2 - 5)), 30, 10)  # 更新炮管碰撞盒

    def move_tank(self, keys):
        # 使用ZQSD
        if keys[pygame.K_w]:  # w=z 键盘qwerty
            if self.yA - self.speed >= 0:
                self.yA -= self.speed  # 向上移动
        if keys[pygame.K_s]:
            if self.yA + self.speed <= (HEIGHT - self.height):
                self.yA += self.speed  # 向下移动
        if keys[pygame.K_a]:  # a=q 键盘qwerty
            if self.xA - self.speed >= 0:
                self.xA -= self.speed  # 向左移动
        if keys[pygame.K_d]:
            if self.xA + self.speed <= (WIDTH - self.width):
                self.xA += self.speed  # 向右移动

        # 使用方向键
        if keys[pygame.K_LEFT]:
            if self.xA - self.speed >= 0:
                self.xA -= self.speed  # 向左移动
        if keys[pygame.K_RIGHT]:
            if self.xA + self.speed <= (WIDTH - self.width):
                self.xA += self.speed  # 向右移动
        if keys[pygame.K_UP]:
            if self.yA - self.speed >= 0:
                self.yA -= self.speed  # 向上移动
        if keys[pygame.K_DOWN]:
            if self.yA + self.speed <= (HEIGHT - self.height):
                self.yA += self.speed  # 向下移动
        if keys[pygame.K_l]:
            print("您的得分是 " + str(score))
            pygame.quit()
            sys.exit()

    def shoot(self, current_time):
        if current_time - self.last_shot_time > self.cooldown_time and not self.bullet_state_A:
            self.bullet_xA = int(self.xA + self.width)
            self.bullet_yA = int(self.yA + self.height / 2)
            self.bullet_state_A = True
            self.last_shot_time = current_time
            self.bullet_hitbox = pygame.Rect(self.bullet_xA - self.bullet_radius, self.bullet_yA - self.bullet_radius, self.bullet_radius * 2, self.bullet_radius * 2)  # 子弹碰撞盒

    def update_bullet(self):
        if self.bullet_state_A:
            self.bullet_xA += self.bullet_speed
            self.bullet_hitbox.x = self.bullet_xA - self.bullet_radius
            self.bullet_hitbox.y = self.bullet_yA - self.bullet_radius
            if self.bullet_xA > WIDTH:
                self.bullet_state_A = False


tank = Tanks_code()

# 定义敌人数目
NB_ENEMY = 5

class Enemy_code:
    def __init__(self):
        self.size = 20  # 敌人大小
        self.x, self.y = WIDTH - self.size, random.randint(0, int(HEIGHT - self.size))  # 初始位置
        self.color = RED  # 敌人颜色
        self.speed = random.randint(1, 3)  # 敌人速度
        self.hitbox = pygame.Rect(self.x, self.y, self.size, self.size)  # 敌人碰撞盒

    def draw_enemy(self):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.size, self.size))  # 绘制敌人

    def update_enemy(self):
        self.x -= self.speed  # 更新敌人位置
        self.hitbox.x = self.x
        self.hitbox.y = self.y
        if self.x < 0:
            self.x, self.y = WIDTH - self.size, random.randint(0, int(HEIGHT - self.size))  # 重置敌人位置
            self.hitbox.x = self.x
            self.hitbox.y = self.y


enemy_grp = [Enemy_code() for _ in range(NB_ENEMY)]

class life_code:
    def __init__(self):
        self.x, self.y = 10, 10  # 生命条初始位置
        self.width_life, self.height_life = 202, 24  # 生命条大小
        self.width_outline, self.height_outline = 202, 24  # 生命条轮廓大小
        self.color_outline = (0, 0, 0, 0.5)  # 生命条轮廓颜色
        self.color = (0, 255, 0, 0.5)  # 生命条颜色

    def draw_life(self):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width_life, self.height_life))  # 绘制生命条
        pygame.draw.rect(window, self.color_outline, (self.x, self.y, self.width_outline, self.height_outline), 2)  # 绘制生命条轮廓

    def update_life(self):
        self.width_life -= 20
        if self.width_life < 10:
            for radius in range(explosion_radius, 81, 5):
                window.fill(BLACK)
                pygame.draw.circle(window, ORANGE, (int(tank.xA + (tank.width / 2)), int(tank.yA + (tank.height / 2))), radius)
                if radius > 30:
                    pygame.draw.circle(window, ORANGE_DARKER, (int(tank.xA + (tank.width / 2)), int(tank.yA + (tank.height / 2))), radius - 20)
                pygame.display.flip()
                pygame.time.delay(30)
            window.fill(BLACK)
            pygame.time.delay(500)
            font = pygame.font.Font(None, 36)
            text = font.render("游戏结束！您的得分是 " + str(score), True, WHITE)
            text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            window.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.delay(3000)
            pygame.quit()
            sys.exit()


life = life_code()

# 变量得分
score = 0

# 函数敌人被击中
def enemy_touch(score, enemy):
    score += 1
    tank.bullet_state_A = False
    for radius in range(explosion_radius, 51, 5):
        window.fill(WHITE)  # 清除屏幕
        for e in enemy_grp:
            e.draw_enemy()
        tank.draw_tank()
        pygame.draw.circle(window, ORANGE, (enemy.x + int((enemy.size / 2)), enemy.y + int((enemy.size / 2))), radius)  # 绘制爆炸效果
        explosion_hitbox = pygame.Rect(enemy.x + int((enemy.size / 2)) - radius, enemy.y + int((enemy.size / 2)) - radius, radius * 2, radius * 2)
        for e in enemy_grp:
            if e != enemy and explosion_hitbox.colliderect(e.hitbox):
                enemy.x = WIDTH - enemy.size
                enemy.y = random.randint(0, HEIGHT - enemy.size)
                enemy.hitbox.x = enemy.x
                enemy.hitbox.y = enemy.y
                score = enemy_touch(score, e)  # 递归调用更新得分
        pygame.display.flip()
    enemy.x = WIDTH - enemy.size
    enemy.y = random.randint(0, HEIGHT - enemy.size)
    enemy.hitbox.x = enemy.x
    enemy.hitbox.y = enemy.y
    return score

# *****************************************主循环*****************************************
clock = pygame.time.Clock()
while True:
    # 为了正确退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("您的得分是 " + str(score))
            pygame.quit()
            sys.exit()
    window.fill(WHITE)
    current_time = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()
    life.draw_life()

    tank.move_tank(keys)
    if keys[pygame.K_SPACE] and not tank.bullet_state_A:
        tank.shoot(current_time)
    tank.update_bullet()
    enemies_off_screen = 0
    for enemy in enemy_grp:  # 对于所有在地图上的敌人
        enemy.update_enemy()
        if enemy.x <= 0:  # 如果一个敌人碰到左边的屏幕边缘
            enemies_off_screen += 1  # 计数，以便知道有多少敌人碰到边缘，从而减少生命值
        if tank.bullet_state_A and tank.bullet_hitbox.colliderect(enemy.hitbox):
            score = enemy_touch(score, enemy)  # 更新得分
        if tank.tank_hitbox.colliderect(enemy.hitbox) or tank.canon_hitbox.colliderect(enemy.hitbox):
            enemy.x = WIDTH - enemy.size
            enemy.y = random.randint(0, HEIGHT - enemy.size)
            enemy.hitbox.x = enemy.x
            enemy.hitbox.y = enemy.y
            life.update_life()
        enemy.draw_enemy()
    for die in range(enemies_off_screen):
        life.update_life()

    if tank.bullet_state_A:
        pygame.draw.circle(window, tank.bullet_color, (tank.bullet_xA, tank.bullet_yA), tank.bullet_radius)  # 绘制子弹
    tank.draw_tank()
    pygame.display.flip()
    # 限制主循环速度为60 FPS
    clock.tick(60)
