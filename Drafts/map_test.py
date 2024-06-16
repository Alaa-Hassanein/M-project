import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos, background):
        super().__init__()
        self.image = image
        self.pos = pygame.Vector2(pos)
        self.rect = self.image.get_rect(center=self.pos)
        self.background = background

    def update(self, events, dt):
        pressed = pygame.key.get_pressed()
        move = pygame.Vector2((0, 0))
        if pressed[pygame.K_w]: move += (0, -1)
        if pressed[pygame.K_a]: move += (-1, 0)
        if pressed[pygame.K_s]: move += (0, 1)
        if pressed[pygame.K_d]: move += (1, 0)
        if move.length() > 0: move.normalize_ip()

        new_pos = self.pos + move*(dt/5)
        new_rect = self.rect.copy()
        new_rect.center = new_pos
        new_rect.clamp_ip(self.background.get_rect())
        new_pos = new_rect.center
        
        hit_box = self.background.subsurface(new_rect)
        print(type(new_rect))
        for x in range(new_rect.width):
            for y in range(new_rect.height):
                if sum(hit_box.get_at((x, y))) < 500:
                    
                    return

        self.pos = new_pos
        self.rect.center = self.pos

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    screen_rect = screen.get_rect()

    clock = pygame.time.Clock()
    sprites = pygame.sprite.Group()

    background = pygame.transform.scale2x(pygame.image.load('maze.jpg'))
    pimg = pygame.Surface((10, 10))
    pimg.fill((200, 20, 20))
    sprites.add(Player(pimg, (50, 50), background))

    dt = 0
    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return

        sprites.update(events, dt)
        screen.fill(pygame.Color('grey'))
        screen.blit(background, (0, 0))
        sprites.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60)

if __name__ == '__main__':
    main()