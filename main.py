import pygame
import random

if __name__ == '__main__':
    pygame.init()

    # Константы
    width, height = 900, 540
    fps = 60
    block_size = 50
    speed = 5
    spawn_rate = 500
    num_obst = 4

    # Цвета
    white = (255, 255, 255)
    green = (8, 37, 0)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Crossy Road Inspired Game")

    try:
        frog_image = pygame.image.load('frog.jpg')
        rock_image = pygame.image.load('rock.png')
        log2_image = pygame.image.load('log2.png')
        log_image = pygame.image.load('log1.png')
        background_image = pygame.image.load('background.png')
    except pygame.error:
        print(f"НЕКРАСИВЫЕ ИЗОБРАЖЕНИЯ! МНЕ НЕ НРАВИТСЯ!")
        exit()

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.transform.scale(frog_image, (block_size, block_size))
            self.rect = self.image.get_rect()
            self.rect.center = (block_size // 2, height - block_size)

        def update(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a] and self.rect.left > 0:
                self.rect.x -= 5
            if keys[pygame.K_RIGHT] or keys[pygame.K_d] and self.rect.right < width:
                self.rect.x += 5
            if keys[pygame.K_UP] or keys[pygame.K_w] and self.rect.top > 0:
                self.rect.y -= 5
            if keys[pygame.K_DOWN] or keys[pygame.K_s] and self.rect.bottom < height:
                self.rect.y += 5


    class Obstacle(pygame.sprite.Sprite):
        def __init__(self, x, y, image):
            super().__init__()
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        def update(self):
            self.rect.y += speed
            if self.rect.top > height:
                self.kill()

    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)


    def create_obstacles():
        for _ in range(num_obst):
            if level == 1:
                weights1 = [2, 2, 2]
            elif level == 2:
                weights1 = [3, 2, 3]
            else:
                weights1 = [5, 1, 3]
            obstacle_type = random.choices(['rock', 'water', 'log'], weights=weights1, k=1)[0]
            x_position = random.randint(0, (width // block_size) - 1) * block_size
            if obstacle_type == 'rock':
                y_position = random.randint(-3 * block_size, -block_size)
                obstacle_image = pygame.transform.scale(rock_image, rock_image.get_size())
            elif obstacle_type == 'water':
                y_position = random.randint(-3 * block_size, -block_size)
                obstacle_image = pygame.transform.scale(log2_image, log2_image.get_size())
            else:  # log
                y_position = random.randint(-3 * block_size, -block_size)
                obstacle_image = pygame.transform.scale(log_image, log_image.get_size())

            obstacle = Obstacle(x_position, y_position, obstacle_image)
            all_sprites.add(obstacle)
            obstacles.add(obstacle)


    def show_start_screen():
        screen.blit(background_image, (0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("Нажмите SPACE чтобы начать", True, green)
        text_rect = text.get_rect(center=(width // 2, height // 2 + 115))
        screen.blit(text, text_rect)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False

    def show_level_screen(level):
        screen.blit(background_image, (0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render(f"Уровень {level}", True, green)
        text_rect = text.get_rect(center=(width // 2, height // 2 + 115))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(3000)

    def ready_steady_go():
        for text in ["На старт!", "Внимание!", "Марш!"]:
            screen.blit(background_image, (0, 0))
            font = pygame.font.Font(None, 74)
            text_surface = font.render(text, True, green)
            text_rect = text_surface.get_rect(center=(width // 2, height // 2 + 115))

            screen.blit(text_surface, text_rect)
            pygame.display.flip()
            pygame.time.delay(1000)

    def game_over():
        screen.blit(background_image, (0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over! Нажмите SPACE чтобы продолжить", True, green)
        text_rect = text.get_rect(center=(width // 2, height // 2 + 115))
        screen.blit(text, text_rect)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False

    def next_level(level):
        global speed, spawn_rate, num_obst
        speed += 1
        spawn_rate -= 50
        num_obst += 1
        show_level_screen(level)
        ready_steady_go()

    clock = pygame.time.Clock()
    running = True
    level = 1
    show_start_screen()
    show_level_screen(level)
    ready_steady_go()
    last_spawn_time = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time >= spawn_rate:
            create_obstacles()
            last_spawn_time = current_time

        all_sprites.update()

        if pygame.sprite.spritecollideany(player, obstacles):
            print("Game Over!")
            game_over()
            spawn_rate = 500
            num_obst = 4
            all_sprites.empty()
            obstacles.empty()
            player = Player()
            all_sprites.add(player)
            show_start_screen()
            show_level_screen(level)
            ready_steady_go()

        if player.rect.right >= width:
            print("You Win!")
            level += 1
            if level > 2:
                print("Поздравляем! Вы прошли все уровни!")
                running = False
            else:
                next_level(level)
                player.rect.center = (block_size // 2, height - block_size)
                all_sprites.empty()
                obstacles.empty()
                all_sprites.add(player)

        screen.fill(white)

        all_sprites.draw(screen)

        finish_line_rect = pygame.Rect(width - block_size, 0, block_size, height)
        pygame.draw.rect(screen, green, finish_line_rect)

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()


