"""
Jogo: Asteroides
Tutorial base: Asteroids Python Tutorial - https://www.youtube.com/watch?v=XKMjMGbdrpY&t=1s
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

# Fonte padrão
fonte = pygame.font.SysFont("Arial", 24, True)

# Clock para controlar FPS
clock = pygame.time.Clock()

# Variáveis principais do jogo
gameover = False
vidas = 3
pontos = 0
tiroRapido = False
tempoPowerup = 0
duracaoPowerup = 5000  # tempo do power-up em ms (5s)

# Controle da tela inicial
mostra_tela_inicial = True

# ============================================================
# 2️⃣ CARREGAMENTO DE IMAGENS
# ============================================================
fundoImg = pygame.image.load("AsteroidsImages/starbg.png")

naveImg = pygame.image.load("AsteroidsImages/spaceRocket.png")
naveImg = pygame.transform.smoothscale(naveImg, (50, 50))

asteroideG = pygame.image.load("AsteroidsImages/asteroid150.png")
asteroideM = pygame.image.load("AsteroidsImages/asteroid100.png")
asteroideP = pygame.image.load("AsteroidsImages/asteroid50.png")

estrelaImg = pygame.image.load("AsteroidsImages/cogumeloMario.png")
estrelaImg = pygame.transform.scale(estrelaImg, (40, 40))

# ============================================================
# 3️⃣ CLASSES DO JOGO
# ============================================================
class Player(object):
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
        self.rotacaoRetan = self.rotacaoSuperf.get_rect()
        self.rotacaoRetan.center = (self.x, self.y)
        self.cosseno = math.cos(math.radians(self.angulo + 90))
        self.seno = math.sin(math.radians(self.angulo + 90))
        self.ponta = (self.x + self.cosseno * self.largura // 2, self.y - self.seno * self.altura // 2)

    def desenhar(self, janela):
        janela.blit(self.rotacaoSuperf, self.rotacaoRetan)

    def updateLocal(self):
<<<<<<< HEAD
        if self.x > telaL + 50: # A nave passou 50px além da borda direita da tela.
            self.x = 0 # Move a nave para o início do eixo X
        elif self.x < 0: # A nave passou além da borda esquerda.
            self.x = telaL # Move a nave para o final da tela
        elif self.y < 0:
            self.y = telaA
        elif self.y > telaA + 50:
            self.y = 0
    
    def viraEsquerda (self):
=======
        if self.x > telaL + 50: self.x = 0
        elif self.x < -self.largura: self.x = telaL
        elif self.y < 0: self.y = telaA
        elif self.y > telaA + 50: self.y = 0

    def viraEsquerda(self):
>>>>>>> afa6e8142b4fa503cd0f1a13ceabfec0c99e40ba
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


class Projetil(object):
    def __init__(self):
        self.mira = player.ponta
        self.x, self.y = self.mira
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

<<<<<<< HEAD
    # excluir os projeteis que sairam da tela
    def foraDaTela (self):
        if self.x < -50 or self.x > telaL or self.y < -50 or self.y > telaA:
            return True
=======
    def foraDaTela(self):
        return self.x < -50 or self.x > telaL or self.y < -50 or self.y > telaA

>>>>>>> afa6e8142b4fa503cd0f1a13ceabfec0c99e40ba

class Asteroide(object):
    def __init__(self, categoria):
        self.categoria = categoria
        self.image = [asteroideP, asteroideM, asteroideG][categoria - 1]
        self.largura = 50 * categoria
        self.altura = 50 * categoria
        # protege randrange caso imagem maior
        max_x = max(1, telaL - self.largura)
        max_y = max(1, telaA - self.altura)
        self.x, self.y = random.choice([
            (random.randrange(0, max_x), random.choice([-self.altura - 5, telaA + 5])),
            (random.choice([-self.largura - 5, telaL + 5]), random.randrange(0, max_y))
        ])
        self.xdirec = 1 if self.x < telaL // 2 else -1
        self.ydirec = 1 if self.y < telaA // 2 else -1
        self.xv = self.xdirec * random.randrange(1, 3)
        self.yv = self.ydirec * random.randrange(1, 3)

    def desenhar(self, janela):
        janela.blit(self.image, (self.x, self.y))


<<<<<<< HEAD
# desenhando imagens na tela
def desenhandoTelaFinal (): 
    janela.blit(fundoImg, (0,0)) # colocando imagem de fundo

    # criando texto
    fonte = pygame.font.SysFont("comicsansms", 15) 
    textoVidas = fonte.render("VIDAS: " + str(vidas), 1, (255,255,255))
    textoJogarDeNovo = fonte.render("Pressione ESPAÇO para jogar novamente", 1, (255,255,255))

    textoPontos = fonte.render("PONTOS: " + str(pontos), 2, (255,255,255))

    player.desenhar(janela) # colocando imagem da nave do player em cima da imagem de fundo
    
    for a in asteroides:
        a.desenhar(janela)

    for b in playerBullets:
        b.desenhar(janela)
=======
class Estrela(object):
    def __init__(self):
        self.img = estrelaImg
        self.largura = self.img.get_width()
        self.altura = self.img.get_height()
        max_x = max(1, telaL - self.largura)
        max_y = max(1, telaA - self.altura)
        self.x, self.y = random.choice([
            (random.randrange(0, max_x), random.choice([-self.altura - 5, telaA + 5])),
            (random.choice([-self.largura - 5, telaL + 5]), random.randrange(0, max_y))
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
    textoJogarDeNovo = fonte_local.render("Pressione ESPAÇO para jogar novamente", True, (255, 255, 255))

    player.desenhar(janela)
    for a in asteroides: a.desenhar(janela)
    for b in playerBullets: b.desenhar(janela)
    for s in estrelas: s.draw(janela)
>>>>>>> afa6e8142b4fa503cd0f1a13ceabfec0c99e40ba

    if gameover:
        janela.blit(textoJogarDeNovo, (telaL // 2 - textoJogarDeNovo.get_width() // 2, telaA // 2 - textoJogarDeNovo.get_height() // 2))

    janela.blit(textoVidas, (25, 25))
    janela.blit(textoPontos, (475, 25))


# ============================================================
# 5️⃣ LOOP PRINCIPAL (corrigido: usa events = pygame.event.get() UMA vez)
# ============================================================
player = Player()
playerBullets = []
asteroides = []
estrelas = [Estrela()]
conteAsteroides = 0

# precompute fonts/visuals da tela inicial
titulo_font = pygame.font.SysFont("comicsansms", 72, True)
botao_font = pygame.font.SysFont("Arial", 36, True)
botao_cor = (255, 255, 255)
botao_text_cor = (0, 0, 0)
botao_rect = pygame.Rect(telaL // 2 - 100, telaA // 2 + 80, 200, 60)

running = True
while running:
    clock.tick(60)
    events = pygame.event.get()  # pega todos os eventos UMA vez por frame

    # processa eventos globais (fechar janela)
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # ------------------------------------------------------------
    # 🎬 TELA INICIAL
    # ------------------------------------------------------------
    if mostra_tela_inicial:
        janela.blit(fundoImg, (0, 0))
        titulo_surf = titulo_font.render("ASTEROIDS", True, (255, 255, 255))
        titulo_rect = titulo_surf.get_rect(center=(telaL // 2, 160))
        pygame.draw.rect(janela, (0, 0, 0, 120), (0, 0, telaL, telaA))  # leve overlay (opcional)
        janela.blit(titulo_surf, titulo_rect)

        # desenha botão
        pygame.draw.rect(janela, botao_cor, botao_rect, border_radius=12)
        jogar_surf = botao_font.render("JOGAR", True, botao_text_cor)
        jogar_rect = jogar_surf.get_rect(center=botao_rect.center)
        janela.blit(jogar_surf, jogar_rect)

        # checa clique no botão (usa a mesma lista events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and botao_rect.collidepoint(event.pos):
                mostra_tela_inicial = False
                # resetar contadores/estado do jogo ao iniciar (opcional)
                gameover = False
                vidas = 3
                pontos = 0
                tiroRapido = False
                tempoPowerup = 0
                player = Player()
                playerBullets = []
                asteroides = []
                estrelas = [Estrela()]
                conteAsteroides = 0
        pygame.display.update()
        continue  # volta ao while; não executa a lógica do jogo enquanto estiver na tela inicial

    # ------------------------------------------------------------
    # 🎮 LÓGICA DO JOGO (após tela inicial)
    # ------------------------------------------------------------
    conteAsteroides += 1

    if not gameover:
        # Spawn de asteroides e power-ups
        if conteAsteroides % 50 == 0:
            asteroides.append(Asteroide(random.choice([1, 1, 1, 2, 2, 3])))
        if conteAsteroides % 1000 == 0:
            estrelas.append(Estrela())

        # Movimentos e colisões
        player.updateLocal()

        for b in playerBullets[:]:
            b.movimento()
            if b.foraDaTela():
                playerBullets.remove(b)

        for a in asteroides[:]:
            a.x += a.xv
            a.y += a.yv

            # colisões player x asteroide (AABB)
            if a.x < player.x + player.largura and a.x + a.largura > player.x and a.y < player.y + player.altura and a.y + a.altura > player.y:
                vidas -= 1
                if a in asteroides: asteroides.remove(a)
                break

            # colisão projétil x asteroide
            for b in playerBullets[:]:
                if b.x < a.x + a.largura and b.x + b.largura > a.x and b.y < a.y + a.altura and b.y + b.altura > a.y:
                    if a.categoria > 1:
                        pontos += 10 * a.categoria
                        novo = Asteroide(a.categoria - 1)
                        novo.x, novo.y = a.x, a.y
                        asteroides.append(novo)
                    else:
                        pontos += 30
                    if a in asteroides: asteroides.remove(a)
                    if b in playerBullets: playerBullets.remove(b)
                    break

        # power-up
        for s in estrelas[:]:
            s.mover()
            if s.x < -100 or s.x > telaL or s.y < -100 or s.y > telaA:
                if s in estrelas: estrelas.remove(s)
                continue
            for b in playerBullets[:]:
                if b.x < s.x + s.largura and b.x + b.largura > s.x and b.y < s.y + s.altura and b.y + b.altura > s.y:
                    tiroRapido = True
                    tempoPowerup = pygame.time.get_ticks()
                    if s in estrelas: estrelas.remove(s)
                    if b in playerBullets: playerBullets.remove(b)
                    break

        if vidas <= 0:
            gameover = True

        # Movimentação com teclas
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]: player.viraEsquerda()
        if teclas[pygame.K_RIGHT]: player.viraDireita()
        if teclas[pygame.K_UP]: player.paraFrente()
        if teclas[pygame.K_DOWN]: player.paraTraz()
        if teclas[pygame.K_SPACE] and tiroRapido:
            playerBullets.append(Projetil())

    # eventos (usando a lista events)
    for event in events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not gameover:
                if not tiroRapido:
                    playerBullets.append(Projetil())
            else:
                gameover = False
                vidas, pontos = 3, 0
                asteroides.clear()

    # duração do power-up
    if tiroRapido and pygame.time.get_ticks() - tempoPowerup >= duracaoPowerup:
        tiroRapido = False

    # desenho
    desenhandoTelaFinal()
    if tiroRapido:
        tempo_restante = max(0, (duracaoPowerup - (pygame.time.get_ticks() - tempoPowerup)) // 1000)
        texto_powerup = fonte.render(f"Tiro rápido: {tempo_restante}s", True, (255, 255, 0))
        janela.blit(texto_powerup, (20, 60))

    pygame.display.update()

pygame.quit()
