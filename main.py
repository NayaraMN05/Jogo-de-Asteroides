"""
Jogo: Asteroides
Tutorial: Asteroids Python Tutorial - https://www.youtube.com/watch?v=XKMjMGbdrpY&t=1s
"""

import pygame
import math
import random


# inicializando pygame
pygame.init()

# definindo tamanho e criando tela para o jogo
telaL = 600
telaA = 600
janela = pygame.display.set_mode((telaL, telaA)) 

# definindo nome da aba do jogo
pygame.display.set_caption("Asteroides")

# definindo imagens -> acessando pasta/pegando imagem
fundoImg = pygame.image.load("AsteroidsImages/starbg.png") # de fundo de tela
naveImg = pygame.image.load("AsteroidsImages/spaceRocket.png") # nossa nave
naveImg = pygame.transform.smoothscale(naveImg, (50, 50)) # img original muito grande, diminuindo escala

asteroideG = pygame.image.load("AsteroidsImages/asteroid150.png")
asteroideM = pygame.image.load("AsteroidsImages/asteroid100.png")
asteroideP = pygame.image.load("AsteroidsImages/asteroid50.png")


# fazer com o que o jogo rode seguindo a CPU
clock = pygame.time.Clock()

gameover = False
vidas = 3
pontos = 0

# padrões para o jogador
class Player(object):
    
    def __init__(self):
        #definindo imagem e tamanho padrão para o player
        self.img = naveImg
        self.largura = self.img.get_width()
        self.altura = self.img.get_height()

        # definindo posição padrão na tela (posições x e y)
        self.x = telaL//2
        self.y = telaA//2

        # angulos que a nave do player está voltada
        self.angulo = 0
        self.rotacaoSuperf = pygame.transform.rotate(self.img, self.angulo)
        self.rotacaoRetan = self.rotacaoSuperf.get_rect()
        self.rotacaoRetan.center = (self.x, self.y) # quando rotacionar, rotação no eixo central da nave
        self.cosseno = math.cos(math.radians(self.angulo + 90))
        self.seno = math.sin(math.radians(self.angulo + 90)) 
        self.ponta = (self.x + self.cosseno * self.largura//2, self.y - self.seno * self.altura//2) # qual é a frente da nave

    # desenho padrão de posições na tela
    def desenhar(self, janela):
        janela.blit(self.rotacaoSuperf, self.rotacaoRetan)

    def virando(self): 
        self.rotacaoSuperf = pygame.transform.rotate(self.img, self.angulo)
        self.rotacaoRetan = self.rotacaoSuperf.get_rect()
        self.rotacaoRetan.center = (self.x, self.y)
        self.cosseno = math.cos(math.radians(self.angulo + 90))
        self.seno = math.sin(math.radians(self.angulo + 90))
        self.ponta = (self.x + self.cosseno * self.largura//2, self.y - self.seno * self.altura//2)

    def updateLocal(self):
        if self.x > telaL + 50: # A nave passou 50px além da borda direita da tela.
            self.x = 0 # Move a nave para o início do eixo X
        elif self.x < 0 - self.largura: # A nave passou além da borda esquerda.
            self.x = telaL # Move a nave para o final da tela
        elif self.y < 0:
            self.y = telaA
        elif self.y > telaA + 50:
            self.y = 0
    
    def viraEsquerda (self):
        self.angulo += 5
        self.virando()
        self.updateLocal()

    def viraDireita (self):
        self.angulo -= 5
        self.virando()
        self.updateLocal()

    def paraFrente (self):
        self.x += self.cosseno * 6
        self.y -= self.seno * 6
        self.virando()
        self.updateLocal()
    
    def paraTraz(self):
        self.x -= self.cosseno * 6
        self.y += self.seno * 6
        self.virando()
        self.updateLocal()


# padrões para o projétil
class Projetil(object):
    def __init__(self):
        # da onde o tiro sai
        self.mira = player.ponta
        self.x, self.y = self.mira
        self.largura = 4
        self.altura = 4

        # qual o percurso do tiro
        self.c = player.cosseno
        self.s = player.seno

        # velocidade de cada tiro
        self.xveloc =  self.c * 10
        self.yveloc = self.s * 10

    def movimento(self):
        self.x += self.xveloc
        self.y -= self.yveloc
    
    def desenhar(self, janela):
        pygame.draw.rect(janela, (255, 255, 255), [self.x, self.y, self.largura, self.altura])

    # excluir os projetil que saui da tela
    def foraDaTela (self):
        if self.x < -50 or self.x > telaL or self.y < -50 or self.y > telaA:
            return True

class Asteroide(object):
    def __init__(self, categoria):
        self.categoria = categoria
        if self.categoria == 1:
            self.image = asteroideP
        elif self.categoria == 2:
            self.image = asteroideM
        else:
            self.image = asteroideG

        # definindo tamanho do asteroide
        self.largura = 50 * categoria
        self.altura = 50 * categoria

        # local aleatório pelo qual o asteroid vai surgir
        self.localAst = random.choice([
            # Aparece acima ou abaixo da tela
            (random.randrange(0, telaL - self.largura), random.choice([-1 * self.altura - 5, telaA + 5])),
            # Aparece à esquerda ou à direita da tela
            (random.choice([-1 * self.largura - 5, telaL + 5]), random.randrange(0, telaA - self.altura))
            ])
        self.x, self.y = self.localAst

        # que direção vai seguir
        if self.x < telaL//2:
            self.xdirec = 1
        else:
            self.xdirec = -1
        
        if self.y < telaA//2:
            self.ydirec = 1
        else:
            self.ydirec = -1
        
        # velocidade do asteroide
        self.xv = self.xdirec * random.randrange(1,3)
        self.yv = self.ydirec * random.randrange(1,3)

    
    def desenhar(self, janela):
        # asteroide do tamanho da tela
        janela.blit(self.image, (self.x, self.y))




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

    if gameover:
        janela.blit(textoJogarDeNovo, (telaL//2 - textoJogarDeNovo.get_width()//2, telaA//2 - textoJogarDeNovo.get_height()//2))

    janela.blit(textoVidas, (25,25)) # colocando texto de vidas na tela
    janela.blit(textoPontos, (475,25)) # colocando texto de pontos na tela
    pygame.display.update() # a ordem dos fatores altera o resultado! Tem que deixar esse no final!


player = Player()
playerBullets = []
asteroides = []
conteAsteroides = 0

running = True
while running:
    clock.tick(60) # padrão para não sobrecarregar CPU
    conteAsteroides += 1

    if not gameover:

        if conteAsteroides % 50 == 0:
            ran = random.choice([1,1,1,2,2,3])
            asteroides.append(Asteroide(ran))

        player.updateLocal()

        for b in playerBullets:
            b.movimento()
            # se as balas forem alem da tela, excluir elas:
            if b.foraDaTela():
                playerBullets.pop(playerBullets.index(b))

        for a in asteroides:
            a.x += a.xv
            a.y += a.yv
            

            # COLISÃO entre PLAYER e ASTEROIDE
            if (player.x >= a.x and player.x <= a.x + a.largura) or (player.x + player.largura >= a.x and player.x + player.largura <= a.x + a.largura):
                if (player.y >= a.y and player.y <= a.y + a.altura) or (player.y + player.altura >= a.y and player.y + player.altura <= a.y + a.altura):
                    vidas -= 1
                    asteroides.pop(asteroides.index(a))
                    break


            # COLISÃO entre PROJETIL e ASTEROIDE
            for b in playerBullets:
                if (b.x >= a.x and b.x <= a.x + a.largura) or b.x + b.largura >= a.x and b.x + b.largura <= a.x + a.largura:
                    if (b.y >= a.y and b.y <= a.y + a.altura) or b.y + b.largura >= a.y and b.y + b.altura <= a.y + a.altura:
                        
                        # Quebrando os asteroides
                        if a.categoria == 3:
                            pontos += 10
                            novoAste = Asteroide(2)
                            novoAste.x = a.x
                            novoAste.y = a.y
                            asteroides.append(novoAste)
                        elif a.categoria == 2:
                            pontos += 20
                            novoAste = Asteroide(1)
                            novoAste.x = a.x
                            novoAste.y = a.y
                            asteroides.append(novoAste)
                        else:
                            pontos += 30

                        # excluíndo projétil e asteroide para economizar memória                      
                        asteroides.pop(asteroides.index(a))
                        playerBullets.pop(playerBullets.index(b))
        if vidas  <= 0:
            gameover = True

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            player.viraEsquerda()
        if teclas[pygame.K_RIGHT]:
            player.viraDireita()
        if teclas[pygame.K_UP]:
            player.paraFrente()
        if teclas[pygame.K_DOWN]:
            player.paraTraz()
    
    for event in pygame.event.get():
        # caso o jogador tenha saído, terminar jogo
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not gameover:
                    playerBullets.append(Projetil())
                
                # apertar espaço para jogar de novo
                else:
                    gameover = False
                    vidas = 3
                    pontos = 0 
                    asteroides.clear()
                    
    desenhandoTelaFinal()

pygame.quit()