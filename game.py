import os
import pygame
pygame.init()

width, height =  1000, 650
PINKISH = (250, 100, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
pwidth, pheight = 20, 100
ballradius = 8
scorefont = pygame.font.SysFont("comicsans",50)
winscore = 3

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong Apparently")

bong_img = pygame.image.load(os.path.join("assets", "bong.png"))
bong = pygame.transform.scale(bong_img, (150, 150))

bogn_img = pygame.image.load(os.path.join("assets", "bogn.png"))
bogn = pygame.transform.scale(bogn_img, (150, 150))

bolll_img = pygame.image.load(os.path.join("assets", "balll.png"))
bolll = pygame.transform.scale(bolll_img, (330, 330))

class Paddle:
    COLOR = PINKISH #change this to pinkish later
    VEL = 4
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

class Ball:
    MAXVEL = 8
    COLOR = WHITE #change to pinkish later

    def __init__(self,x,y,radius):
        self.x = self.origx = x
        self.y = self.origy = y
        self.radius =radius
        self.x_vel = self.MAXVEL
        self.y_vel = 0

    def draw(self,win):
        pygame.draw.circle(win, self.COLOR,(self.x,self.y),self.radius)

    def move(self):
        self.x+=self.x_vel
        self.y+=self.y_vel

    def reset(self):
        self.x = self.origx
        self.y = self.origy
        self.y_vel=0
        self.x_vel*=-1


def draw(win, paddles, bong, bogn,ball,bolll,leftscr,rightscr):
    win.fill(PINKISH)

    leftscore = scorefont.render(f"{leftscr}",1,WHITE)
    rightscore = scorefont.render(f"{rightscr}",1,WHITE)
    win.blit(leftscore,(width//4 - leftscore.get_width()//2,20))
    win.blit(rightscore,(width*(3/4) - rightscore.get_width()//2,20))


    for paddle in paddles:
        paddle.draw(win)

    ball.draw(win)

    win.blit(bong, (paddles[0].x - 45, paddles[0].y - 35))
    win.blit(bogn, (paddles[1].x -110, paddles[1].y-35))
    win.blit(bolll,(ball.x -123,ball.y-120))

    pygame.display.update()



def collisions(ball,left,right):
    #for ceil colls
    if ball.y + ball.radius>=height:
        ball.y_vel*=-1
    elif ball.y - ball.radius <= 0:
        ball.y_vel*=-1

    #for left colls
    if ball.x_vel<0:
        if ball.y >= left.y and ball.y<= left.y+left.height:
            if ball.x- ball.radius <= left.x + left.width:
                ball.x_vel*=-1

                midy = left.y + left.height/2
                diffy = midy - ball.y
                reduced = (left.height/2)/ball.MAXVEL
                y_vel = diffy / reduced
                ball.y_vel = y_vel *-1

    #for right cols
    else:
        if ball.y >= right.y and ball.y<= right.y+right.height:
            if ball.x + ball.radius >= right.x:
                ball.x_vel*=-1

                midy = right.y + right.height/2
                diffy = midy - ball.y
                reduced = (right.height/2)/ball.MAXVEL
                y_vel = diffy / reduced
                ball.y_vel = y_vel * -1

        

def paddle_movemment(keys, left, right):
    if keys[pygame.K_w]:
        left.move(up=True)
    if keys[pygame.K_s]:
        left.move(up=False)
    if keys[pygame.K_UP]:
        right.move(up=True)
    if keys[pygame.K_DOWN]:
        right.move(up=False)
    if left.y < -left.height:
        left.y = height
    if left.y > height:
        left.y = 0
    if right.y < -right.height:
        right.y = height
    if right.y > height:
        right.y = 0

def main():
    run = True
    clock = pygame.time.Clock()

    left = Paddle(10, height//2 - pheight//2, pwidth, pheight)
    right = Paddle(width - 10 - pwidth, height//2 - pheight//2, pwidth, pheight)
    ball = Ball(width//2,height//2,ballradius)

    leftscr =0
    rightscr = 0

    while run:
        clock.tick(60)

        draw(win, [left, right], bong, bogn,ball,bolll,leftscr,rightscr)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    break

        keys = pygame.key.get_pressed()
        paddle_movemment(keys, left, right)

        ball.move()
        collisions(ball,left,right)

        if ball.x<0:
            rightscr+=1
            ball.reset()
        elif ball.x>width:
            leftscr+=1
            ball.reset()

        won = False
        if leftscr >= winscore:
            won = True
            wintext = "Left Player Won!"
        elif rightscr >= winscore:
            won = True
            wintext = "Right Player Won!"

        if won:
            text = scorefont.render(wintext, 1, WHITE)
            win.blit(text, (width//2 - text.get_width() //2, height//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(2000)
            ball.reset()
            
            
    pygame.quit()


if __name__ == '__main__':
    main()
