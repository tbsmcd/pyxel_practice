# -*- coding: utf-8 -*-
import pyxel
import random

# 定義値
WINDOW_W = 160
WINDOW_H = 120
BEER_W = 16
BEER_H = 16
ZOMBIE_W = 16
ZOMBIE_H = 16


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Beer:
    def __init__(self, img_id):
        self.pos = Vector(0, 0)
        self.img_beer = img_id
        # ビールの x 軸方向の向き
        self.vec_x = 0

    def update(self, x, y, vec_x):
        self.pos.x = x
        self.pos.y = y
        self.vec_x = vec_x


class Bubble:
    def __init__(self):
        self.pos = Vector(0, 0)
        self.vec_x = 0
        self.size = 2
        self.speed = 3
        # White
        self.color = 7

    def update(self, x, y, vec_x, size=None, color=None):
        self.pos.x = x
        self.pos.y = y
        self.vec_x = vec_x
        if size is not None:
            self.size = size
        if color is not None:
            self.color = color


class Zombie:
    def __init__(self, img_id):
        self.pos = Vector(0, 0)
        self.vec_x = 0
        self.speed = 0
        self.img_zombie = img_id

    def update(self, x, y, vec_x):
        self.pos.x = x
        self.pos.y = y
        self.vec_x = vec_x


class App:
    def __init__(self):
        # ビール
        self.IMG_0 = 0
        self.IMG_0_X = 60
        self.IMG_0_Y = 65
        # ゾンビ
        self.IMG_1 = 1

        pyxel.init(WINDOW_W, WINDOW_H, caption='ビールが泡を噴射してゾンビを殺す')
        pyxel.image(self.IMG_0).load(0, 0, 'img/beer.png')
        pyxel.image(self.IMG_1).load(0, 0, 'img/zombie.png')

        # ビールと泡のインスタンス
        self.beer = Beer(self.IMG_0)
        self.Bubbles = []
        self.Zombies = []

        # Flag
        self.init_flag = 1
        self.game_over = 0

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        #
        # 初期配置
        #
        if self.init_flag == 1:
            # ビールの初期位置
            self.beer.update(WINDOW_W / 4, WINDOW_H / 4 + 30, 1)

            # ゾンビは複数作成可能だが今回は1体
            new_zombie = Zombie(self.IMG_1)
            new_zombie.update(WINDOW_W/2, WINDOW_H/2 + 30, self.beer.vec_x)
            self.Zombies.append(new_zombie)
            self.init_flag = 0

        dx = 0
        dy = 0
        move_flag = 0
        if pyxel.btnp(pyxel.KEY_J):
            dy = 4
            # 縦方向の動きの場合は以前の向きを保持する
            vec_x = self.beer.vec_x
            move_flag = 1
        elif pyxel.btnp(pyxel.KEY_K):
            dy = -4
            vec_x = self.beer.vec_x
            move_flag = 1
        elif pyxel.btnp(pyxel.KEY_H):
            dx = -4
            # 横方向の動きのときは向きに反映
            vec_x = dx
            move_flag = 1
        elif pyxel.btnp(pyxel.KEY_L):
            dx = 4
            vec_x = dx
            move_flag = 1
        # ビールの移動
        if move_flag == 1:
            self.beer.update(self.beer.pos.x + dx, self.beer.pos.y + dy, vec_x)

        for i in range(len(self.Zombies)):
            # ゾンビがビールに近づく
            if random.randrange(9) % 3 == 0:
                rand_int = random.randrange(10)
                if self.Zombies[i].pos.x == self.beer.pos.x or\
                        (self.Zombies[i].pos.y != self.beer.pos.y and rand_int % 2 == 0):
                    # Y軸方向に動く
                    new_zombie_x = self.Zombies[i].pos.x
                    if self.Zombies[i].pos.y > self.beer.pos.y:
                        new_zombie_y = self.Zombies[i].pos.y - 1
                    else:
                        new_zombie_y = self.Zombies[i].pos.y + 1
                else:
                    new_zombie_y = self.Zombies[i].pos.y
                    if self.Zombies[i].pos.x > self.beer.pos.x:
                        new_zombie_x = self.Zombies[i].pos.x - 1
                    else:
                        new_zombie_x = self.Zombies[i].pos.x + 1
                self.Zombies[i].update(new_zombie_x, new_zombie_y, self.beer.vec_x)

            # ビールとゾンビの当たり判定
            if (
                (self.beer.pos.x < self.Zombies[i].pos.x + ZOMBIE_W)
                and (self.Zombies[i].pos.x + ZOMBIE_W < self.beer.pos.x + BEER_W)
                and (self.beer.pos.y < self.Zombies[i].pos.y + ZOMBIE_H)
                and (self.Zombies[i].pos.y + ZOMBIE_H < self.beer.pos.y + BEER_H)
                or
                (self.beer.pos.x < self.Zombies[i].pos.x)
                and (self.Zombies[i].pos.x < self.beer.pos.x + BEER_W)
                and (self.beer.pos.y < self.Zombies[i].pos.y + ZOMBIE_H)
                and (self.Zombies[i].pos.y + ZOMBIE_H < self.beer.pos.y + BEER_H)
                or
                (self.beer.pos.x < self.Zombies[i].pos.x + ZOMBIE_W)
                and (self.Zombies[i].pos.x + ZOMBIE_W < self.beer.pos.x + BEER_W)
                and (self.beer.pos.y < self.Zombies[i].pos.y)
                and (self.Zombies[i].pos.y < self.beer.pos.y + BEER_H)
                or
                (self.beer.pos.x < self.Zombies[i].pos.x)
                and (self.Zombies[i].pos.x < self.beer.pos.x + BEER_W)
                and (self.beer.pos.y < self.Zombies[i].pos.y)
                and (self.Zombies[i].pos.y < self.beer.pos.y + BEER_H)
            ):
                self.game_over = 1

        #
        # 泡操作
        #
        if pyxel.btnp(pyxel.KEY_F):
            new_bubble = Bubble()
            if self.beer.vec_x > 0:
                bubble_margin = 6
            else:
                bubble_margin = -6
            new_bubble.update(self.beer.pos.x + BEER_W / 2 + bubble_margin, self.beer.pos.y + 3, self.beer.vec_x)
            self.Bubbles.append(new_bubble)

        new_bubbles = []
        for bubble in self.Bubbles:
            # print(bubble.pos.x)
            if (bubble.pos.x > -16) and (bubble.pos.x < WINDOW_W):
                if bubble.vec_x > 0:
                    bubble.update(bubble.pos.x + bubble.speed, bubble.pos.y, bubble.vec_x)
                else:
                    bubble.update(bubble.pos.x - bubble.speed, bubble.pos.y, bubble.vec_x)
                # インスタンス削除（生き残りだけ拾う）
                new_bubbles.append(bubble)
                # 泡とゾンビの当たり判定
                new_zombies = []
                for zombie in self.Zombies:
                    if not (
                        (zombie.pos.x < bubble.pos.x) and (zombie.pos.x + ZOMBIE_W > bubble.pos.x)
                            and
                        (zombie.pos.y < bubble.pos.y) and (zombie.pos.y + ZOMBIE_H > bubble.pos.y)
                    ):
                        new_zombies.append(zombie)
                # print(len(self.Zombies))
                self.Zombies = new_zombies
        self.Bubbles = new_bubbles

    def draw(self):
        pyxel.cls(0)
        pyxel.text(15, 40, 'H: LEFT, J: DOWN, K: UP, L: RIGHT', 10)
        pyxel.text(15, 50, 'F: SHOOT BUBBLES', pyxel.frame_count % 16)
        pyxel.text(15, 60, 'Q: QUIT', 10)

        # ビール描画
        if self.beer.vec_x > 0:
            pyxel.blt(self.beer.pos.x, self.beer.pos.y, self.beer.img_beer, 0, 0, -BEER_W, BEER_H)
        else:
            pyxel.blt(self.beer.pos.x, self.beer.pos.y, self.beer.img_beer, 0, 0, BEER_W, BEER_H)
        # 泡描画
        for bubble in self.Bubbles:
            pyxel.circ(bubble.pos.x, bubble.pos.y, bubble.size, bubble.color)

        # ゾンビ描画
        for zombie in self.Zombies:
            if zombie.vec_x > 0:
                pyxel.blt(zombie.pos.x, zombie.pos.y, zombie.img_zombie, 0, 0, -ZOMBIE_W, ZOMBIE_H)
            else:
                pyxel.blt(zombie.pos.x, zombie.pos.y, zombie.img_zombie, 0, 0, ZOMBIE_W, ZOMBIE_H)

        # ゲームオーバー
        if self.game_over == 1:
            pyxel.text(self.beer.pos.x - 10, self.beer.pos.y - 8, 'I WAS DRUNK!', 7)


App()
