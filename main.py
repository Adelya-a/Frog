import pygame
import random

if __name__ == '__main__':
    pygame.init()

    width, height = 1000, 540
    fps = 60
    block_size = 50
    speed = 5
    spawn_rate = 500
    num_obst = 1

    white = (255, 255, 255)
    green = (8, 37, 0)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Frogger quest")

    try:
        frog_image = pygame.image.load('frog.jpg')
        rock_image = pygame.image.load('rock.png')
        log2_image = pygame.image.load('log2.png')
        log_image = pygame.image.load('log1.png')
        background_image = pygame.image.load('background.png')
        background_image_sec = pygame.image.load('background_sec.png')
        pobeda_image = pygame.image.load('Pobeda.png')
    except pygame.error:
        print(f"НЕКРАСИВЫЕ ИЗОБРАЖЕНИЯ! МНЕ НЕ НРАВИТСЯ!")
        exit()

    image_down = [pygame.image.load("Frog_animation/00_Frog_boy.png"),
                  pygame.image.load("Frog_animation/01_Frog_boy.png"),
                  pygame.image.load("Frog_animation/02_Frog_boy.png"),
                  pygame.image.load("Frog_animation/03_Frog_boy.png")]
    image_up = [pygame.image.load("Frog_animation/04_Frog_boy.png"),
                pygame.image.load("Frog_animation/05_Frog_boy.png"),
                pygame.image.load("Frog_animation/06_Frog_boy.png"),
                pygame.image.load("Frog_animation/07_Frog_boy.png")]
    image_left = [pygame.image.load("Frog_animation/09_Frog_boy.png"),
                  pygame.image.load("Frog_animation/08_Frog_boy.png")]
    image_right = [pygame.image.load("Frog_animation/10_Frog_boy.png"),
                   pygame.image.load("Frog_animation/11_Frog_boy.png")]
    move = False
    value = 0
    img = pygame.transform.scale(image_down[value], (40, 50))
    last_im = pygame.transform.scale(image_down[value], (40, 50))
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            width, height = 1000, 540
            self.image = pygame.transform.scale(img, (40, 50))
            self.rect = self.image.get_rect()
            self.rect.center = (25, height // 2 + 100)
        def update(self):
            global value, img, move, screen
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
                self.rect.x -= 6
                move = True
                if value >= len(image_left):
                    value = 0
                img = pygame.transform.scale(image_left[value], (40, 50))
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < 1000:
                self.rect.x += 6
                move = True
                if value >= len(image_right):
                    value = 0
                img = pygame.transform.scale(image_right[value], (40, 50))
            elif (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 0:
                self.rect.y -= 6
                move = True
                if value >= len(image_up):
                    value = 0
                img = pygame.transform.scale(image_up[value], (40, 50))
            elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < 540:
                self.rect.y += 6
                move = True
                if value >= len(image_down):
                    value = 0
                img = pygame.transform.scale(image_down[value], (40, 50))
            else:
                move = False
                if 300 < self.rect.right < 800 and self.rect.bottom < 540:
                    self.rect.y += 1
            if move:
                value += 1
            self.image = pygame.transform.scale(img, (40, 50))
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
            obstacle_type = random.choices(['log1', 'log'])[0]
            x_position = random.randint(300, 750)
            if obstacle_type == 'log1':
                y_position = random.randint(-1 * block_size, -log2_image.get_size()[0])
                obstacle_image = pygame.transform.scale(log2_image, log2_image.get_size())
            else:
                y_position = random.randint(-1 * block_size, -log_image.get_size()[0])
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
        text = font.render("Game Over!", True, green)
        text2 = font.render(" Нажмите SPACE, чтобы продолжить", True, green)
        text_rect = text.get_rect(center=(width // 2, height // 2 + 110))
        text_rect2 = text2.get_rect(center=(width // 2, height // 2 + 170))
        screen.blit(text, text_rect)
        screen.blit(text2, text_rect2)
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
        spawn_rate -= 50
        if level % 2 != 0:
            num_obst += 1
        else:
            speed += 0.5
        show_level_screen(level)
        ready_steady_go()

    clock = pygame.time.Clock()
    running = True
    level = 1
    level_start_time = pygame.time.get_ticks()
    show_start_screen()
    show_level_screen(level)
    ready_steady_go()
    last_spawn_time = pygame.time.get_ticks()


    def show_timer(seconds):
        font = pygame.font.Font(None, 36)
        timer_text = font.render(f"Время: {seconds}s", True, (255,255,255))
        screen.blit(timer_text, (width // 2 - timer_text.get_width() // 2, height - 40))


    def start_timer():
        return pygame.time.get_ticks()


    def calculate_time(start_time):
        return (pygame.time.get_ticks() - start_time) // 1000


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
            all_sprites.empty()
            obstacles.empty()
            player = Player()
            all_sprites.add(player)
            show_level_screen(level)
            ready_steady_go()

        if player.rect.right >= width - block_size:
            print("Ты прошел уровень!")
            level += 1

            level_time = calculate_time(level_start_time)
            print(f"Время на уровень {level - 1}: {level_time} секунд")

            if level > 3:
                print("Поздравляем! Вы прошли все уровни!")
                screen.blit(pobeda_image, (0, 0))
                waiting = True
                running = False
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                    screen.blit(pobeda_image, (0, 0))
                    pygame.display.flip()

            else:
                next_level(level)
                player.rect.center = (25, height // 2 + 100)
                all_sprites.empty()
                obstacles.empty()
                all_sprites.add(player)
                level_start_time = pygame.time.get_ticks()

        screen.blit(background_image_sec, (0, 0))
        all_sprites.draw(screen)
        finish_line_rect = pygame.Rect(width - block_size, 0, block_size, height)
        pygame.draw.rect(screen, green, finish_line_rect)

        level_time = calculate_time(level_start_time)
        if level == 1:
            show_timer(((pygame.time.get_ticks() - level_start_time) // 1000) - 6)
        else:
            show_timer((pygame.time.get_ticks() - level_start_time) // 1000)
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
