class Level:
    def __init__(self, current_level=1, current_xp=0):
        self.current_level = current_level
        self.current_xp = current_xp
        self.xp_table = {
            1: 0,
            2: 300,
            3: 900,
            4: 2700,
            5: 6500,
            6: 14000,
            7: 23000,
            8: 34000,
            9: 48000,
            10: 64000,
            11: 85000,
            12: 100000,
            13: 120000,
            14: 140000,
            15: 165000,
            16: 195000,
            17: 225000,
            18: 265000,
            19: 305000,
            20: 355000
        }

    @property
    def experience_to_next_level(self):
        if self.current_level < 20:
            return self.xp_table[self.current_level + 1] - self.xp_table[self.current_level]

    def add_xp(self, xp):
        self.current_xp += xp

        if self.current_xp > self.experience_to_next_level:
            self.current_xp -= self.experience_to_next_level
            self.current_level += 1
            return True
        return False
