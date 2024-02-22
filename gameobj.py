SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 650
BALL_RADIUS = 5

pwidth, pheight = 20, 100


class Game:

    MAXVEL = 4

    def __init__(
        self,
        y1,
        y2,
        by,
        bx,
    ):
        self.y1 = y1
        self.y2 = y2
        self.x1 = 10
        self.x2 = SCREEN_WIDTH - 10 - pwidth

        self.by = self.origy = by
        self.bx = self.origx = bx

        self.x_vel = self.MAXVEL
        self.y_vel = 0
        self.radius = 5

        self.paddle_velocity = 5

    def reset(self):
        self.bx = self.origx
        self.by = self.origy
        self.y_vel = 0
        self.x_vel *= -1

    def update_paddle(self, player_1, player_2):

        if player_1[0] == True:
            self.y1 -= self.paddle_velocity
        else:
            self.y1 = self.y1

        if player_1[1] == True:
            self.y1 += self.paddle_velocity
        else:
            self.y1 = self.y1

        if player_2[0] == True:
            self.y2 -= self.paddle_velocity
        else:
            self.y2 = self.y2

        if player_2[1] == True:
            self.y2 += self.paddle_velocity
        else:
            self.y2 = self.y2

        if self.y1 < -pheight:
            self.y1 = SCREEN_HEIGHT
        if self.y1 > SCREEN_HEIGHT:
            self.y1 = 0
        if self.y2 < -pheight:
            self.y2 = SCREEN_HEIGHT
        if self.y2 > SCREEN_HEIGHT:
            self.y2 = 0

    def checkreset(self):
        if self.bx < 0:
            self.reset()
        elif self.bx > SCREEN_WIDTH:
            self.reset()

    def move(self):
        self.bx += self.x_vel
        self.by += self.y_vel
        self.checkreset()

    def collisions(self):

        # for ceiling and bottom collisions
        if self.by + self.radius >= SCREEN_HEIGHT:
            self.y_vel *= -1
        if self.by - self.radius <= 0:
            self.y_vel *= -1

        # for left colls
        if self.x_vel < 0:
            if self.by >= self.y1 and self.by <= self.y1 + pheight:
                if self.bx - self.radius <= self.x1 + pwidth + pwidth:
                    self.x_vel *= -1
                    midy = self.y1 + pheight / 2
                    diffy = midy - self.by
                    reduced = (pheight / 2) / self.MAXVEL
                    self.y_vel = diffy / reduced
                    self.y_vel = self.y_vel * -1

        else:
            if self.by >= self.y2 and self.by <= self.y2 + pheight:
                # prob X2 value
                if self.bx + self.radius >= self.x2 - pwidth:
                    self.x_vel *= -1

                    midy = self.y2 + pheight / 2
                    diffy = midy - self.by
                    reduced = (pheight / 2) / self.MAXVEL
                    y_vel = diffy / reduced
                    self.y_vel = y_vel * -1
        self.move()
