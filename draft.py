from tkinter import *  # 导入Tkinter库
from tkinter import filedialog, simpledialog, messagebox  # 从Tkinter中导入文件对话框、简单对话框和消息框
import random  # 导入random库以随机化
from PIL import Image, ImageTk  # 导入Pillow库，用于图像处理

root = Tk()  # 创建主窗口
root.title('拼图游戏1')  # 设置窗口标题

Width = 720  # 游戏窗口宽度
Height = 720  # 游戏窗口高度
steps = 0  # 初始化步骤计数
board = []  # 用于存放棋盘状态
pics = []  # 用于存放图像切片
original_image = None  # 原始图像
Rows, Cols = 3, 3  # 默认行数和列数

# 创建开始游戏的界面
def start_menu():
    menu_window = Toplevel(root)  # 创建一个新的窗口
    menu_window.title("开始游戏2")  # 设置窗口标题

    # 选择图片按钮的功能
    def select_image():
        global original_image, img, Rows, Cols  # 使用全局变量
        file_path = filedialog.askopenfilename(title="选择图片3", filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")])  # 弹出对话框选择图片
        if not file_path:  # 如果没有选择图片
            return  # 结束函数
        original_image = Image.open(file_path)  # 打开选中的图片
        img = original_image.resize((Width, Height), Image.LANCZOS)  # 调整为合适的大小
        
        # 获取切割行数和列数
        get_board_size(menu_window)  # 调用函数获取行列数

    # 弹出对话框获取切割行数和列数
    def get_board_size(menu_window):
        global Rows, Cols  # 使用全局变量
        Rows = simpledialog.askinteger("输入行数", "请输入切割的行数（最小为 2）：", minvalue=2)  # 弹出对话框输入行数
        if Rows is None:  # 如果取消
            return  # 结束函数
        Cols = Rows  # 列数默认为行数
        menu_window.destroy()  # 关闭菜单窗口
        play_game()  # 开始游戏

    # 创建选择图片和开始游戏的按钮
    b_select_image = Button(menu_window, text="开始游戏4", command=select_image, width=20)  # 创建按钮
    b_select_image.pack(pady=10)  # 将按钮放入窗口中

# 游戏逻辑
def init_board():
    global board  # 使用全局变量
    board = [[None for _ in range(Cols)] for _ in range(Rows)]  # 初始化棋盘为空
    l = list(range(Rows * Cols))  # 创建包含所有块的列表
    random.shuffle(l)  # 随机打乱顺序
    
    for i in range(Rows):  # 遍历行
        for j in range(Cols):  # 遍历列
            idx = i * Cols + j  # 计算索引
            orderID = l[idx]  # 获取随机顺序的ID
            if orderID == Cols * Rows - 1:  # 如果是最后一个块:  
                board[i][j] = None  # 将空白块设置为None
            else:
                board[i][j] = Square(orderID)  # 保留其他方块

def draw_board(canvas):  # 负责绘制棋盘
    canvas.create_rectangle((0, 0, Width, Height), width=1, outline='Black', fill='green')  # 绘制棋盘边界
    for i in range(Rows):  # 遍历行
        for j in range(Cols):  # 遍历列
            if board[i][j] is None:  # 如果是空白块
                canvas.create_rectangle(j * (Width // Cols), i * (Height // Rows),  # 绘制白色矩形
                                         (j + 1) * (Width // Cols), (i + 1) * (Height // Rows), fill='white', outline='black')
            else:  # 不是空白块
                board[i][j].draw(canvas, ((Width // Cols) * (j + 0.5), (Height // Rows) * (i + 0.5)))  # 绘制方块

def mouse_click(event):  # 处理鼠标点击事件
    global steps  # 使用全局变量
    r = int(event.y // (Height // Rows))  # 计算行
    c = int(event.x // (Width // Cols))  # 计算列
    if 0 <= r < Rows and 0 <= c < Cols:  # 确保点击在棋盘范围内
        if board[r][c] is None:  # 如果点击的是空白块
            return  # 不做处理
        current_square = board[r][c]  # 获取当前方块
        empty_positions = [(r - 1, c), (r, c + 1), (r + 1, c), (r, c - 1)]  # 可能的空白块位置
        for nr, nc in empty_positions:  # 遍历空白块位置
            if 0 <= nr < Rows and 0 <= nc < Cols and board[nr][nc] is None:  # 如果是有效位置且为空
                board[r][c] = None  # 移动当前方块到空位置
                board[nr][nc] = current_square
                steps += 1  # 步骤数增加
                break  # 跳出循环
    label1.config(text=str(steps))  # 更新步骤数标签
    cv.delete('all')  # 清空画布
    draw_board(cv)  # 重新绘制棋盘
    if win():  # 检查是否胜利
        messagebox.showinfo(title='祝贺', message='你赢了')  # 显示胜利消息
        root.quit()  # 退出程序

class Square:  # 定义方块类
    def __init__(self, orderID):  # 初始化方块
        self.orderID = orderID  # 设置方块ID
        self.image = pics[orderID]  # 获取方块对应的图像

    def draw(self, canvas, board_pos):  # 绘制方块
        canvas.create_image(board_pos, image=self.image)  # 在画布上绘制图像

def win():  # 检查是否胜利
    for i in range(Rows):  # 遍历行
        for j in range(Cols):  # 遍历列
            if board[i][j] and board[i][j].orderID != i * Cols + j:  # 如果方块不在正确位置
                return False  # 返回未胜利
    return True  # 所有方块在正确位置，返回胜利

def play_game():  # 开始游戏
    global steps, pics  # 使用全局变量
    steps = 0  # 重置步骤数
    pics.clear()  # 清空之前的图片切片
    image_width = Width // Cols  # 计算每个方块的宽度
    image_height = Height // Rows  # 计算每个方块的高度

    # 切分图像
    for i in range(Rows):  # 遍历行
        for j in range(Cols):  # 遍历列
            box = (j * image_width, i * image_height, (j + 1) * image_width, (i + 1) * image_height)  # 计算切分区域
            part = img.crop(box)  # 裁剪图像
            pics.append(ImageTk.PhotoImage(part))  # 将切片添加到图片列表中
    init_board()  # 初始化棋盘
    cv.delete('all')  # 清空画布
    draw_board(cv)  # 重新绘制棋盘

def callBack():  # 重来按钮的回调函数
    print("重来")  # 控制台输出
    play_game()  # 重新开始游戏

def show_original_image():  # 查看原图的功能
    # 创建一个新窗口显示原始图片
    original_window = Toplevel(root)  # 创建一个新的窗口
    original_window.title("原图")  # 设置窗口标题
    
    original_img_tk = ImageTk.PhotoImage(original_image.resize((Width, Height), Image.LANCZOS))  # 调整原图大小并转换为Tkinter格式
    
    # 创建标签显示原始图片
    label = Label(original_window, image=original_img_tk)  # 创建标签
    label.image = original_img_tk  # 保存对图像的引用
    label.pack()  # 将标签放入窗口

# 创建画布和控件
cv = Canvas(root, bg='white', width=Width, height=Height)  # 创建画布
b1 = Button(root, text="重来", command=callBack, width=20)  # 重来按钮
b2 = Button(root, text="查看原图", command=show_original_image, width=20)  # 查看原图按钮
label1 = Label(root, text='0', fg='red', width=20)  # 步骤数标签
label1.pack()  # 将标签放入窗口
cv.bind("<Button-1>", mouse_click)  # 绑定鼠标点击事件
cv.pack()  # 将画布放入窗口
b1.pack()  # 将重来按钮放入窗口
b2.pack()  # 将查看原图按钮放入窗口

start_menu()  # 显示开始游戏菜单

root.mainloop()  # 进入主事件循环
