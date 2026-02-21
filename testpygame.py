import pygame
import sys
import random
import math

# ── Khởi tạo ─────────────────────────────────
pygame.init()

WIDTH, HEIGHT = 800, 500
GROUND_Y = 400
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Demo - Chuong 1")
clock = pygame.time.Clock()

# ── Màu sắc ──────────────────────────────────
WHITE   = (255, 255, 255)
BLACK   = (0,   0,   0  )
RED     = (220, 50,  50 )
BLUE    = (60,  100, 220)
GREEN   = (50,  180, 80 )
YELLOW  = (255, 215, 0  )
SKY1    = (30,  30,  80 )   # bầu trời trên
SKY2    = (80,  60,  120)   # bầu trời dưới
GROUND  = (60,  140, 50 )
DIRT    = (100, 70,  30 )
BROWN   = (80,  50,  20 )

# ── Font ─────────────────────────────────────
font_big   = pygame.font.SysFont("consolas", 28, bold=True)
font_small = pygame.font.SysFont("consolas", 18)

# ── Sprite: Player ───────────────────────────
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((36, 52), pygame.SRCALPHA)
        self.rect  = self.image.get_rect(midbottom=(150, GROUND_Y))
        self.vel_y = 0
        self.on_ground = False
        self.facing = 1       # 1 phải, -1 trái
        self.anim_timer = 0
        self.anim_frame = 0

    def draw_character(self, frame):
        surf = pygame.Surface((36, 52), pygame.SRCALPHA)
        leg_bob = int(math.sin(frame * 0.5) * 4) if self.on_ground else 0

        # Thân
        pygame.draw.rect(surf, (50, 100, 200), (10, 20, 16, 18))
        pygame.draw.rect(surf, (80, 130, 230), (11, 21, 8, 8))  # highlight

        # Đầu
        pygame.draw.rect(surf, (245, 195, 140), (8, 4, 20, 18))
        # Tóc
        pygame.draw.rect(surf, (60, 30, 0), (8, 4, 20, 7))
        # Mắt
        pygame.draw.rect(surf, WHITE, (14, 11, 5, 5))
        pygame.draw.rect(surf, (0, 80, 200), (15, 12, 3, 3))
        pygame.draw.rect(surf, BLACK, (16, 13, 2, 2))

        # Chân
        pygame.draw.rect(surf, (30, 60, 150), (10, 38, 6, 12 + leg_bob))
        pygame.draw.rect(surf, (30, 60, 150), (20, 38, 6, 12 - leg_bob))
        pygame.draw.rect(surf, BROWN, (9, 48 + leg_bob, 8, 4))
        pygame.draw.rect(surf, BROWN, (19, 48 - leg_bob, 8, 4))

        # Tay
        pygame.draw.rect(surf, (245, 195, 140), (2, 22, 8, 12))
        pygame.draw.rect(surf, (245, 195, 140), (26, 22, 8, 12))

        return surf

    def update(self, dt):
        keys = pygame.key.get_pressed()

        # Di chuyển ngang
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]:
            self.rect.x -= 220 * dt
            self.facing = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += 220 * dt
            self.facing = 1

        # Nhảy
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = -520
            self.on_ground = False

        # Trọng lực
        self.vel_y += 900 * dt
        self.rect.y += self.vel_y * dt

        # Va chạm mặt đất
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.vel_y = 0
            self.on_ground = True

        # Giới hạn màn hình
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))

        # Animation
        if self.on_ground and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or
                                keys[pygame.K_a]   or keys[pygame.K_d]):
            self.anim_timer += dt
            if self.anim_timer > 0.1:
                self.anim_timer = 0
                self.anim_frame += 1
        else:
            self.anim_frame = 0

        # Vẽ nhân vật
        self.image = self.draw_character(self.anim_frame)
        if self.facing == -1:
            self.image = pygame.transform.flip(self.image, True, False)


# ── Sprite: Enemy ────────────────────────────
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((34, 34), pygame.SRCALPHA)
        self.rect  = self.image.get_rect(midbottom=(x, GROUND_Y))
        self.speed = random.uniform(80, 130)
        self.dir   = -1
        self.timer = 0

    def draw_slime(self, t):
        surf = pygame.Surface((34, 34), pygame.SRCALPHA)
        bob  = int(math.sin(t * 6) * 3)

        # Thân
        pygame.draw.ellipse(surf, (200, 40, 40), (2, 8 + bob, 30, 22 - bob))
        pygame.draw.ellipse(surf, (230, 80, 80), (6, 10 + bob, 14, 10))

        # Mắt
        pygame.draw.rect(surf, YELLOW, (6, 12 + bob, 6, 6))
        pygame.draw.rect(surf, YELLOW, (22, 12 + bob, 6, 6))
        pygame.draw.rect(surf, BLACK, (7, 13 + bob, 4, 4))
        pygame.draw.rect(surf, BLACK, (23, 13 + bob, 4, 4))

        # Sừng
        pygame.draw.rect(surf, (150, 20, 20), (8,  2 + bob, 4, 8))
        pygame.draw.rect(surf, (150, 20, 20), (22, 2 + bob, 4, 8))

        return surf

    def update(self, dt):
        self.timer += dt
        self.rect.x += self.speed * self.dir * dt

        if self.rect.left < 0:
            self.dir = 1
        if self.rect.right > WIDTH:
            self.dir = -1

        self.image = self.draw_slime(self.timer)
        if self.dir == 1:
            self.image = pygame.transform.flip(self.image, True, False)


# ── Sprite: Coin ─────────────────────────────
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.rect  = self.image.get_rect(center=(x, y))
        self.base_y = y
        self.timer  = random.uniform(0, math.pi * 2)

    def update(self, dt):
        self.timer += dt * 3
        self.rect.centery = int(self.base_y + math.sin(self.timer) * 5)

        surf = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(surf, YELLOW, (10, 10), 9)
        pygame.draw.circle(surf, (255, 240, 100), (8, 8), 5)
        pygame.draw.circle(surf, (180, 140, 0), (10, 10), 9, 2)
        self.image = surf


# ── Tạo nhóm sprite ──────────────────────────
player       = Player()
all_sprites  = pygame.sprite.Group(player)
enemy_group  = pygame.sprite.Group()
coin_group   = pygame.sprite.Group()

for ex in [350, 530, 680]:
    e = Enemy(ex)
    enemy_group.add(e)
    all_sprites.add(e)

for cx, cy in [(260, GROUND_Y-80), (430, GROUND_Y-80), (600, GROUND_Y-80)]:
    c = Coin(cx, cy)
    coin_group.add(c)
    all_sprites.add(c)

score = 0
hp    = 3
invincible_timer = 0

# ── Nền: cây và núi ──────────────────────────
def draw_background(surface, t):
    # Bầu trời gradient
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(SKY1[0] + (SKY2[0]-SKY1[0]) * ratio)
        g = int(SKY1[1] + (SKY2[1]-SKY1[1]) * ratio)
        b = int(SKY1[2] + (SKY2[2]-SKY1[2]) * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))

    # Trăng
    pygame.draw.circle(surface, (255, 255, 220), (680, 70), 40)
    pygame.draw.circle(surface, (70, 60, 110),   (695, 60), 35)

    # Sao
    random.seed(42)
    for _ in range(60):
        sx = random.randint(0, WIDTH)
        sy = random.randint(0, 200)
        br = int(180 + math.sin(t * 2 + sx) * 70)
        pygame.draw.circle(surface, (br, br, br), (sx, sy), 1)

    # Núi xa
    for i, (mx, mh, mc) in enumerate([
        (0, 200, (40,35,70)), (150,160,(40,35,70)), (320,220,(40,35,70)),
        (480,180,(40,35,70)), (620,200,(40,35,70)), (750,170,(40,35,70))
    ]):
        pts = [(mx, GROUND_Y-20), (mx+110, GROUND_Y-20), (mx+55, GROUND_Y-20-mh)]
        pygame.draw.polygon(surface, mc, pts)

    # Núi gần
    for mx, mh, mc in [
        (50,130,(55,45,90)), (230,110,(55,45,90)), (420,140,(55,45,90)),
        (590,120,(55,45,90)), (720,135,(55,45,90))
    ]:
        pts = [(mx, GROUND_Y-20), (mx+90, GROUND_Y-20), (mx+45, GROUND_Y-20-mh)]
        pygame.draw.polygon(surface, mc, pts)
        # Tuyết
        pygame.draw.polygon(surface, (200, 220, 255),
            [(mx+45, GROUND_Y-20-mh), (mx+28, GROUND_Y-20-mh+30), (mx+62, GROUND_Y-20-mh+30)])

    # Mặt đất
    pygame.draw.rect(surface, GROUND, (0, GROUND_Y, WIDTH, 20))
    pygame.draw.rect(surface, (40, 110, 35), (0, GROUND_Y, WIDTH, 6))
    pygame.draw.rect(surface, DIRT,   (0, GROUND_Y+20, WIDTH, HEIGHT - GROUND_Y - 20))

    # Cây
    for tx in [60, 180, 340, 500, 640, 760]:
        # Thân cây
        pygame.draw.rect(surface, BROWN, (tx-5, GROUND_Y-50, 10, 50))
        # Lá
        for ly, lw in [(GROUND_Y-90, 40), (GROUND_Y-120, 30), (GROUND_Y-145, 20)]:
            pygame.draw.polygon(surface, (30, 120, 40),
                [(tx, ly), (tx-lw, ly+40), (tx+lw, ly+40)])
            pygame.draw.polygon(surface, (40, 150, 50),
                [(tx, ly+5), (tx-lw+8, ly+38), (tx+lw-8, ly+38)])


# ── Hiển thị HUD ─────────────────────────────
def draw_hud(surface, score, hp):
    # Nền HUD
    pygame.draw.rect(surface, (0, 0, 0, 150), (0, 0, WIDTH, 40))

    # HP
    for i in range(3):
        color = RED if i < hp else (60, 60, 60)
        pygame.draw.circle(surface, color, (28 + i * 32, 20), 12)
        pygame.draw.circle(surface, (255, 100, 100) if i < hp else (80, 80, 80),
                           (24 + i * 32, 16), 5)

    # Score
    txt = font_small.render(f"SCORE: {score:05d}", True, YELLOW)
    surface.blit(txt, (WIDTH - 170, 10))

    # Hướng dẫn
    guide = font_small.render("← → Di chuyen   SPACE Nhay", True, (180, 180, 200))
    surface.blit(guide, (WIDTH//2 - guide.get_width()//2, HEIGHT - 28))


# ── Game Over ────────────────────────────────
def draw_game_over(surface, score):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    surface.blit(overlay, (0, 0))

    txt1 = font_big.render("GAME  OVER", True, (255, 60, 80))
    txt2 = font_small.render(f"Score cuoi: {score}", True, YELLOW)
    txt3 = font_small.render("Nhan R de choi lai", True, WHITE)

    surface.blit(txt1, txt1.get_rect(center=(WIDTH//2, HEIGHT//2 - 30)))
    surface.blit(txt2, txt2.get_rect(center=(WIDTH//2, HEIGHT//2 + 10)))
    surface.blit(txt3, txt3.get_rect(center=(WIDTH//2, HEIGHT//2 + 40)))


# ── Vòng lặp chính – Game Loop ───────────────
t = 0
game_over = False

while True:
    dt = clock.tick(FPS) / 1000.0
    t += dt

    # ── Xử lý sự kiện ────────────────────────
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                # Reset
                score, hp = 0, 3
                game_over = False
                player.rect.midbottom = (150, GROUND_Y)
                player.vel_y = 0
                for e in enemy_group:
                    e.rect.x = random.randint(200, WIDTH - 100)
                for c in coin_group:
                    c.collected = False if hasattr(c, 'collected') else False
                    coin_group.add(c)
                    all_sprites.add(c)

    if not game_over:
        # ── Cập nhật ──────────────────────────
        all_sprites.update(dt)

        invincible_timer = max(0, invincible_timer - dt)

        # Va chạm player – quái
        if invincible_timer <= 0:
            hits = pygame.sprite.spritecollide(player, enemy_group, False)
            if hits:
                hp -= 1
                invincible_timer = 1.5
                player.vel_y = -300
                if hp <= 0:
                    game_over = True

        # Nhặt coin
        collected = pygame.sprite.spritecollide(player, coin_group, True)
        for _ in collected:
            score += 100

    # ── Vẽ ────────────────────────────────────
    draw_background(screen, t)
    all_sprites.draw(screen)

    # Nhấp nháy khi bất tử
    if invincible_timer > 0 and int(t * 10) % 2 == 0:
        pass  # bỏ qua vẽ player 1 frame
    else:
        screen.blit(player.image, player.rect)

    draw_hud(screen, score, hp)

    if game_over:
        draw_game_over(screen, score)

    pygame.display.flip()