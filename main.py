import pygame
import random

if __name__ == '__main__':
    pygame.init()

    width, height = 1000, 540
    fps = 60
    block_size = 50
    speed = 5
    spawn_rate = 500
    num_obst = 4

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
        end_image = pygame.image.load('home.png')
    except pygame.error:
        print(f"НЕКРАСИВЫЕ ИЗОБРАЖЕНИЯ! МНЕ НЕ НРАВИТСЯ!")
        exit()

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.transform.scale(frog_image, (block_size, block_size))
            self.rect = self.image.get_rect()
            self.rect.center = (25, height // 2 + 100)

        def update(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a] and self.rect.left > 0:
                self.rect.x -= 7
            if keys[pygame.K_RIGHT] or keys[pygame.K_d] and self.rect.right < width:
                self.rect.x += 7
            if keys[pygame.K_UP] or keys[pygame.K_w] and self.rect.top > 0:
                self.rect.y -= 7
            if keys[pygame.K_DOWN] or keys[pygame.K_s] and self.rect.bottom < height:
                self.rect.y += 7


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
            obstacle_type = random.choices(['rock', 'water', 'log'], k=1)[0]
            x_position = random.randint(50, 800)
            if obstacle_type == 'rock':
                y_position = random.randint(-3 * block_size, -rock_image.get_size()[0])
                obstacle_image = pygame.transform.scale(rock_image, rock_image.get_size())
            elif obstacle_type == 'water':
                y_position = random.randint(-3 * block_size, -log2_image.get_size()[0])
                obstacle_image = pygame.transform.scale(log2_image, log2_image.get_size())
            else:
                y_position = random.randint(-3 * block_size, -log_image.get_size()[0])
                obstacle_image = pygame.transform.scale(log_image, log_image.get_size())

            obstacle = Obstacle(x_position, y_position, obstacle_image)
            all_sprites.add(obstacle)
            obstacles.add(obstacle)


    def show_start_screen():
        screen.blit(background_image, (0, 0))
        font = pygame.font.Font(None, 74)
        #pygame.draw.rect(screen, '#449B6A', pygame.Rect(0, 350, 1000, 1000))
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
        #pygame.draw.rect(screen, (148, 215, 118), pygame.Rect(width // 30, 250, 1000, 1000), 0, 30)
        font = pygame.font.Font(None, 74)
        text = font.render(f"Уровень {level}", True, green)
        text_rect = text.get_rect(center=(width // 2, height // 2 + 115))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(3000)

    def ready_steady_go():
        for text in ["На старт!", "Внимание!", "Марш!"]:
            screen.blit(background_image, (0, 0))
            #pygame.draw.rect(screen, (148, 215, 118), pygame.Rect(width // 30, 250, 1000, 1000), 0, 30)
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
       # pygame.draw.rect(screen, (148, 215, 118), pygame.Rect(width // 30, 250, 1000, 1000), 0, 30)
        # pygame.draw.rect(screen, (148, 215, 118), pygame.Rect(width // 30, 250, 950, 150), 0, 30)
        text_rect = text.get_rect(center=(width // 2, height // 2 + 30))
        text_rect2 = text2.get_rect(center=(width // 2, height // 2 + 80))
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
        speed += 0.5
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
            spawn_rate = 1000
            all_sprites.empty()
            obstacles.empty()
            player = Player()
            all_sprites.add(player)
            show_level_screen(level)
            ready_steady_go()

        if player.rect.right >= width:
            print("You Win!")
            level += 1
            spawn_rate -= 50
            if level > 1:
                print("Поздравляем! Вы прошли все уровни!")
                #screen.blit(end_image, (0, 0))
                # pygame.display.flip()
                # waiting = True
                # while waiting:
                #     for event in pygame.event.get():
                #         if event.type == pygame.QUIT:
                #             pygame.quit()
                #             exit()
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


