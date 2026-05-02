import pygame
import sys
import random
import math

WIDTH, HEIGHT = 800, 600
TITLE = "Slice Edge: Boss Protocol"
FPS = 60
DEFAULT_HP = 50
MAX_WAVE_TARGETS = 12
QUIZ_HEAL_AMOUNT = 5 

WHITE      = (255, 255, 255)
BG_GRAY    = (230, 230, 235)
BLACK      = (20, 20, 25)
RED        = (220, 20, 60)
GREEN      = (34, 139, 34)
LIME_GREEN = (50, 255, 50) 
ORANGE     = (255, 140, 0)
YELLOW     = (255, 215, 0)
UI_ACCENT  = (70, 130, 180)

class FloatingText(pygame.sprite.Sprite):
    def __init__(self, text, pos, color, font):
        super().__init__()
        base_text = font.render(text, True, color)
        shadow_text = font.render(text, True, BLACK)
        
        self.image = pygame.Surface((base_text.get_width() + 4, base_text.get_height() + 4), pygame.SRCALPHA)
        self.image.blit(shadow_text, (4, 4))
        self.image.blit(base_text, (0, 0))
        
        self.rect = self.image.get_rect(center=pos)
        self.vel_y = -3
        self.life = 45 

    def update(self):
        self.rect.y += self.vel_y
        self.life -= 1
        if self.life <= 0:
            self.kill()

class Particle(pygame.sprite.Sprite):
    image_cache = None

    def __init__(self, pos):
        super().__init__()
        if Particle.image_cache is None:
            try:
                Particle.image_cache = pygame.image.load("python_logo.png").convert_alpha()
                Particle.image_cache = pygame.transform.smoothscale(Particle.image_cache, (40, 40))
            except:
                Particle.image_cache = pygame.Surface((40, 40), pygame.SRCALPHA)
                pygame.draw.circle(Particle.image_cache, GREEN, (20, 20), 20)
        
        self.image = Particle.image_cache
        self.rect = self.image.get_rect(center=pos)
        
        self.vel_x = random.uniform(-10, 10)
        self.vel_y = random.uniform(-15, 5)
        self.gravity = 0.5
        self.life = random.randint(40, 80) 

    def update(self):
        self.vel_y += self.gravity
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.life -= 1
        
        if self.life <= 0 or self.rect.top > HEIGHT:
            self.kill()

class Target(pygame.sprite.Sprite):
    javier_surface = None
    quiz_surface = None

    def __init__(self, size=50, hp=None, color=None, can_split=True, pos=None, gravity=0.45):
        super().__init__()
        self.can_split = can_split
        self.is_javier = False
        self.is_quiz = False
        self.barrier_hp = 0
        self.gravity = gravity
        
        if pos:
            self.rect = pygame.Rect(pos[0], pos[1], size, size)
        else:
            self.rect = pygame.Rect(random.randint(100, WIDTH - 100), HEIGHT, size, size)

        if hp is not None and color is not None:
            self.hp = hp
            self.color = color
            self._create_image(size, color)
        else:
            r = random.random()
            if r < 0.04: 
                self.setup_smug_javier()
            elif r < 0.09: 
                self.setup_quiz()
            elif r < 0.17: 
                self.setup_standard(YELLOW, 2, 80)
            elif r < 0.27:
                self.setup_standard(ORANGE, 3, 60)
            else:
                self.setup_standard(GREEN, 1, 55)

        if not pos: 
            self.vel_y = -math.sqrt(2 * self.gravity * (HEIGHT * 0.75)) + random.uniform(-1, 1)
            self.vel_x = random.randint(-2, 2)
        else:
            self.vel_y = 0
            self.vel_x = 0

    def _create_image(self, size, color):
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.rect(self.image, color, (0, 0, size, size), border_radius=8)

    def setup_standard(self, color, hp, size):
        self.color = color
        self.hp = hp
        self._create_image(size, color)
        self.rect = self.image.get_rect(center=self.rect.center)

    def setup_smug_javier(self):
        self.is_javier = True
        self.hp = 1
        self.barrier_hp = 15
        self.color = YELLOW
        size = 100
        
        if Target.javier_surface is None:
            try:
                Target.javier_surface = pygame.image.load("smug_javier.png").convert_alpha()
                Target.javier_surface = pygame.transform.smoothscale(Target.javier_surface, (size, size))
            except:
                self.setup_standard(ORANGE, 1, size)
                return

        self.image = Target.javier_surface
        self.rect = self.image.get_rect(center=self.rect.center)
        
        b_size = int(size * 1.3)
        self.barrier_surf = pygame.Surface((b_size, b_size), pygame.SRCALPHA)
        pygame.draw.circle(self.barrier_surf, (0, 150, 255, 80), (b_size//2, b_size//2), b_size//2)
        pygame.draw.circle(self.barrier_surf, (0, 200, 255, 150), (b_size//2, b_size//2), b_size//2, 3)

    def setup_quiz(self):
        self.is_quiz = True
        self.hp = 1
        self.color = WHITE
        self.can_split = False
        size = 120 
        
        if Target.quiz_surface is None:
            try:
                Target.quiz_surface = pygame.image.load("quiz.png").convert_alpha()
                Target.quiz_surface = pygame.transform.smoothscale(Target.quiz_surface, (size, size))
            except:
                Target.quiz_surface = pygame.Surface((size, size), pygame.SRCALPHA)
                pygame.draw.rect(Target.quiz_surface, WHITE, (0, 0, size, size), border_radius=4)
                pygame.draw.line(Target.quiz_surface, BLACK, (20, 30), (100, 30), 4)
                pygame.draw.line(Target.quiz_surface, BLACK, (20, 60), (100, 60), 4)
                pygame.draw.line(Target.quiz_surface, BLACK, (20, 90), (80, 90), 4)

        self.image = Target.quiz_surface
        self.rect = self.image.get_rect(center=self.rect.center)
        self.gravity = 0.20 

    def take_damage(self):
        if self.is_javier and self.barrier_hp > 0:
            self.barrier_hp -= 1
            return False
        self.hp -= 1
        return self.hp <= 0

    def update(self):
        self.vel_y += self.gravity
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        return "miss" if self.rect.top > HEIGHT else None

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = 200
        try:
            self.image = pygame.image.load("sad_javier.png").convert_alpha()
            self.image = pygame.transform.smoothscale(self.image, (self.size, self.size))
        except:
            self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.circle(self.image, RED, (self.size//2, self.size//2), self.size//2)
            
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 5))
        self.max_hp = 60
        self.hp = self.max_hp
        self.vel_x = 3.5
        self.spawn_timer = 0.4
        self.shake_frames = 0 

    def update(self, dt):
        self.rect.x += self.vel_x
        
        if self.rect.left < 0 and self.vel_x < 0:
            self.vel_x *= -1
        elif self.rect.right > WIDTH and self.vel_x > 0:
            self.vel_x *= -1
            
        if self.shake_frames > 0:
            self.shake_frames -= 1
        
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self.spawn_timer = random.uniform(0.25, 0.5)
            return self.spawn_mini_rain()
        return None

    def spawn_mini_rain(self):
        mini_size = 75 
        mini = Target(size=mini_size, hp=1, color=WHITE, can_split=False, pos=self.rect.center)
        mini.is_javier = True
        mini.vel_y = random.uniform(5, 9)
        mini.vel_x = random.uniform(-4, 4)
        if Target.javier_surface:
            mini.image = pygame.transform.smoothscale(Target.javier_surface, (mini_size, mini_size))
        return mini

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        
        self.title_font = pygame.font.SysFont("Impact", 72)
        self.main_font = pygame.font.SysFont("Arial", 28, bold=True)
        self.ui_font = pygame.font.SysFont("Verdana", 18, bold=True)
        self.victory_font = pygame.font.SysFont("Impact", 64)

        self.targets = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.floating_texts = pygame.sprite.Group()
        self.slice_points = []
        self.reset_game()

    def reset_game(self):
        self.state = 'menu'
        self.score = 0
        self.player_hp = DEFAULT_HP
        self.wave = 1
        self.smug_slain_counter = 0 
        self.boss = None
        self.targets.empty()
        self.particles.empty()
        self.floating_texts.empty()
        self.spawn_remaining = 0
        self.spawn_timer = 0
        self.victory_text_timer = 0
        self.warning_text_timer = 0

    def handle_slicing(self):
        if len(self.slice_points) < 2: return
        p1, p2 = self.slice_points[-2], self.slice_points[-1]
        
        for target in self.targets:
            if target.rect.clipline(p1, p2):
                if target.take_damage():
                    self.on_target_death(target)
                    target.kill()

        if self.boss and self.boss.rect.clipline(p1, p2):
            self.boss.hp -= 1
            self.boss.shake_frames = 8 
            if self.boss.hp <= 0:
                for _ in range(25):
                    self.particles.add(Particle(self.boss.rect.center))
                
                self.boss = None
                self.score += 500
                self.smug_slain_counter = 0 
                self.victory_text_timer = 180 

    def on_target_death(self, target):
        if target.is_quiz:
            self.player_hp = min(DEFAULT_HP, self.player_hp + QUIZ_HEAL_AMOUNT)
            self.floating_texts.add(FloatingText("A+", target.rect.center, LIME_GREEN, self.victory_font))
            self.score += 25
            return 
            
        self.score += 10
        
        if target.is_javier and target.can_split:
            self.smug_slain_counter += 1
                
            if self.smug_slain_counter >= 3 and not self.boss:
                if random.random() < 0.6:
                    self.boss = Boss()
                    self.warning_text_timer = 180
        
        if target.color == YELLOW and target.can_split and not target.is_javier:
            num_splinters = random.randint(5, 8) 
            for _ in range(num_splinters):
                angle = random.uniform(0, 2 * math.pi)
                dist = target.rect.width // 2
                spawn_x = target.rect.centerx + math.cos(angle) * dist
                spawn_y = target.rect.centery + math.sin(angle) * dist
                
                mini = Target(size=45, hp=1, color=YELLOW, can_split=False, pos=(spawn_x, spawn_y))
                mini.vel_y = random.uniform(-6, -12)
                mini.vel_x = random.uniform(-7, 7)
                self.targets.add(mini)

    def update(self):
        dt = self.clock.get_time() / 1000.0
        if self.state != 'playing': return

        if self.victory_text_timer > 0:
            self.victory_text_timer -= 1
            
        if self.warning_text_timer > 0:
            self.warning_text_timer -= 1

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if not self.slice_points or pos != self.slice_points[-1]:
                self.slice_points.append(pos)
            if len(self.slice_points) > 12: self.slice_points.pop(0)
            self.handle_slicing()
        else:
            self.slice_points.clear()

        for t in self.targets:
            if t.update() == "miss":
                if not t.is_quiz:
                    self.player_hp -= 1
                t.kill()
                
        self.particles.update()
        self.floating_texts.update()

        if self.spawn_remaining > 0:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                self.targets.add(Target())
                self.spawn_remaining -= 1
                self.spawn_timer = random.uniform(0.4, 0.9)
        
        if not self.targets and not self.boss and self.spawn_remaining <= 0:
            self.wave += 1
            self.spawn_remaining = min(self.wave * 2, MAX_WAVE_TARGETS)

        if self.boss:
            new_mini = self.boss.update(dt)
            if new_mini: self.targets.add(new_mini)

        if self.player_hp <= 0: self.state = 'menu'

    def draw_menu(self):
        self.screen.fill(BG_GRAY)
        pygame.draw.rect(self.screen, WHITE, (50, 50, WIDTH-100, HEIGHT-100), border_radius=20)
        
        title_surf = self.title_font.render("SLICE EDGE", True, BLACK)
        self.screen.blit(title_surf, title_surf.get_rect(center=(WIDTH//2, HEIGHT//3)))
        
        prompt_surf = self.main_font.render("PRESS ENTER TO START", True, UI_ACCENT)
        self.screen.blit(prompt_surf, prompt_surf.get_rect(center=(WIDTH//2, HEIGHT//2 + 50)))
        
        hint_surf = self.ui_font.render("Slice Smug Javiers to lure the Boss", True, (100, 100, 100))
        self.screen.blit(hint_surf, hint_surf.get_rect(center=(WIDTH//2, HEIGHT - 100)))

    def draw(self):
        if self.state == 'menu':
            self.draw_menu()
        else:
            self.screen.fill(BG_GRAY)
            
            self.particles.draw(self.screen)
            
            if self.boss:
                shake_x, shake_y = 0, 0
                if self.boss.shake_frames > 0:
                    shake_x = random.randint(-6, 6)
                    shake_y = random.randint(-6, 6)

                boss_draw_pos = (self.boss.rect.x + shake_x, self.boss.rect.y + shake_y)
                self.screen.blit(self.boss.image, boss_draw_pos)
                
                bar_width = 150
                bar_height = 14
                bar_x = self.boss.rect.centerx - (bar_width // 2) + shake_x
                bar_y = self.boss.rect.top - 25 + shake_y
                
                pygame.draw.rect(self.screen, BLACK, (bar_x - 3, bar_y - 3, bar_width + 6, bar_height + 6))
                pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
                
                if self.boss.hp > 0:
                    fill_width = int((self.boss.hp / self.boss.max_hp) * bar_width)
                    pygame.draw.rect(self.screen, RED, (bar_x, bar_y, fill_width, bar_height))
                    pygame.draw.rect(self.screen, (255, 100, 100), (bar_x, bar_y, fill_width, bar_height // 3))

            for t in self.targets:
                self.screen.blit(t.image, t.rect)
                if t.is_javier and t.barrier_hp > 0:
                    b_rect = t.barrier_surf.get_rect(center=t.rect.center)
                    self.screen.blit(t.barrier_surf, b_rect)
                
                hp_val = t.barrier_hp if t.is_javier and t.barrier_hp > 0 else t.hp
                if hp_val > 0:
                    txt = self.ui_font.render(str(hp_val), True, BLACK)
                    self.screen.blit(txt, txt.get_rect(center=(t.rect.centerx, t.rect.top - 15)))

            if len(self.slice_points) > 1:
                pygame.draw.lines(self.screen, BLACK, False, self.slice_points, 5)

            self.floating_texts.draw(self.screen)

            self.draw_hud_text(f"SCORE: {self.score}", 20, 20)
            self.draw_hud_text(f"HP: {self.player_hp}", 20, 50, RED)
            self.draw_hud_text(f"WAVE: {self.wave}", WIDTH - 20, 20, GREEN, align="right")
            self.draw_hud_text(f"STREAK: {self.smug_slain_counter}/3", WIDTH - 20, 50, UI_ACCENT, align="right")

            if self.warning_text_timer > 0:
                shadow = self.victory_font.render("Eminent: Javier Incoming!", True, BLACK)
                text = self.victory_font.render("Eminent: Javier Incoming!", True, RED)
                self.screen.blit(shadow, shadow.get_rect(center=(WIDTH//2 + 4, HEIGHT//2 + 4)))
                self.screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2)))

            if self.victory_text_timer > 0:
                shadow = self.victory_font.render("10+ Sa Programming!", True, BLACK)
                text = self.victory_font.render("10+ Sa Programming!", True, ORANGE)
                self.screen.blit(shadow, shadow.get_rect(center=(WIDTH//2 + 4, HEIGHT//2 + 4)))
                self.screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2)))

        pygame.display.flip()

    def draw_hud_text(self, text, x, y, color=BLACK, align="left"):
        surf = self.main_font.render(text, True, color)
        if align == "right":
            rect = surf.get_rect(topright=(x, y))
        else:
            rect = surf.get_rect(topleft=(x, y))
        self.screen.blit(surf, rect)

    def run(self):
        while True:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.state == 'menu':
                        self.reset_game()
                        self.state = 'playing'
                        self.spawn_remaining = 5

            self.update()
            self.draw()

if __name__ == "__main__":
    Game().run()