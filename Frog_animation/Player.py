import pygame

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
            if 300 < self.rect.right < 800:
                self.rect.y += 1
        if move:
            value += 1
        self.image = pygame.transform.scale(img, (40, 50))
