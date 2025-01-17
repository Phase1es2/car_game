import pygame
import config
from game_manager import GameManager
from utils.draw_text import draw_text

pygame.init()
pygame.mixer.init()
#pygame.font.init()

screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
clock = pygame.time.Clock()

ico = pygame.image.load("static/images/maze_logo.png").convert()
pygame.display.set_icon(ico)

pygame.mixer.music.load("static/sounds/bgm.wav")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

game_manager = GameManager(screen, 1)

running = True
success_time = -1
success_finished = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif success_finished and event.type == pygame.KEYDOWN:  # 如果已通关，则按任意键结束
            running = False

    if success_finished:
        screen.fill("black")
        draw_text(screen, "Winner Winner Chicken Dinner!", 50, config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2)
    else:
        if success_time >= 0:
            if pygame.time.get_ticks() - success_time > 2000:  # 如果获胜后已经等待了2秒，则加载下一关
                has_next = game_manager.next_level()
                if not has_next:  # 如果没有下一关，则游戏结束
                    success_finished = True
                    continue
                success_time = -1   # 将获胜时间清空
        screen.fill("black")
        if game_manager.update():
            success_time = pygame.time.get_ticks()  # 更新获胜时刻

    pygame.display.flip()
    clock.tick(config.FPS)

pygame.quit()
