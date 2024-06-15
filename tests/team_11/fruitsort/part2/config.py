import pygame
import yaml


# 設定碰撞種類
class CollisionTypes:
    PARTICLE = 1
    WALL = 2


# 把鍵值轉換成屬性
class ConfigNode:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)


# 讀取config.yaml檔,初始化遊戲參數＆圖片
class Config:
    def __init__(self):
        with open("part2/config.yaml", "r") as yaml_file:
            # 把yaml轉換程python字典,存在self.config中
            self.config = yaml.safe_load(yaml_file)
        
        # 把screen, pad, physics中的資料變成屬性, ex: self.screen.width
        self.screen = ConfigNode(**self.config["screen"])
        self.pad = ConfigNode(**self.config["pad"])
        self.physics = ConfigNode(**self.config["physics"])

        # 儲存水果名稱到列表裡
        self.fruit_names = ["one", "two", "three", "four",
                            "five", "six", "seven", "eight", 
                            "nine", "ten", "eleven"]
        
        # 儲存水果圖片到 self.config[name]["blit"] 裡
        for name in self.fruit_names:
            self.config[name]["blit"] = pygame.transform.scale(
                pygame.image.load(f"blits/{name}.png"),
                size = self.config[name]["size"],
            )
        
        # 設定螢幕中心位置
        self.screen_center = (self.screen.width // 2, self.screen.height // 2)
        
        # 載入背景圖片
        background_image = pygame.image.load("blits/background.png")
        self.background_blit = pygame.transform.scale(background_image, (self.screen.width, self.screen.height))
        
        # 載入筷子圖片
        self.cloud_blit = pygame.image.load("blits/cloud.png")

        # 載入開始圖片
        self.start_image = pygame.image.load("blits/open.png")
        self.start_image = pygame.transform.scale(self.start_image, (self.screen.width, self.screen.height))
        
        # 載入結束圖片
        self.game_over_image = pygame.image.load("blits/end.png")
        self.game_over_image = pygame.transform.scale(self.game_over_image, (self.screen.width, self.screen.height))
        
        # 載入開始按鈕圖片
        self.start_button_image = pygame.image.load("blits/enter.png")
        self.start_button_image = pygame.transform.scale(self.start_button_image, (400, 100))
        self.start_button_pos = (self.screen.width // 2 - 200, self.screen.height // 2 + 150)  
        
        # 載入結束按鈕圖片
        self.again_button_image = pygame.image.load("blits/again.png")
        self.again_button_image = pygame.transform.scale(self.again_button_image, (400, 100))
        self.again_button_pos = (self.screen.width // 2 - 200, self.screen.height // 2 + 150)  

        # 顯示 next sushi 的位置
        self.next_sushi_pos = (760, 55)
        self.sushi_size = (100, 100)
    

        self.wheel_image = pygame.image.load("blits/wheel.png")
        self.wheel_image = pygame.transform.scale(self.wheel_image, (300, 300))
        self.wheel_pos = (38, 25)  # 假设轮盘的位置在左上角
        
        
        self.pointer_image = pygame.image.load("blits/needle.png")
        self.pointer_image = pygame.transform.scale(self.pointer_image, (50, 500))
        

    # config[0, "blit"] 返回第一個水果圖片
    def __getitem__(self, key):
        index, field = key
        fruit = self.fruit_names[index]
        return self.config[fruit][field]
    
    # 回傳左上角座標
    @property
    def top_left(self):
        return self.pad.left, self.pad.top
    
    # 回傳左下角座標
    @property
    def bot_left(self):
        return self.pad.left, self.pad.bot
    
    # 回傳右上角座標
    @property
    def top_right(self):
        return self.pad.right, self.pad.top
    
    # 回傳右下角座標
    @property
    def bot_right(self):
        return self.pad.right, self.pad.bot


config = Config()
