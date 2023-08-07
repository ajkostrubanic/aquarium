from typing import List, Dict
from collections import defaultdict
import random, shutil, time, sys, os

WIDTH, HEIGHT = shutil.get_terminal_size()
CLEAR = 'clear' if os.name == 'posix' else 'CLS'

LEFT, RIGHT = 'LR'
FISH_TYPES = [
    {LEFT: "<###><", RIGHT: "><###>"},
    {LEFT: "<XXX><", RIGHT: "><XXX>"},
    {LEFT: "<999><", RIGHT: "><999>"},
    {LEFT: "<888><", RIGHT: "><888>"},
]

BIG_FISH_TYPES = [
    {LEFT: [
        r"  /#######\  ",
        r"< o #######<<",
        r"  \#######/  "
        ],
    RIGHT: [
        r"  /########\ ",
        r">>####### o >",
        r"  \########/ "
    ]},
    {LEFT: [
        r"  /9999999999\   ",
        r"< o 9999999999 <<",
        ],
    RIGHT: [
        r"   /9999999999\  ",
        r">> 9999999999 o >",
    ]}
]

class Fish:
    def __init__(self, ascii: dict[str, str], x: int, y: int):
        self.ascii_left = ascii[LEFT]
        self.ascii_right = ascii[RIGHT]
        self.x = x
        self.y = y
        self.dir = random.choice([LEFT, RIGHT])

    def ascii(self) -> str:
        if self.dir == LEFT:
            return self.ascii_left
        else:
            return self.ascii_right
        
    def draw(self, aquarium: dict[tuple[int,int], str]) -> None:
        ascii = self.ascii()
        x, y = self.x, self.y
        for i, ch in enumerate(ascii):
            aquarium[x+i,y] = ch

    def simulate(self) -> None:
        x, y = self.x, self.y
        dir = self.dir
        if dir == LEFT and x < 5:
            self.dir = RIGHT
            self.x += 1
        elif dir == LEFT:
            self.x -= 1
        elif dir == RIGHT and x > WIDTH - 5:
            self.dir = LEFT
            self.x -= 1
        elif dir == RIGHT:
            self.x += 1
        if 2 <= y <= HEIGHT-2:
            self.y += random.choice([-1, 0, 0, 0, 1])
        elif y <= 2:
            self.y += 1
        elif y >= HEIGHT-2:
            self.y -= 1

class BigFish(Fish):
    def draw(self, aquarium: dict[tuple[int,int], str]) -> None:
        ascii = self.ascii()
        x, y = self.x, self.y
        for j, line in enumerate(ascii):
            for i, ch in enumerate(line):
                aquarium[x+i,y+j] = ch

    def simulate(self) -> None:
        x, y = self.x, self.y
        dir = self.dir
        if dir == LEFT and x < 20:
            self.dir = RIGHT
            self.x += 1
        elif dir == LEFT:
            self.x -= 1
        elif dir == RIGHT and x > WIDTH - 20:
            self.dir = LEFT
            self.x -= 1
        elif dir == RIGHT:
            self.x += 1
        if 5 <= y <= HEIGHT-5:
            self.y += random.choice([-1, 0, 0, 0, 1])
        elif y <= 5:
            self.y += 1
        elif y >= HEIGHT-5:
            self.y -= 1

class Kelp:
    def __init__(self, x: int, height: int):
        self.x = x
        self.h = height

    def draw(self, aquarium: dict[tuple[int,int], str]) -> None:
        for dj in range(self.h):
            ascii = random.choice(["( ", ") ", " )", " ("])
            for di in range(2):
                aquarium[self.x+di, HEIGHT - dj] = ascii[di]

class Bubble:
    def __init__(self, ascii: str, x: int, y: int):
        self.ascii = ascii
        self.x = x
        self.y = y

    def draw(self, aquarium: dict[tuple[int,int], str]) -> None:
        aquarium[self.x, self.y] = self.ascii

    def simulate(self) -> None:
        self.y -= 1

    def out_of_bounds(self) -> bool:
        return self.y < 0
       

def generate_random_fishes(n: int) -> List[Fish]:
    """Generate a random array of `n` fishes."""
    fishes = []
    for i in range(n):
        fish = Fish(
            ascii=random.choice(FISH_TYPES),
            x=random.randint(5,WIDTH-5),
            y=random.randint(5,HEIGHT-5)
        )
        fishes.append(fish)
    return fishes

def generate_random_big_fishes(n: int) -> List[BigFish]:
    """Generate a random array of `n` big fishes."""
    big_fishes = []
    for i in range(n):
        big_fish = BigFish(
            ascii=random.choice(BIG_FISH_TYPES),
            x=random.randint(10,WIDTH-10),
            y=random.randint(5,HEIGHT-5)
        )
        big_fishes.append(big_fish)
    return big_fishes

def generate_random_kelp(n: int) -> List[Kelp]:
    kelps = []
    for i in range(n):
        kelp = Kelp(
            x=random.randint(5, WIDTH-5),
            height=random.randint(5,20)
        )
        kelps.append(kelp)
    return kelps

def print_aquarium(fishes: List[Fish], big_fishes: List[BigFish], kelps: List[Kelp], bubbles: List[Bubble]) -> None:
    aquarium = defaultdict(lambda: ' ')

    for kelp in kelps:
        kelp.draw(aquarium)

    for bubble in bubbles:
        bubble.draw(aquarium)

    for fish in fishes:
        fish.draw(aquarium)

    for big_fish in big_fishes:
        big_fish.draw(aquarium)

    lines = ""
    for y in range(HEIGHT):
        line = ""
        for x in range(WIDTH):
            line += aquarium[x,y]
        lines += line + '\n'
    os.system(CLEAR)
    print(lines, flush=True)

def simulate_aquarium(fishes: List[Fish], big_fishes: List[BigFish], bubbles: List[Bubble]) -> List[Dict]:
    fishes_p = []
    big_fishes_p = []

    if random.random() < 0.1:
        bubbles.append(Bubble(
            ascii=random.choice(['O', 'o', '0']),
            x=random.randint(-5, WIDTH-5),
            y=HEIGHT
        ))

    for fish in fishes:
        fish.simulate()

    for big_fish in big_fishes:
        big_fish.simulate()

    for bubble in bubbles:
        bubble.simulate()
        if bubble.out_of_bounds():
            bubbles.remove(bubble)
    
    return fishes, big_fishes, bubbles


try:
    fishes = generate_random_fishes(8)
    big_fishes = generate_random_big_fishes(2)
    kelps = generate_random_kelp(10)
    bubbles = []
    print_aquarium(fishes, big_fishes, kelps, bubbles)
    while True:
        fishes, big_fishes, bubbles = simulate_aquarium(fishes, big_fishes, bubbles)
        print_aquarium(fishes, big_fishes, kelps, bubbles)
        time.sleep(0.2)
except KeyboardInterrupt:
    print("Goodbye.")