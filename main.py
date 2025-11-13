"""
Alunos: Nayara Nobre, Renato Conceição, Raphael Gomes
Jogo: Asteroides
Base: Asteroids Python Tutorial
"""

# ============================================================
# 1️⃣ IMPORTAÇÕES E CONFIGURAÇÕES INICIAIS
# ============================================================

import pygame
import math
import random

pygame.init()

# Tamanho da tela
telaL = 600
telaA = 600
janela = pygame.display.set_mode((telaL, telaA))
pygame.display.set_caption("Asteroides")

# Fonte e clock
fonte = pygame.font.SysFont("Arial", 24, True)
clock = pygame.time.Clock()

# Variáveis principais do jogo
gameover = False
vidas = 3
pontos = 0
tiroRapido = False
tempoPowerup = 0
duracaoPowerup = 5000  # 5 segundos
mostra_tela_inicial = True
isSoundOn = True

# ============================================================
# 2️⃣ CARREGAMENTO DE IMAGENS E SONS
# ============================================================

# Imagens
fundoImg = pygame.image.load("AsteroidsImages/starbg.png")
naveImg = pygame.image.load("AsteroidsImages/spaceRocket.png")
naveImg = pygame.transform.smoothscale(naveImg, (50, 50))
asteroideG = pygame.image.load("AsteroidsImages/asteroid150.png")
asteroideM = pygame.image.load("AsteroidsImages/asteroid100.png")
asteroideP = pygame.image.load("AsteroidsImages/asteroid50.png")
estrelaImg = pygame.image.load("AsteroidsImages/cogumeloMario.png")
estrelaImg = pygame.transform.scale(estrelaImg, (40, 40))

# Sons
tiro = pygame.mixer.Sound("AsteroidsSons/tiro.wav")
somDeTiroGrande = pygame.mixer.Sound("AsteroidsSons/bangLarge.wav")
somDeTiroPequeno = pygame.mixer.Sound("AsteroidsSons/bangSmall.wav")
tiro.set_volume(0.25)
somDeTiroGrande.set_volume(0.25)
somDeTiroPequeno.set_volume(0.25)

# ============================================================
# 3️⃣ CLASSES DO JOGO
# ============================================================

class Player:
    def __init__(self):
        self.img = naveImg
        self.largura = self.img.get_width()
        self.altura = self.img.get_height()
        self.x = telaL // 2
        self.y = telaA // 2
        self.angulo = 0
        self.atualizar_rotacao()

    def atualizar_rotacao(self):
        self.rotacaoSuperf = pygame.transform.rotate(self.img, self.angulo)
        self.rotacaoRetan = self.rotacaoSuperf.get_rect(center=(self.x, self.y))
        self.cosseno = math.cos(math.radians(self.angulo + 90))
        self.seno = math.sin(math.radians(self.angulo + 90))
        self.ponta = (self.x + self.cosseno * self.largura // 2, self.y - self.seno * self.altura // 2)

    def desenhar(self, janela):
        janela.blit(self.rotacaoSuperf, self.rotacaoRetan)

    def updateLocal(self):
        if self.x > telaL + 50: self.x = 0
        elif self.x < -self.largura: self.x = telaL
        if self.y > telaA + 50: self.y = 0
        elif self.y < -self.altura: self.y = telaA

    def viraEsquerda(self):
        self.angulo += 5
        self.atualizar_rotacao()

    def viraDireita(self):
        self.angulo -= 5
        self.atualizar_rotacao()

    def paraFrente(self):
        self.x += self.cosseno * 6
        self.y -= self.seno * 6
        self.updateLocal()
        self.atualizar_rotacao()

    def paraTraz(self):
        self.x -= self.cosseno * 6
        self.y += self.seno * 6
        self.updateLocal()
        self.atualizar_rotacao()


class Projetil:
    def __init__(self, player):
        self.x, self.y = player.ponta
        self.largura = 4
        self.altura = 4
        self.c = player.cosseno
        self.s = player.seno
        self.xveloc = self.c * 10
        self.yveloc = self.s * 10

    def movimento(self):
        self.x += self.xveloc
        self.y -= self.yveloc

    def desenhar(self, janela):
        pygame.draw.rect(janela, (255, 255, 255), [self.x, self.y, self.largura, self.altura])

    def foraDaTela(self):
        return self.x < -50 or self.x > telaL or self.y < -50 or self.y > telaA


class Asteroide:
    def __init__(self, categoria):
        self.categoria = categoria
        self.image = [asteroideP, asteroideM, asteroideG][categoria - 1]
        self.largura = 50 * categoria
        self.altura = 50 * categoria
        self.x, self.y = random.choice([
            (random.randrange(0, telaL - self.largura), random.choice([-self.altura - 5, telaA + 5])),
            (random.choice([-self.largura - 5, telaL + 5]), random.randrange(0, telaA - self.altura))
        ])
        self.xdirec = 1 if self.x < telaL // 2 else -1
        self.ydirec = 1 if self.y < telaA // 2 else -1
        self.xv = self.xdirec * random.randrange(1, 3)
        self.yv = self.ydirec * random.randrange(1, 3)

    def desenhar(self, janela):
        janela.blit(self.image, (self.x, self.y))


class Estrela:
    def __init__(self):
        self.img = estrelaImg
        self.largura = self.img.get_width()
        self.altura = self.img.get_height()
        self.x, self.y = random.choice([
            (random.randrange(0, telaL - self.largura), random.choice([-self.altura - 5, telaA + 5])),
            (random.choice([-self.largura - 5, telaL + 5]), random.randrange(0, telaA - self.altura))
        ])
        self.xdirec = 1 if self.x < telaL // 2 else -1
        self.ydirec = 1 if self.y < telaA // 2 else -1
        self.xv = self.xdirec * 2
        self.yv = self.ydirec * 2

    def mover(self):
        self.x += self.xv
        self.y += self.yv

    def draw(self, janela):
        janela.blit(self.img, (self.x, self.y))

# ============================================================
# 4️⃣ FUNÇÃO DE DESENHO
# ============================================================

def desenhandoTelaFinal():
    janela.blit(fundoImg, (0, 0))
    fonte_local = pygame.font.SysFont("comicsansms", 15)
    textoVidas = fonte_local.render("VIDAS: " + str(vidas), True, (255, 255, 255))
    textoPontos = fonte_local.render("PONTOS: " + str(pontos), True, (255, 255, 255))
    janela.blit(textoVidas, (25, 25))
    janela.blit(textoPontos, (475, 25))
    player.desenhar(janela)
    for a in asteroides: a.desenhar(janela)
    for b in playerBullets: b.desenhar(janela)
    for s in estrelas: s.draw(janela)

# ============================================================
# 5️⃣ LOOP PRINCIPAL
# ============================================================

player = Player()
playerBullets = []
asteroides = []
estrelas = []
conteAsteroides = 0
titulo_font = pygame.font.SysFont("comicsansms", 72, True)
botao_font = pygame.font.SysFont("Arial", 36, True)
botao_rect = pygame.Rect(telaL // 2 - 100, telaA // 2 + 80, 200, 60)

running = True
while running:
    clock.tick(60)
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Tela inicial
    if mostra_tela_inicial:
        janela.blit(fundoImg, (0, 0))
        titulo_surf = titulo_font.render("ASTEROIDS", True, (255, 255, 255))
        titulo_rect = titulo_surf.get_rect(center=(telaL // 2, 160))
        janela.blit(titulo_surf, titulo_rect)
        pygame.draw.rect(janela, (255, 255, 255), botao_rect, border_radius=12)
        jogar_surf = botao_font.render("JOGAR", True, (0, 0, 0))
        jogar_rect = jogar_surf.get_rect(center=botao_rect.center)
        janela.blit(jogar_surf, jogar_rect)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and botao_rect.collidepoint(event.pos):
                mostra_tela_inicial = False
                vidas = 3
                pontos = 0
                tiroRapido = False
                tempoPowerup = 0
                player = Player()
                playerBullets = []
                asteroides = []
                estrelas = []
                conteAsteroides = 0
        pygame.display.update()
        continue

    # ===================== LÓGICA DO JOGO =====================
    conteAsteroides += 1

    if not gameover:
        if conteAsteroides % 50 == 0:
            asteroides.append(Asteroide(random.choice([1, 1, 2, 3])))
        if conteAsteroides % 1000 == 0:
            estrelas.append(Estrela())

        player.updateLocal()
        for b in playerBullets[:]:
            b.movimento()
            if b.foraDaTela():
                playerBullets.remove(b)

        for a in asteroides[:]:
            a.x += a.xv
            a.y += a.yv
            # colisão com player
            if (a.x < player.x + player.largura and a.x + a.largura > player.x and
                a.y < player.y + player.altura and a.y + a.altura > player.y):
                vidas -= 1
                asteroides.remove(a)
                if vidas <= 0:
                    gameover = True
                break

            # colisão com tiro
            for b in playerBullets[:]:
                if (b.x < a.x + a.largura and b.x + b.largura > a.x and
                    b.y < a.y + a.altura and b.y + b.altura > a.y):
                    if a.categoria > 1:
                        pontos += 10 * a.categoria
                        novo = Asteroide(a.categoria - 1)
                        novo.x, novo.y = a.x, a.y
                        asteroides.append(novo)
                    else:
                        pontos += 30
                    if isSoundOn:
                        (somDeTiroGrande if a.categoria > 2 else somDeTiroPequeno).play()
                    asteroides.remove(a)
                    playerBullets.remove(b)
                    break

        # Power-up
        for s in estrelas[:]:
            s.mover()
            if s.x < -100 or s.x > telaL or s.y < -100 or s.y > telaA:
                estrelas.remove(s)
                continue
            if (player.x < s.x + s.largura and player.x + player.largura > s.x and
                player.y < s.y + s.altura and player.y + player.altura > s.y):
                tiroRapido = True
                tempoPowerup = pygame.time.get_ticks()
                estrelas.remove(s)

        # Controle de teclas
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]: player.viraEsquerda()
        if teclas[pygame.K_RIGHT]: player.viraDireita()
        if teclas[pygame.K_UP]: player.paraFrente()
        if teclas[pygame.K_DOWN]: player.paraTraz()
        if teclas[pygame.K_SPACE]:
            if tiroRapido or conteAsteroides % 10 == 0:
                playerBullets.append(Projetil(player))
                if isSoundOn: tiro.play()

    # eventos extras
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                isSoundOn = not isSoundOn
            if event.key == pygame.K_SPACE and gameover:
                gameover = False
                vidas = 3
                pontos = 0
                asteroides.clear()

    if tiroRapido and pygame.time.get_ticks() - tempoPowerup >= duracaoPowerup:
        tiroRapido = False

    # Desenho
    desenhandoTelaFinal()
    if tiroRapido:
        tempo_restante = max(0, (duracaoPowerup - (pygame.time.get_ticks() - tempoPowerup)) // 1000)
        texto_powerup = fonte.render(f"Tiro rápido: {tempo_restante}s", True, (255, 255, 0))
        janela.blit(texto_powerup, (20, 60))
    pygame.display.update()

pygame.quit()