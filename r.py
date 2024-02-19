class Paddle:
    COLOR = PINKISH   # change this to pinkish later
    VEL = 4

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(
            win, self.COLOR, (self.x, self.y, self.width, self.height)
        )

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL


class Ball:
    MAXVEL = 8
    COLOR = WHITE   # change to pinkish later

    def __init__(self, x, y, radius):
        self.x = self.origx = x
        self.y = self.origy = y
        self.radius = radius
        self.x_vel = self.MAXVEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.origx
        self.y = self.origy
        self.y_vel = 0
        self.x_vel *= -1


def collisions(ball, left, right):
    # for ceil colls
    if ball.y + ball.radius >= height:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    # for left colls
    if ball.x_vel < 0:
        if ball.y >= left.y and ball.y <= left.y + left.height:
            if ball.x - ball.radius <= left.x + left.width:
                ball.x_vel *= -1

                midy = left.y + left.height / 2
                diffy = midy - ball.y
                reduced = (left.height / 2) / ball.MAXVEL
                y_vel = diffy / reduced
                ball.y_vel = y_vel * -1

    # for right cols
    else:
        if ball.y >= right.y and ball.y <= right.y + right.height:
            if ball.x + ball.radius >= right.x:
                ball.x_vel *= -1

                midy = right.y + right.height / 2
                diffy = midy - ball.y
                reduced = (right.height / 2) / ball.MAXVEL
                y_vel = diffy / reduced
                ball.y_vel = y_vel * -1

