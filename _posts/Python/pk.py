class Pokemon:
    ATTR_TYPE_CHOICES = (
        'electric', 'fire', 'water', 'grass', 'stone'
    )

    def __init__(self, name, attr_type, hp, damage, defence, speed):
        self.__name = name
        self.__hp = [hp, hp]
        self.__damage = damage
        self.__defence = defence
        self.__speed = speed

        if attr_type in self.ATTR_TYPE_CHOICES:
            self.__attr_type = attr_type
        else:
            raise ValueError(f"attr_type must be one of the followings: {self.ATTR_TYPE_CHOICES}")

    @property
    def name(self):
        return self.__name
    
    @property
    def status(self):
        info_dict = {
            "name": self.__name,
            "hp": f'{self.__hp[0]}/{self.__hp[1]}',
            "damage": self.__damage,
            "defence": self.__defence,
            "speed": self.__speed,
            "type": self.__attr_type
        }
        return info_dict

    def _damaged(self, demage):
        self.__hp[0] -= (demage - self.__defence)

    def is_dead(self):
        if self.__hp[0] <= 0:
            return True, f'{self.name} is dead!'
        else:
            return False, None

    def attack(self, target):
        target._damaged(self.__damage)

        base_msg = f'{self.__name} attacked {target.name}! '

        target_dead, msg = target.is_dead()

        if target_dead:
            return base_msg + msg
        else:
            return base_msg

p = Pokemon('피카츄', 'electric', 140, 30, 10, 10)

f = Pokemon('파이리', 'fire', 150, 40, 5, 5)
