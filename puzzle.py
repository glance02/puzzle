import pygame
import random
import sys
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


class Game:
    def __init__(self, width=600, height=600, grid_size=3):
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.tile_size = width // grid_size
        self.white = (255, 255, 255)
        self.whiteblock = pygame.image.load("./blackblock.jpg")

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("拼图游戏")
        self.font = pygame.font.Font(None, 36)
        self.IMAGE_PATH = "./picture1.jpg"  # 不要忘记转义反斜杠
        self.TIME_LIMIT = 120  # 时间限制

        self.tiles = []
        self.selected_index = None
        self.clock = pygame.time.Clock()
        self.start_ticks = None
        self.dragging = False  # 添加这个变量来跟踪是否在拖动
        self.drag_tile_index = None  # 用于记录拖动的拼图块索引
        self.dragged_tile_image = None  # 储存拖动拼图块的图像
        self.old_tile_image = None
        self.old_tile_image_index = None

    def load_image(self, path):
        try:
            image = pygame.image.load(path)
            image = pygame.transform.scale(image, (self.width, self.height))
            tiles = []
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    rect = (j * self.tile_size, i * self.tile_size, self.tile_size, self.tile_size)
                    tile = image.subsurface(rect)
                    tiles.append(tile)
            return tiles
        except pygame.error as e:
            print(f"无法加载图像: {path}, 错误信息: {e}")
            sys.exit()

    def shuffle_tiles(self):
        random.shuffle(self.tiles)

    def draw_tiles(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                tile = self.tiles[i * self.grid_size + j]
                if tile is not None:
                    self.screen.blit(tile, (j * self.tile_size, i * self.tile_size))

    def swap_tiles(self, index1, index2):
        self.tiles[index1], self.tiles[index2] = self.tiles[index2], self.tiles[index1]

    def draw_text(self, text, position):
        label = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(label, position)

    def check_win(self, right_image):
        for i in range(self.grid_size * self.grid_size):
            tile1_data = np.frombuffer(self.tiles[i].get_buffer().raw, dtype=np.uint8)
            tile2_data = np.frombuffer(right_image[i].get_buffer().raw, dtype=np.uint8)
            if not np.array_equal(tile1_data, tile2_data):
                return False
        return True

    def view_original_image(self):  # 添加的查看原图方法
        original_image = pygame.image.load(self.IMAGE_PATH)
        original_image = pygame.transform.scale(original_image, (self.width, self.height))
        viewing = True
        while viewing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    viewing = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # 按下ESC键退出查看原图
                        viewing = False

            self.screen.fill(self.white)
            self.screen.blit(original_image, (0, 0))
            pygame.display.flip()

    def game_loop(self):
        self.start_ticks = pygame.time.get_ticks()
        self.tiles = self.load_image(self.IMAGE_PATH)
        right_image = self.load_image(self.IMAGE_PATH)

        while self.check_win(right_image):
            self.shuffle_tiles()

        while True:
            self.screen.fill(self.white)

            self.draw_tiles()

            if self.check_win(right_image):
                find_dialogue = tk.Tk()
                find_dialogue.geometry('300x130')  # 设置对话框大小和位置
                find_dialogue.title("你很勇嘛")  # 设置对话框标题
                find_dialogue.resizable(0, 0)  # 不可调整大小
                # 添加标签显示信息
                message_label = tk.Label(find_dialogue, text="Congratulations! You win!", font=("宋体", 14))
                message_label.pack(pady=20)  # 添加一个标签并设置上边距
                
                ok_button = tk.Button(find_dialogue, text="确定", command=lambda: find_dialogue.destroy())  
                ok_button.pack(pady=10)  # 添加按钮并设置上边距

                pygame.display.flip()
                # 等待对话框关闭
                find_dialogue.wait_window()  # 等待对话框关闭
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    clicked_index = (mouse_y // self.tile_size) * self.grid_size + (mouse_x // self.tile_size)

                    if self.tiles[clicked_index] is not None:
                        self.selected_index = None  # 取消单击选择
                        self.dragging = True  # 开始拖动
                        self.drag_tile_index = clicked_index  # 记录拖动的拼图块索引
                        self.dragged_tile_image = self.tiles[self.drag_tile_index]  # 获取被拖动的拼图块图像
                        self.old_tile_image = self.tiles[self.drag_tile_index]  # 储存被拖动的拼图块图像
                        self.old_tile_image_index = clicked_index  # 储存被拖动的拼图块索引
                        self.tiles[self.drag_tile_index] = self.whiteblock  # 显示白块占位符 

                if event.type == pygame.MOUSEMOTION:
                    if self.dragging:  # 如果正在拖动
                        mouse_x, mouse_y = event.pos  # 更新鼠标位置

                if event.type == pygame.MOUSEBUTTONUP:
                    if self.dragging:  # 如果正在拖动并且松开鼠标
                        mouse_x, mouse_y = event.pos
                        target_index = (mouse_y // self.tile_size) * self.grid_size + (mouse_x // self.tile_size)
                        if self.tiles[target_index] is not None:
                            # 显示原来的拼图块图像
                            self.tiles[self.old_tile_image_index] = self.old_tile_image  
                            self.swap_tiles(self.drag_tile_index, target_index)  # 交换拼图块
                            self.dragging = False  # 停止拖动
                        self.drag_tile_index = None  # 重置拖动索引
                        self.dragged_tile_image = None  # 重置拖动图像

                # 添加查看原图的事件
                if event.type == pygame.KEYDOWN:
                    if event.unicode == 'q' or event.unicode == 'Q':  # 按下'Q'键查看原图
                        self.view_original_image()

            elapsed_time = (self.TIME_LIMIT - (pygame.time.get_ticks() - self.start_ticks) // 1000)
            self.draw_text(f"time: {elapsed_time}s", (10, 10))

            # 如果是时间到，则游戏结束
            if elapsed_time <= 0:
                # 创建对话框
                find_dialogue = tk.Tk()
                find_dialogue.geometry('300x130')  # 设置对话框大小和位置
                find_dialogue.title("你很弱欸")  # 设置对话框标题
                find_dialogue.resizable(0, 0)  # 不可调整大小
                # 添加标签显示信息
                message_label = tk.Label(find_dialogue, text="Time's up! You lose!", font=("Arial", 14))
                message_label.pack(pady=20)  # 添加一个标签并设置上边距
                
                ok_button = tk.Button(find_dialogue, text="确定", command=lambda: find_dialogue.destroy())  
                ok_button.pack(pady=10)  # 添加按钮并设置上边距

                # 更新Pygame显示
                pygame.display.flip()
                
                # 等待对话框关闭
                find_dialogue.wait_window()  # 等待对话框关闭
                break

            if self.dragging and self.dragged_tile_image is not None:
                # 如果正在拖动，绘制被拖动的拼图块在鼠标位置
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.screen.blit(self.dragged_tile_image, (mouse_x - self.tile_size // 2, mouse_y - self.tile_size // 2))

            pygame.display.flip()
            self.clock.tick(60)

class Menu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("菜单界面")
        self.root.geometry("400x450")
        self.GAME_IMAGE_PATH = "./picture1.jpg"
        self.GAME_GRID = 3
        self.GAME_TIME = 120

        # 创建一个框架来承载所有的组件
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack(expand=True)

        # 提示标签
        title_label = tk.Label(self.frame, text="拼图游戏", font=("楷体", 24))
        title_label.pack(pady=10)

        # 选择图片按钮
        image_button = tk.Button(self.frame, text="选择图片", command=self.select_image, width=20)
        image_button.pack(pady=5)

        # 添加时间输入框
        time_label = tk.Label(self.frame, text="请输入拼图时间:")
        time_label.pack(pady=5)
        self.time_entry = tk.Entry(self.frame)
        self.time_entry.pack(pady=5)

        # 添加分割次数输入框
        segment_label = tk.Label(self.frame, text="请输入分割次数:")
        segment_label.pack(pady=5)
        self.segment_entry = tk.Entry(self.frame)
        self.segment_entry.pack(pady=5)

        # 添加提交按钮
        submit_button = tk.Button(self.frame, text="开始游戏", command=self.exit_program, width=20)
        submit_button.pack(pady=10)

        # 提示信息
        tips_label = tk.Label(self.frame, text="提示: 按 'Q' 键查看原图, ESC 退出原图状态", bg="#ADD8E6", fg="black", font=("宋体", 12))
        tips_label.pack(pady=10)

        self.root.mainloop()

    def select_image(self):
        file_path = filedialog.askopenfilename(title="选择图片", filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")])
        if file_path:
            self.GAME_IMAGE_PATH = file_path  # 更新游戏中的图片路径

    def exit_program(self):
        self.GAME_GRID = int(self.segment_entry.get()) if self.segment_entry.get().isdigit() else 3  # 更新游戏中的分割次数，默认值为3
        self.GAME_TIME = int(self.time_entry.get()) if self.time_entry.get().isdigit() else 120  # 更新游戏中的时间，默认值为120
        self.root.quit()  # 退出主循环
        self.root.destroy()  # 销毁窗口
        game = Game(600, 600, self.GAME_GRID)
        game.IMAGE_PATH = self.GAME_IMAGE_PATH
        game.TIME_LIMIT = self.GAME_TIME
        game.game_loop()


if __name__ == "__main__":
    menu = Menu()
