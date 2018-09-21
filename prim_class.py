# coding=utf-8
class Enemy:
    n_class = 0

    def __init__(self, damage):
        self.damage = damage
        self.add_n()
        self.healt = 20

    @classmethod
    def add_n(cls):
        cls.n_class += 1

    @staticmethod
    def prin_privet(s):
        print(s)

    def atack(self):
        print(f"Atack {self.damage:d}")
        self.prin_privet("!!!!!")

    def __call__(self):
        return self.healt


class BossEnemy(Enemy):
    def __init__(self, damage):
        super().__init__(damage)
        self.coef = 3

    def atack(self):
        print(f"Atack {self.damage * 2 :d}")
        self.prin_privet("!!!!!")

    def superatack(self):
        print(f"SuperAtack {(self.damage * self.coef):d}")
        self.prin_privet("!!!!!")


bot1 = Enemy(1)
print(bot1.n_class)
bot1.atack()
bot2 = Enemy(3)
print(bot2.n_class)
bot2.atack()
bot3 = BossEnemy(3)
bot3.atack()
bot3.superatack()
print(bot3())
