
import constantes
import os
import pygame
import sys
pygame.init()

WIDTH, HEIGHT = 700, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
esta_rodando = True
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 15
SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WINNING_SCORE = 5
class Paddle:
    VEL = 6
    def __init__(self, x ,color, y , largura, altura):
        self.x = self.original_x = x
        self.color = color
        self.y = self.original_y = y
        self.largura = largura
        self.altura = altura

    def draw(self, win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.largura, self.altura))

    def move(self, up=True):
        if up:
            self.y += self.VEL
        else:
            self.y -= self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


class Ball:
    MAX_VEL = 10
    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, constantes.BLUE,(self.x, self.y),self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


def draw(win,paddles, ball, left_score, right_score):

        screen.fill(constantes.BLACK) #preenche o box de preto se nao ficaria o rastro

        left_score_text = SCORE_FONT.render(f'{left_score}', True, constantes.GREEN)
        right_score_text = SCORE_FONT.render(f'{right_score}', True, constantes.WHITE)
        win.blit(left_score_text,(WIDTH//4 - left_score_text.get_width()//2,20))
        win.blit(right_score_text, (WIDTH * (3 / 4) - right_score_text.get_width() // 2, 20))


        for paddle in paddles:
            paddle.draw(win)

        ball.draw(win)

        pygame.display.update()

def handle_collision(ball,left_paddle,right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel*= -1

    if ball.x_vel < 0:#isso calcula o movimento em x do paddle da esquerda
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.altura:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.largura:
                ball.x_vel *= -1
                # isso calcula o movimento em y ou seja o angulo
                middle_y = left_paddle.y + left_paddle.altura / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.altura/2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1*y_vel


    else:
        # isso calcula o movimento em x do paddle da direita
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.altura:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1
                #isso calcula o movimento em y ou seja o angulo
                middle_y = right_paddle.y + right_paddle.altura / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.altura / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1*y_vel



def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=False)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.altura <= HEIGHT:
        left_paddle.move(up=True)

    if keys[pygame.K_UP] and left_paddle.y - left_paddle.VEL >= 0:
        right_paddle.move(up=False)
    if keys[pygame.K_DOWN] and left_paddle.y + left_paddle.VEL + left_paddle.altura <= HEIGHT:
        right_paddle.move(up=True)



def main():
    esta_rodando = True
    clock = pygame.time.Clock()
#desenhando os paddles
    left_paddle = Paddle(10, constantes.GREEN,HEIGHT // 2 - PADDLE_HEIGHT //
                         2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, constantes.WHITE,HEIGHT //
                          2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
#desenhando a bola
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

#implementando a pontuacao
    left_score = 0
    right_score = 0

    while esta_rodando:
        draw(screen,[left_paddle,right_paddle],ball, left_score, right_score)
        clock.tick(constantes.FPS)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                esta_rodando = False



        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys,left_paddle,right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "GREEN PLAYER WON"
            text = SCORE_FONT.render(win_text, 1, constantes.GREEN)
            screen.blit(text, (WIDTH // 2 - text.get_width() //
                               2, HEIGHT // 2 - text.get_height() // 2))
            esta_rodando = False
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "WHITE PLAYER WON"
            text = SCORE_FONT.render(win_text, 1, constantes.WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() //
                               2, HEIGHT // 2 - text.get_height() // 2))
            esta_rodando = False

        if won:
            pygame.display.update()
            pygame.time.delay(2000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0
            pygame.quit()





if __name__ == '__main__':
    main()



