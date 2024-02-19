class dataaa:
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


def collisions(dataaa, left, right):
    # for ceil colls
    if dataaa.by + ball.radius >= SCREEN_HEIGHT:
        dataaa.y_vel *= -1
    elif dataaa.by - ball.radius <= 0:
        dataaa.y_vel *= -1

    # for left colls
    if dataaa.x_vel < 0:
        if dataaa.by >= self.y1 and ball.by <= self.y1 + left.SCREEN_HEIGHT:
            if dataaa.x - ball.radius <= left.x + left.width:
                dataaa.x_vel *= -1

                midy = self.y1 + left.SCREEN_HEIGHT / 2
                diffy = midy - dataaa.by
                reduced = (left.SCREEN_HEIGHT / 2) / dataaa.MAXVEL
                y_vel = diffy / reduced
                dataaa.y_vel = y_vel * -1

    # for right cols
    else:
        if dataaa.by >= self.y2 and ball.by <= self.y2 + right.SCREEN_HEIGHT:
            if dataaa.x + ball.radius >= right.x:
                dataaa.x_vel *= -1

                midy = self.y2 + right.SCREEN_HEIGHT / 2
                diffy = midy - dataaa.y
                reduced = (right.SCREEN_HEIGHT / 2) / dataaa.MAXVEL
                y_vel = diffy / reduced
                dataaa.y_vel = y_vel * -1
