# -*- coding:utf-8 -*-
import pygame
from pygame.locals import *
import sys

def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Test") 

    while (1):
        screen.fill((0,0,0))        # 画面を黒色(#000000)に塗りつぶし
        pygame.display.update()     # 画面を更新

        # イベント処理
        for event in pygame.event.get():
            if event.type == QUIT:  # 閉じるボタンが押されたら終了
                pygame.quit()       # Pygameの終了(画面閉じられる)
                sys.exit()


if __name__ == "__main__":
    main()
