import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Охота на кабанчиков")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("arial", 20, bold=True)
BIG = pygame.font.SysFont("arial", 36, bold=True)
SMALL = pygame.font.SysFont("arial", 15)

WHITE = (245, 245, 245)
GOLD = (255, 205, 40)
GREEN = (70, 220, 90)
RED = (220, 45, 40)
BLUE = (80, 190, 255)
PURPLE = (190, 90, 255)

WEAPONS = {
    "Двустволка": {"price": 0, "damage": 45, "delay": 500, "ammo": 2, "reload": 1200, "radius": 0},
    "Пистолет": {"price": 100, "damage": 25, "delay": 250, "ammo": 12, "reload": 1000, "radius": 0},
    "Два пистолета": {"price": 300, "damage": 19, "delay": 160, "ammo": 24, "reload": 1200, "radius": 0},
    "Томпсон": {"price": 400, "damage": 15, "delay": 100, "ammo": 30, "reload": 1400, "radius": 0},
    "Автомат": {"price": 550, "damage": 24, "delay": 115, "ammo": 32, "reload": 1450, "radius": 0},
    "Дробовик": {"price": 650, "damage": 72, "delay": 620, "ammo": 6, "reload": 1500, "radius": 0},
    "Снайперка": {"price": 800, "damage": 150, "delay": 1050, "ammo": 5, "reload": 1700, "radius": 0},
    "Миниган": {"price": 1100, "damage": 13, "delay": 55, "ammo": 100, "reload": 2300, "radius": 0},
    "РПГ": {"price": 600, "damage": 110, "delay": 900, "ammo": 1, "reload": 1800, "radius": 130},
    "Гранатомёт": {"price": 850, "damage": 75, "delay": 650, "ammo": 4, "reload": 1600, "radius": 100},
    "Лазерная винтовка": {"price": 1400, "damage": 48, "delay": 130, "ammo": 40, "reload": 1600, "radius": 0},
    "Плазмопушка": {"price": 1800, "damage": 160, "delay": 800, "ammo": 5, "reload": 1900, "radius": 155},
}

# Боссы появляются по очереди: у каждого свои здоровье, скорость, размер и урон.
BOSS_TYPES = [
    "Король кабанов",
    "Огненный кабан",
    "Бронированный титан",
    "Ядовитый кабан",
    "Киберкабан",
]

DIFFICULTIES = {
    "Легко": (200, 0.75, 0.8),
    "Нормально": (150, 1.0, 1.0),
    "Сложно": (110, 1.5, 1.35),
}

# Экономика сложности: множитель цены оружия и награды за кабанчиков.
# Легко: оружие дешевле, очков выпадает больше.
# Нормально: стандартные цены и награды.
# Сложно: оружие дороже, очков выпадает меньше.
ECONOMY = {
    "Легко": {"price": 0.65, "reward": 0.90},
    "Нормально": {"price": 1.00, "reward": 0.65},
    "Сложно": {"price": 1.60, "reward": 0.30},
}

UPGRADE_NAMES = {
    "damage": "Урон оружия",
    "fire_rate": "Скорость стрельбы",
    "magazine": "Размер магазина",
}

# Уровень 0 — закрыто, уровень 1 — разблокировано.
# Максимальный уровень каждой способности — 3.
SKILL_NAMES = {
    "shurikens": "Шурикены",
    "berserk": "Берсерк",
    "telekinesis": "Телекинез",
    "dash": "Рывок",
}

SKILL_DESCRIPTIONS = {
    "shurikens": "Вращающиеся шурикены наносят урон при касании.",
    "berserk": "Временно увеличивает урон оружия.",
    "telekinesis": "Уничтожает одного кабанчика на экране.",
    "dash": "Быстрый рывок в выбранном направлении.",
}



LANGUAGES = ["Русский", "Українська", "English"]
language_index = 0

# Переводы интерфейса. Игровая логика и названия внутренних параметров не меняются.
TRANSLATIONS = {
    "Українська": {
        "ОХОТА НА КАБАНЧИКОВ": "ПОЛЮВАННЯ НА КАБАНЧИКІВ", "Выбери сложность:": "Обери складність:",
        "Легко": "Легко", "Нормально": "Нормально", "Сложно": "Складно",
        "ENTER — начать": "ENTER — почати", "WASD — движение | зажми ЛКМ для автострельбы | B — магазин | U — улучшения": "WASD — рух | затисни ЛКМ для автострільби | B — магазин | U — покращення",
        "N — навыки | Q — шурикены | E — берсерк | F — телекинез | SHIFT — рывок": "N — навички | Q — сюрикени | E — берсерк | F — телекінез | SHIFT — ривок",
        "12 видов оружия и 5 разных боссов!": "12 видів зброї та 5 різних босів!",
        "Здоровье:": "Здоров’я:", "Очки:": "Монети:", "Детали:": "Деталі:", "Очки навыков:": "Очки навичок:", "Убийства:": "Вбивства:", "Оружие:": "Зброя:", "Патроны:": "Набої:",
        "Дрон: куплен": "Дрон: куплено", "Дрон: G в игре / магазин": "Дрон: G у грі / магазин", "B — магазин | U — улучшения | N — навыки": "B — магазин | U — покращення | N — навички",
        "ПЕРЕЗАРЯДКА...": "ПЕРЕЗАРЯДЖАННЯ...", "ТЫ ПРОИГРАЛ!": "ТИ ПРОГРАВ!", "SPACE — начать заново": "SPACE — почати знову",
        "МАГАЗИН ОРУЖИЯ": "МАГАЗИН ЗБРОЇ", "КУПЛЕНО": "КУПЛЕНО", "МОДЕРНИЗАЦИЯ": "МОДЕРНІЗАЦІЯ", "Детали босса:": "Деталі боса:",
        "Урон оружия": "Шкода зброї", "Скорость стрельбы": "Швидкість стрільби", "Размер магазина": "Розмір магазину",
        "Шурикены": "Сюрикени", "Берсерк": "Берсерк", "Телекинез": "Телекінез", "Рывок": "Ривок",
        "Урон +20% за уровень": "Шкода +20% за рівень", "Стрельба быстрее на 12%": "Стрільба швидша на 12%", "Магазин больше на 25%": "Магазин більший на 25%",
        "1 деталь": "1 деталь", "Нажми на улучшение | U — закрыть": "Натисни на покращення | U — закрити", "ДЕРЕВО НАВЫКОВ": "ДЕРЕВО НАВИЧОК",
        "Нажми на навык: открыть — 1 очко, улучшить — 1 очко": "Натисни на навичку: відкрити — 1 очко, покращити — 1 очко",
        "ЗАКРЫТО": "ЗАКРИТО", "ГОТОВО": "ГОТОВО", "ОТКРЫТЬ — 1 очко": "ВІДКРИТИ — 1 очко", "УЛУЧШИТЬ — 1 очко": "ПОКРАЩИТИ — 1 очко", "МАКСИМУМ": "МАКСИМУМ",
        "N — закрыть | Очки выдаются за победу над боссом": "N — закрити | Очки даються за перемогу над босом",
        "Двустволка": "Двостволка", "Пистолет": "Пістолет", "Два пистолета": "Два пістолети", "Томпсон": "Томпсон", "Автомат": "Автомат", "Дробовик": "Дробовик", "Снайперка": "Снайперка", "Миниган": "Мініган", "РПГ": "РПГ", "Гранатомёт": "Гранатомет", "Лазерная винтовка": "Лазерна гвинтівка", "Плазмопушка": "Плазмова гармата",
        "Король кабанов": "Король кабанів", "Огненный кабан": "Вогняний кабан", "Бронированный титан": "Броньований титан", "Ядовитый кабан": "Отруйний кабан", "Киберкабан": "Кіберкабан",
        "Куплено:": "Куплено:", "Выбрано:": "Обрано:", "Не хватает очков! Нужно:": "Не вистачає монет! Потрібно:", "Дрон уже куплен!": "Дрон уже куплено!", "ДРОН КУПЛЕН! Он помогает стрелять.": "ДРОН КУПЛЕНО! Він допомагає стріляти.", "Для дрона нужно 3000 очков!": "Для дрона потрібно 3000 монет!",
        "Улучшено:": "Покращено:", "Нужны детали с босса!": "Потрібні деталі з боса!", "Разблокировано:": "Відкрито:", "Нет очков навыков! Победи босса.": "Немає очок навичок! Переможи боса.", "Нет очков навыков!": "Немає очок навичок!", "У этой способности максимальный уровень!": "Ця здібність має максимальний рівень!",
        "КУПЛЕН": "КУПЛЕНО", "не куплен": "не куплено", "Урон ": "Шкода ", "магазин ": "магазин ", "перезарядка ": "перезаряджання ", " очков": " монет", "уровень ": "рівень ", " с": " с",
        "G — дрон за 3000 очков": "G — дрон за 3000 монет", "B — закрыть": "B — закрити", "Уровень 1": "Рівень 1", "Уровень 2": "Рівень 2", "Уровень 3 — МАКС.": "Рівень 3 — МАКС.",
        "Вращающиеся шурикены наносят урон при касании.": "Сюрикени, що обертаються, завдають шкоди при дотику.", "Временно увеличивает урон оружия.": "Тимчасово збільшує шкоду зброї.", "Уничтожает одного кабанчика на экране.": "Знищує одного кабанчика на екрані.", "Быстрый рывок в выбранном направлении.": "Швидкий ривок у вибраному напрямку.",
        "L — язык: ": "L — мова: ", "Русский": "Російська", "Українська": "Українська", "English": "Англійська",
        "Экономика: оружие x": "Економіка: зброя x", " | награды x": " | нагороди x", "Дрон: ": "Дрон: ", "Убийств: ": "Вбивств: ", " | Очков: ": " | Монет: ",
        "Ящики: аптечки / патроны / монеты / детали": "Ящики: аптечки / набої / монети / деталі",
        "АПТЕЧКА: здоровье восстановлено!": "АПТЕЧКА: здоров’я відновлено!",
        "ЯЩИК БОЕПРИПАСОВ: магазин заполнен!": "ЯЩИК БОЄПРИПАСІВ: магазин заповнено!",
        "ТАЙНИК: ": "СХОВОК: ", " монет!": " монет!", "ЯЩИК ДЕТАЛЕЙ: ": "ЯЩИК ДЕТАЛЕЙ: ",
    },
    "English": {
        "ОХОТА НА КАБАНЧИКОВ": "BOAR HUNT", "Выбери сложность:": "Choose difficulty:", "Легко": "Easy", "Нормально": "Normal", "Сложно": "Hard",
        "ENTER — начать": "ENTER — start", "WASD — движение | зажми ЛКМ для автострельбы | B — магазин | U — улучшения": "WASD — move | hold LMB to auto-fire | B — shop | U — upgrades",
        "N — навыки | Q — шурикены | E — берсерк | F — телекинез | SHIFT — рывок": "N — skills | Q — shurikens | E — berserk | F — telekinesis | SHIFT — dash",
        "12 видов оружия и 5 разных боссов!": "12 weapons and 5 unique bosses!", "Здоровье:": "Health:", "Очки:": "Coins:", "Детали:": "Parts:", "Очки навыков:": "Skill points:", "Убийства:": "Kills:", "Оружие:": "Weapon:", "Патроны:": "Ammo:",
        "Дрон: куплен": "Drone: owned", "Дрон: G в игре / магазин": "Drone: G in game / shop", "B — магазин | U — улучшения | N — навыки": "B — shop | U — upgrades | N — skills", "ПЕРЕЗАРЯДКА...": "RELOADING...", "ТЫ ПРОИГРАЛ!": "YOU DIED!", "SPACE — начать заново": "SPACE — restart",
        "МАГАЗИН ОРУЖИЯ": "WEAPON SHOP", "КУПЛЕНО": "OWNED", "МОДЕРНИЗАЦИЯ": "UPGRADES", "Детали босса:": "Boss parts:", "Урон оружия": "Weapon damage", "Скорость стрельбы": "Fire rate", "Размер магазина": "Magazine size",
        "Шурикены": "Shurikens", "Берсерк": "Berserk", "Телекинез": "Telekinesis", "Рывок": "Dash", "Урон +20% за уровень": "Damage +20% per level", "Стрельба быстрее на 12%": "12% faster firing", "Магазин больше на 25%": "25% larger magazine",
        "1 деталь": "1 part", "Нажми на улучшение | U — закрыть": "Click an upgrade | U — close", "ДЕРЕВО НАВЫКОВ": "SKILL TREE", "Нажми на навык: открыть — 1 очко, улучшить — 1 очко": "Click a skill: unlock — 1 point, upgrade — 1 point",
        "ЗАКРЫТО": "LOCKED", "ГОТОВО": "READY", "ОТКРЫТЬ — 1 очко": "UNLOCK — 1 point", "УЛУЧШИТЬ — 1 очко": "UPGRADE — 1 point", "МАКСИМУМ": "MAX LEVEL", "N — закрыть | Очки выдаются за победу над боссом": "N — close | Earn points by defeating bosses",
        "Двустволка": "Double-barrel", "Пистолет": "Pistol", "Два пистолета": "Dual pistols", "Томпсон": "Thompson", "Автомат": "Assault rifle", "Дробовик": "Shotgun", "Снайперка": "Sniper rifle", "Миниган": "Minigun", "РПГ": "RPG", "Гранатомёт": "Grenade launcher", "Лазерная винтовка": "Laser rifle", "Плазмопушка": "Plasma cannon",
        "Король кабанов": "Boar King", "Огненный кабан": "Fire Boar", "Бронированный титан": "Armored Titan", "Ядовитый кабан": "Poison Boar", "Киберкабан": "Cyber Boar",
        "Куплено:": "Purchased: ", "Выбрано:": "Selected: ", "Не хватает очков! Нужно:": "Not enough coins! Need: ", "Дрон уже куплен!": "Drone already owned!", "ДРОН КУПЛЕН! Он помогает стрелять.": "DRONE PURCHASED! It helps you shoot.", "Для дрона нужно 3000 очков!": "The drone costs 3000 coins!", "Улучшено:": "Upgraded: ", "Нужны детали с босса!": "You need boss parts!", "Разблокировано:": "Unlocked: ", "Нет очков навыков! Победи босса.": "No skill points! Defeat a boss.", "Нет очков навыков!": "No skill points!", "У этой способности максимальный уровень!": "This skill is already max level!",
        "КУПЛЕН": "OWNED", "не куплен": "not owned", "Урон ": "Damage ", "магазин ": "magazine ", "перезарядка ": "reload ", " очков": " coins", "уровень ": "level ", " с": " s", "G — дрон за 3000 очков": "G — drone for 3000 coins", "B — закрыть": "B — close", "Уровень 1": "Level 1", "Уровень 2": "Level 2", "Уровень 3 — МАКС.": "Level 3 — MAX",
        "Вращающиеся шурикены наносят урон при касании.": "Orbiting shurikens damage enemies on contact.", "Временно увеличивает урон оружия.": "Temporarily increases weapon damage.", "Уничтожает одного кабанчика на экране.": "Destroys one boar on screen.", "Быстрый рывок в выбранном направлении.": "Quick dash in the chosen direction.", "L — язык: ": "L — language: ", "Русский": "Russian", "Українська": "Ukrainian", "English": "English",
        "Экономика: оружие x": "Economy: weapon x", " | награды x": " | rewards x", "Дрон: ": "Drone: ", "Убийств: ": "Kills: ", " | Очков: ": " | Coins: ",
        "Ящики: аптечки / патроны / монеты / детали": "Crates: medkits / ammo / coins / parts",
        "АПТЕЧКА: здоровье восстановлено!": "MEDKIT: health restored!",
        "ЯЩИК БОЕПРИПАСОВ: магазин заполнен!": "AMMO CRATE: magazine refilled!",
        "ТАЙНИК: ": "CACHE: ", " монет!": " coins!", "ЯЩИК ДЕТАЛЕЙ: ": "PARTS CRATE: ",
    },
}

def translate(value):
    result = str(value)
    language = LANGUAGES[language_index]
    if language == "Русский":
        return result
    dictionary = TRANSLATIONS[language]
    if result in dictionary:
        return dictionary[result]
    # Replace known phrases longest-first so dynamic values remain intact.
    for source in sorted(dictionary, key=len, reverse=True):
        if source and source in result:
            result = result.replace(source, dictionary[source])
    return result


def text(value, x, y, color=WHITE, font=FONT, center=False):
    image = font.render(translate(value), True, color)
    rect = image.get_rect()
    if center:
        rect.center = (int(x), int(y))
    else:
        rect.topleft = (int(x), int(y))
    screen.blit(image, rect)


def line(color, start, end, thickness):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.hypot(dx, dy)
    if length < 1:
        return

    surface = pygame.Surface(
        (max(1, int(length)) + 4, max(1, thickness) + 4),
        pygame.SRCALPHA
    )
    pygame.draw.rect(
        surface, (15, 15, 15),
        (0, 0, surface.get_width(), surface.get_height()),
        border_radius=3
    )
    pygame.draw.rect(
        surface, color,
        (2, 2, max(1, int(length)), max(1, thickness)),
        border_radius=3
    )

    rotated = pygame.transform.rotate(
        surface, -math.degrees(math.atan2(dy, dx))
    )
    screen.blit(
        rotated,
        rotated.get_rect(center=(
            int((start[0] + end[0]) / 2),
            int((start[1] + end[1]) / 2)
        ))
    )


def background(px, py):
    screen.fill((66, 85, 59))

    for x in range(int(-px) % 65, WIDTH, 65):
        pygame.draw.line(screen, (60, 78, 54), (x, 0), (x, HEIGHT))

    for y in range(int(-py) % 65, HEIGHT, 65):
        pygame.draw.line(screen, (60, 78, 54), (0, y), (WIDTH, y))
    # Декоративная трава и камешки привязаны к мировым координатам, поэтому не плавают.
    for gx in range(math.floor((px-WIDTH/2)/115), math.ceil((px+WIDTH/2)/115)+1):
        for gy in range(math.floor((py-HEIGHT/2)/115), math.ceil((py+HEIGHT/2)/115)+1):
            seed = (gx * 73856093) ^ (gy * 19349663)
            rng = random.Random(seed)
            wx, wy = gx*115+rng.randint(8, 105), gy*115+rng.randint(8, 105)
            sx, sy = int(WIDTH//2+wx-px), int(HEIGHT//2+wy-py)
            if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
                pygame.draw.line(screen, (81, 105, 61), (sx, sy), (sx-3, sy-8), 2)
                pygame.draw.line(screen, (81, 105, 61), (sx, sy), (sx+4, sy-6), 2)
                if seed % 5 == 0:
                    pygame.draw.ellipse(screen, (82, 83, 70), (sx+7, sy+3, 7, 4))


def draw_player(mouse, weapon, recoil=0, flash=False):
    cx, cy = WIDTH // 2, HEIGHT // 2
    dx, dy = mouse[0] - cx, mouse[1] - cy
    length = max(1, math.hypot(dx, dy))
    ux, uy = dx / length, dy / length
    px, py = -uy, ux

    def p(forward, side=0):
        return (
            int(cx + ux * forward + px * side),
            int(cy + uy * forward + py * side)
        )

    pygame.draw.ellipse(screen, (35, 40, 30), (cx-42, cy+30, 84, 35))
    pygame.draw.ellipse(screen, (25, 25, 23), (cx-34, cy+35, 30, 24))
    pygame.draw.ellipse(screen, (25, 25, 23), (cx+4, cy+35, 30, 24))
    pygame.draw.rect(screen, (68, 83, 54), (cx-29, cy+5, 25, 40), border_radius=5)
    pygame.draw.rect(screen, (68, 83, 54), (cx+4, cy+5, 25, 40), border_radius=5)

    # Тактический рюкзак за плечами и бронежилет с объёмными панелями.
    pygame.draw.rect(screen, (34, 43, 35), (cx-33, cy-20, 15, 35), border_radius=5)
    pygame.draw.rect(screen, (77, 88, 59), (cx-31, cy-17, 11, 25), border_radius=3)
    pygame.draw.ellipse(screen, (30, 35, 28), (cx-34, cy-32, 68, 70))
    pygame.draw.ellipse(screen, (76, 95, 58), (cx-30, cy-30, 60, 64))

    for ox, oy in [(-18, -16), (8, -20), (-6, -3), (14, 7), (-17, 15), (3, 20)]:
        pygame.draw.ellipse(screen, (42, 59, 38), (cx+ox, cy+oy, 13, 8))

    pygame.draw.rect(screen, (35, 42, 36), (cx-23, cy-27, 46, 49), border_radius=7)
    pygame.draw.rect(screen, (91, 100, 72), (cx-18, cy-22, 36, 40), border_radius=5)
    pygame.draw.rect(screen, (47, 58, 47), (cx-13, cy-18, 26, 32), border_radius=4)
    pygame.draw.line(screen, (160, 151, 111), (cx-15, cy-18), (cx+14, cy+15), 3)
    pygame.draw.line(screen, (160, 151, 111), (cx+15, cy-18), (cx-14, cy+15), 3)
    pygame.draw.rect(screen, (42, 47, 38), (cx-8, cy-42, 16, 15), border_radius=3)
    pygame.draw.circle(screen, (124, 91, 69), (cx+2, cy-47), 16)
    pygame.draw.ellipse(screen, (190, 145, 107), (cx-14, cy-59, 28, 24))
    pygame.draw.ellipse(screen, (48, 67, 43), (cx-22, cy-66, 44, 28))
    pygame.draw.ellipse(screen, (93, 108, 67), (cx-18, cy-66, 36, 17))
    pygame.draw.rect(screen, (42, 48, 38), (cx-17, cy-56, 34, 7), border_radius=3)
    pygame.draw.line(screen, (200, 205, 170), (cx-15, cy-53), (cx+15, cy-53), 2)
    pygame.draw.rect(screen, (35, 45, 40), (cx-13, cy-47, 26, 8), border_radius=3)
    pygame.draw.circle(screen, (20, 20, 20), (cx-6+int(ux*4), cy-49+int(uy*3)), 2)
    pygame.draw.circle(screen, (20, 20, 20), (cx+6+int(ux*4), cy-49+int(uy*3)), 2)
    pygame.draw.circle(screen, (205, 165, 125), (cx, cy-38), 3)

    left_hand = p(42, -13)
    right_hand = p(59, 13)
    line((66, 83, 52), (cx-22, cy-18), left_hand, 15)
    line((66, 83, 52), (cx+22, cy-18), right_hand, 15)

    k = recoil * 8

    if weapon == "Двустволка":
        line((95, 61, 36), p(8-k), p(45-k), 16)
        line((35, 36, 34), p(38-k, -5), p(116-k, -5), 7)
        line((35, 36, 34), p(38-k, 5), p(116-k, 5), 7)
        line((120, 125, 117), p(58-k, -5), p(112-k, -5), 3)
        line((120, 125, 117), p(58-k, 5), p(112-k, 5), 3)

    elif weapon == "Пистолет":
        line((35, 37, 38), p(20-k), p(69-k), 10)
        line((115, 118, 115), p(36-k, -2), p(68-k, -2), 3)
        line((45, 47, 43), p(38-k), p(31-k, 15), 9)

    elif weapon == "Два пистолета":
        for side in (-1, 1):
            line((40, 42, 42), p(20-k, side*17), p(53-k, side*17), 9)
            line((125, 125, 118), p(36-k, side*17-2), p(51-k, side*17-2), 3)
            line((45, 47, 43), p(34-k, side*17), p(29-k, side*17+9), 7)

    elif weapon == "Томпсон":
        line((75, 48, 29), p(10-k), p(42-k), 15)
        line((35, 37, 35), p(35-k), p(105-k), 15)
        line((120, 120, 110), p(55-k, -3), p(104-k, -3), 3)
        line((30, 32, 31), p(62-k), p(70-k, 20), 10)
        mag = p(62-k, 12)
        pygame.draw.ellipse(screen, (25, 27, 26), (mag[0]-8, mag[1]-3, 16, 24))

    elif weapon in ("Автомат", "Лазерная винтовка"):
        body_color = (55, 63, 61) if weapon == "Автомат" else (40, 80, 105)
        line((75, 48, 29), p(10-k), p(35-k), 13)
        line(body_color, p(30-k), p(112-k), 15)
        line((150, 155, 145) if weapon == "Автомат" else (70, 220, 255),
             p(48-k, -5), p(105-k, -5), 3)
        line((30, 32, 31), p(63-k), p(71-k, 18), 9)
        if weapon == "Лазерная винтовка":
            pygame.draw.circle(screen, (70, 220, 255), p(112-k), 5)

    elif weapon == "Дробовик":
        line((95, 61, 36), p(8-k), p(43-k), 16)
        line((35, 36, 34), p(35-k, -4), p(112-k, -4), 10)
        line((135, 140, 130), p(55-k, -4), p(108-k, -4), 3)
        line((55, 45, 34), p(60-k), p(70-k, 17), 9)

    elif weapon == "Снайперка":
        line((75, 48, 29), p(8-k), p(35-k), 13)
        line((35, 39, 40), p(30-k), p(132-k), 12)
        line((135, 140, 145), p(42-k, -3), p(130-k, -3), 3)
        pygame.draw.circle(screen, (30, 30, 30), p(67-k, -7), 7)
        line((45, 47, 43), p(66-k), p(76-k, 17), 8)

    elif weapon == "Миниган":
        line((70, 48, 29), p(8-k), p(35-k), 14)
        line((45, 49, 48), p(32-k), p(110-k), 20)
        for side in (-6, 0, 6):
            line((150, 155, 150), p(52-k, side), p(125-k, side), 3)
        line((30, 32, 31), p(65-k), p(72-k, 20), 10)

    elif weapon == "Плазмопушка":
        line((65, 73, 83), p(8-k), p(105-k), 28)
        line((35, 45, 60), p(82-k), p(127-k), 32)
        pygame.draw.circle(screen, (90, 210, 255), p(110-k), 10)
        line((130, 220, 255), p(45-k, -8), p(90-k, -8), 4)

    elif weapon == "РПГ":
        line((58, 68, 55), p(8-k), p(112-k), 23)
        line((35, 40, 35), p(80-k), p(125-k), 29)
        line((130, 130, 112), p(27-k, -7), p(83-k, -7), 3)
        line((70, 48, 33), p(38-k), p(32-k, 24), 12)

    else:
        line((45, 49, 43), p(8-k), p(108-k), 25)
        line((25, 28, 26), p(92-k), p(124-k), 31)
        line((130, 132, 119), p(29-k, -8), p(84-k, -8), 3)

    # Кисти, перчатки и мелкие металлические детали на оружии.
    for hand in (left_hand, right_hand):
        pygame.draw.circle(screen, (25, 29, 26), hand, 9)
        pygame.draw.circle(screen, (91, 91, 68), hand, 6)
        pygame.draw.line(screen, (150, 148, 115), (hand[0]-3, hand[1]-2), (hand[0]+3, hand[1]+2), 2)
    rail_start, rail_end = p(49-k, -2), p(83-k, -2)
    pygame.draw.line(screen, (180, 185, 177), rail_start, rail_end, 2)
    for rail_t in (0.25, 0.5, 0.75):
        rx = int(rail_start[0] + (rail_end[0]-rail_start[0])*rail_t)
        ry = int(rail_start[1] + (rail_end[1]-rail_start[1])*rail_t)
        pygame.draw.circle(screen, (35, 39, 38), (rx, ry), 2)

    if flash:
        muzzle = p(145-k if weapon in ("РПГ", "Гранатомёт") else 95-k)
        pygame.draw.circle(screen, (255, 90, 15), muzzle, 20)
        pygame.draw.circle(screen, (255, 150, 25), muzzle, 15)
        pygame.draw.circle(screen, (255, 225, 100), muzzle, 9)
        pygame.draw.polygon(screen, (255, 245, 185), [p(85-k, -7), muzzle, p(85-k, 7)])


class Pig:
    def __init__(self, difficulty, px, py, boss=False, boss_type=None):
        self.boss = boss
        self.kind = (boss_type or BOSS_TYPES[0]) if boss else random.choice(
            ["обычный", "быстрый", "броневой", "золотой"]
        )

        angle = random.random() * math.tau
        dist = random.randint(450, 650)
        self.x = px + math.cos(angle) * dist
        self.y = py + math.sin(angle) * dist

        self.attack_timer = 0
        self.flash = 0
        # Таймеры и состояние особых атак боссов.
        self.special_timer = 0
        self.special_until = 0
        self.charge_until = 0
        self.charge_dx = self.charge_dy = 0.0
        self.cloud_x = self.cloud_y = 0.0
        self.cloud_until = 0
        self.cloud_hit_timer = 0
        self.stomp_until = 0
        self.stomp_hit_done = False
        self.fire_trail_until = 0
        self.fire_trail_x = self.fire_trail_y = 0.0
        self.cyber_burst_until = 0
        self.cyber_burst_hit = False
        self.projectile_timer = random.randint(400, 1200)
        self.animation_phase = random.random() * math.tau

        stats = {
            "обычный": (55, 1.25, 1.0, 10, (174, 105, 78), 8),
            "быстрый": (35, 2.5, 0.8, 15, (225, 145, 120), 8),
            "броневой": (120, 0.8, 1.15, 25, (105, 105, 115), 10),
            "золотой": (70, 1.5, 1.0, 60, (255, 195, 25), 8),
            "Король кабанов": (900, 0.65, 2.1, 300, (120, 40, 45), 18),
            "Огненный кабан": (760, 1.15, 1.8, 350, (235, 75, 25), 24),
            "Бронированный титан": (1550, 0.42, 2.55, 450, (105, 115, 130), 30),
            "Ядовитый кабан": (820, 0.9, 1.95, 375, (100, 190, 65), 22),
            "Киберкабан": (1050, 1.35, 1.75, 500, (50, 190, 210), 20),
        }

        hp_value, speed, self.size, self.points, self.color, self.attack_damage = stats[self.kind]
        # Боссы стали крепче и щедрее: награда выше на 25%, здоровье выше на 20%.
        if self.boss:
            hp_value *= 1.20
            self.points = int(round(self.points * 1.25))
            self.attack_damage = int(round(self.attack_damage * 1.10))
        self.hp = hp_value * difficulty[1]
        self.speed = speed * difficulty[2]
        self.max_hp = self.hp
        self.radius = int(24 * self.size)

    def update(self, px, py, now, enemy_projectiles=None, ground_waves=None):
        dx, dy = px-self.x, py-self.y
        dist = max(1, math.hypot(dx, dy))
        ux, uy = dx / dist, dy / dist
        damage_taken = 0

        if self.boss:
            if self.kind == "Король кабанов":
                # Король периодически делает длинный таран.
                if now >= self.special_timer:
                    self.special_timer = now + 3200
                    self.charge_until = now + 720
                    self.charge_dx, self.charge_dy = ux, uy
                if now < self.charge_until:
                    self.x += self.charge_dx * self.speed * 3.2
                    self.y += self.charge_dy * self.speed * 3.2
                else:
                    self.x += ux * self.speed
                    self.y += uy * self.speed

            elif self.kind == "Огненный кабан":
                # Огненный босс быстро бросается на игрока и оставляет вспышку.
                if now >= self.special_timer:
                    self.special_timer = now + 2600
                    self.charge_until = now + 850
                    self.charge_dx, self.charge_dy = ux, uy
                if now < self.charge_until:
                    self.x += self.charge_dx * self.speed * 3.6
                    self.y += self.charge_dy * self.speed * 3.6
                    self.fire_trail_x, self.fire_trail_y = self.x, self.y
                    self.fire_trail_until = now + 650
                else:
                    self.x += ux * self.speed
                    self.y += uy * self.speed

            elif self.kind == "Бронированный титан":
                self.x += ux * self.speed
                self.y += uy * self.speed
                # Мощный удар по земле, если игрок подошёл близко.
                if dist < 235 and now >= self.special_timer:
                    self.special_timer = now + 2900
                    self.stomp_until = now + 650
                    self.stomp_hit_done = False
                if now < self.stomp_until and not self.stomp_hit_done and dist < 330:
                    self.stomp_hit_done = True
                    damage_taken += 38

            elif self.kind == "Ядовитый кабан":
                self.x += ux * self.speed
                self.y += uy * self.speed
                # Ядовитое облако появляется в месте, где стоял игрок.
                if now >= self.special_timer:
                    self.special_timer = now + 3900
                    self.cloud_x, self.cloud_y = px, py
                    self.cloud_until = now + 1750
                if now < self.cloud_until:
                    cloud_dist = math.hypot(px-self.cloud_x, py-self.cloud_y)
                    if cloud_dist < 100 and now >= self.cloud_hit_timer:
                        self.cloud_hit_timer = now + 450
                        damage_taken += 5

            elif self.kind == "Киберкабан":
                # Кибербосс телепортируется в сторону игрока каждые несколько секунд.
                if now >= self.special_timer:
                    self.special_timer = now + 3600
                    angle = random.random() * math.tau
                    self.x = px + math.cos(angle) * 245
                    self.y = py + math.sin(angle) * 245
                    self.special_until = now + 550
                    self.cyber_burst_until = now + 500
                    self.cyber_burst_hit = False
                if now < self.cyber_burst_until and not self.cyber_burst_hit and dist < 190:
                    damage_taken += 18
                    self.cyber_burst_hit = True
                dx, dy = px-self.x, py-self.y
                dist = max(1, math.hypot(dx, dy))
                ux, uy = dx/dist, dy/dist
                self.x += ux * self.speed
                self.y += uy * self.speed
            else:
                self.x += ux * self.speed
                self.y += uy * self.speed
        else:
            self.x += ux * self.speed
            self.y += uy * self.speed

        if self.boss and self.kind == "Огненный кабан" and now < self.fire_trail_until:
            if math.hypot(px-self.fire_trail_x, py-self.fire_trail_y) < 75 and now >= self.attack_timer:
                damage_taken += 8

        # Дальние атаки: обычные броневые кабаны кидают камни, боссы используют
        # собственные типы снарядов. Координаты хранятся в мировом пространстве.
        if enemy_projectiles is not None and now >= self.projectile_timer:
            can_fire = self.boss or self.kind == "броневой"
            if can_fire and dist < 690:
                self.projectile_timer = now + (1050 if self.boss else 2450)
                spread = [-0.16, 0.0, 0.16] if self.kind == "Король кабанов" else [0.0]
                for offset in spread:
                    base_angle = math.atan2(py-self.y, px-self.x) + offset
                    if self.kind == "Ядовитый кабан":
                        shot_color, shot_kind, shot_speed, shot_damage = (110, 240, 70), "poison", 245, 9
                    elif self.kind == "Огненный кабан":
                        shot_color, shot_kind, shot_speed, shot_damage = (255, 100, 25), "fire", 300, 11
                    elif self.kind == "Бронированный титан":
                        shot_color, shot_kind, shot_speed, shot_damage = (190, 200, 210), "rock", 210, 13
                    elif self.kind == "Киберкабан":
                        shot_color, shot_kind, shot_speed, shot_damage = (70, 235, 255), "plasma", 340, 10
                    elif self.kind == "Король кабанов":
                        shot_color, shot_kind, shot_speed, shot_damage = (240, 205, 130), "fang", 285, 8
                    else:
                        shot_color, shot_kind, shot_speed, shot_damage = (165, 150, 120), "rock", 190, 5
                    enemy_projectiles.append({
                        "x": self.x, "y": self.y, "dx": math.cos(base_angle),
                        "dy": math.sin(base_angle), "speed": shot_speed,
                        "damage": shot_damage * (1.25 if self.boss else 1.0),
                        "color": shot_color, "kind": shot_kind,
                        "life": 3.0, "radius": 10 if self.boss else 7
                    })

        if self.boss and self.kind == "Бронированный титан" and now < self.stomp_until:
            if ground_waves is not None and not self.stomp_hit_done:
                ground_waves.append({"x": self.x, "y": self.y, "radius": 24,
                                     "max_radius": 240, "speed": 310,
                                     "damage": 30, "color": (235, 190, 85), "hit": False})
                self.stomp_hit_done = True

        self.flash = max(0, self.flash-1)

        if dist < self.radius+25 and now >= self.attack_timer:
            self.attack_timer = now+850
            damage_taken += self.attack_damage

        return damage_taken

    def draw(self, px, py):
        x = int(WIDTH//2+self.x-px)
        y = int(HEIGHT//2+self.y-py)

        if x < -130 or x > WIDTH+130 or y < -130 or y > HEIGHT+130:
            return

        s = self.size
        c = WHITE if self.flash else self.color

        if self.boss:
            now = pygame.time.get_ticks()
            if self.kind == "Ядовитый кабан" and now < self.cloud_until:
                cloud_sx = int(WIDTH//2 + self.cloud_x - px)
                cloud_sy = int(HEIGHT//2 + self.cloud_y - py)
                pygame.draw.circle(screen, (65, 155, 55), (cloud_sx, cloud_sy), 100, 4)
                pygame.draw.circle(screen, (105, 205, 70), (cloud_sx, cloud_sy), 65, 2)
            if self.kind == "Бронированный титан" and now < self.stomp_until:
                pygame.draw.circle(screen, (230, 190, 75), (x, y), int(100*s), 5)
            if self.kind == "Огненный кабан" and now < self.charge_until:
                pygame.draw.circle(screen, (255, 100, 25), (x, y), int(31*s), 4)
            if self.kind == "Огненный кабан" and now < self.fire_trail_until:
                fx = int(WIDTH//2 + self.fire_trail_x - px)
                fy = int(HEIGHT//2 + self.fire_trail_y - py)
                pygame.draw.circle(screen, (255, 90, 20), (fx, fy), 40, 3)
            if self.kind == "Король кабанов" and now < self.charge_until:
                pygame.draw.circle(screen, (255, 210, 60), (x, y), int(31*s), 4)
            if self.kind == "Киберкабан" and now < self.special_until:
                pygame.draw.circle(screen, (80, 235, 255), (x, y), int(34*s), 4)

        # Мягкая тень, четыре ноги с копытцами и объёмное туловище.
        pygame.draw.ellipse(screen, (24, 27, 25),
                            (x-int(35*s), y+int(18*s), int(70*s), int(20*s)))
        for lx in (-20, -7, 10, 23):
            leg_x = x + int(lx*s)
            pygame.draw.line(screen, (78, 56, 48), (leg_x, y+int(7*s)),
                             (leg_x, y+int(24*s)), max(3, int(6*s)))
            pygame.draw.ellipse(screen, (45, 43, 41),
                                (leg_x-int(4*s), y+int(19*s), max(5, int(9*s)), max(4, int(6*s))))
            pygame.draw.line(screen, (110, 104, 96), (leg_x, y+int(21*s)),
                             (leg_x+int(2*s), y+int(24*s)), max(1, int(s*1.2)))
        pygame.draw.ellipse(screen, (65, 43, 37),
                            (x-int(31*s), y-int(21*s), int(62*s), int(45*s)))
        pygame.draw.ellipse(screen, c,
                            (x-int(29*s), y-int(23*s), int(58*s), int(43*s)))
        pygame.draw.ellipse(screen, tuple(min(255, v+28) for v in c),
                            (x-int(19*s), y-int(18*s), int(31*s), int(29*s)))
        # Щетина и небольшие пятна на спине.
        for i in range(7):
            fx = x + int((i-3)*6*s)
            fy = y - int((19 + (i % 2)*3)*s)
            pygame.draw.line(screen, (55, 48, 45), (fx, fy), (fx+int(2*s), fy-int(5*s)), max(1, int(s)))
        # Уши с внутренней частью.
        pygame.draw.ellipse(screen, (75, 48, 44),
                            (x-int(24*s), y-int(34*s), int(17*s), int(22*s)))
        pygame.draw.ellipse(screen, c,
                            (x-int(23*s), y-int(35*s), int(16*s), int(20*s)))
        pygame.draw.ellipse(screen, (205, 112, 121),
                            (x-int(19*s), y-int(31*s), int(8*s), int(12*s)))
        pygame.draw.ellipse(screen, (75, 48, 44),
                            (x+int(7*s), y-int(34*s), int(17*s), int(22*s)))
        pygame.draw.ellipse(screen, c,
                            (x+int(8*s), y-int(35*s), int(16*s), int(20*s)))
        pygame.draw.ellipse(screen, (205, 112, 121),
                            (x+int(12*s), y-int(31*s), int(8*s), int(12*s)))
        pygame.draw.circle(screen, c, (x, y-int(7*s)), max(8, int(21*s)))
        pygame.draw.ellipse(screen, tuple(max(0, v-18) for v in c),
                            (x-int(16*s), y-int(13*s), int(32*s), int(27*s)))
        # Рыло с двойным бликом и ноздрями.
        pygame.draw.ellipse(screen, (142, 76, 83),
                            (x-int(15*s), y-int(2*s), int(30*s), int(19*s)))
        pygame.draw.ellipse(screen, (242, 157, 164),
                            (x-int(13*s), y-int(1*s), int(26*s), int(14*s)))
        pygame.draw.ellipse(screen, (255, 190, 193),
                            (x-int(8*s), y+int(1*s), int(9*s), max(2, int(4*s))))
        for off in (-6, 6):
            pygame.draw.ellipse(screen, (90, 40, 45),
                               (x+int((off-1)*s), y+int(4*s), max(2, int(3*s)), max(3, int(6*s))))
        # Выразительные глаза с бликом.
        for off in (-9, 9):
            pygame.draw.ellipse(screen, (245, 226, 200),
                               (x+int((off-4)*s), y-int(17*s), max(5, int(9*s)), max(5, int(10*s))))
            pygame.draw.circle(screen, (25, 20, 18),
                               (x+int(off*s)+1, y-int(12*s)), max(2, int(3*s)))
            pygame.draw.circle(screen, WHITE,
                               (x+int((off-1)*s), y-int(14*s)), max(1, int(1.7*s)))
        # Клыки у взрослых кабанов и усиленная броня у соответствующего босса.
        if self.boss or self.kind in ("броневой", "быстрый"):
            for side in (-1, 1):
                tx = x + int(side*13*s)
                pygame.draw.polygon(screen, (238, 226, 184), [
                    (tx, y+int(4*s)), (tx+int(side*7*s), y+int(8*s)),
                    (tx+int(side*3*s), y-int(3*s))])
        if self.boss:
            # Наплечники/пластины и центральный металлический шип.
            pygame.draw.ellipse(screen, (40, 43, 48),
                                (x-int(28*s), y-int(20*s), int(19*s), int(25*s)))
            pygame.draw.ellipse(screen, tuple(min(255, v+45) for v in self.color),
                                (x-int(27*s), y-int(21*s), int(15*s), int(20*s)))
            pygame.draw.ellipse(screen, (40, 43, 48),
                                (x+int(9*s), y-int(20*s), int(19*s), int(25*s)))
            pygame.draw.ellipse(screen, tuple(min(255, v+45) for v in self.color),
                                (x+int(11*s), y-int(21*s), int(15*s), int(20*s)))
            pygame.draw.polygon(screen, (225, 220, 190), [
                (x-int(5*s), y-int(29*s)), (x, y-int(42*s)), (x+int(5*s), y-int(29*s))])

        if self.kind == "золотой":
            pygame.draw.circle(screen, GOLD, (x, y-32), 7)

        if self.boss:
            pygame.draw.circle(screen, self.color, (x, y-int(43*s)), max(5, int(7*s)), 2)
            text(self.kind.upper(), x, y-int(58*s), RED, SMALL, True)

        bw = max(20, int(60*s))
        pygame.draw.rect(screen, (50, 20, 20),
                         (x-bw//2, y-int(40*s), bw, 6))
        pygame.draw.rect(screen, GREEN,
                         (x-bw//2, y-int(40*s),
                          int(bw*max(0, self.hp/self.max_hp)), 6))


def draw_shuriken(x, y, angle, size=23):
    """Рисует металлический восьмиконечный шурикен с вращением."""
    cx, cy = int(x), int(y)
    points = []
    # Восемь внешних и внутренних вершин создают форму звезды.
    for i in range(16):
        a = angle + i * math.pi / 8
        r = size if i % 2 == 0 else size * 0.43
        points.append((int(cx + math.cos(a) * r),
                       int(cy + math.sin(a) * r)))

    shadow = [(px + 2, py + 3) for px, py in points]
    pygame.draw.polygon(screen, (25, 28, 31), shadow)
    pygame.draw.polygon(screen, (75, 83, 91), points)
    pygame.draw.polygon(screen, (205, 215, 222), points, 2)

    inner = []
    for i in range(8):
        a = angle + i * math.pi / 4
        r = size * (0.34 if i % 2 == 0 else 0.18)
        inner.append((int(cx + math.cos(a) * r),
                      int(cy + math.sin(a) * r)))
    pygame.draw.polygon(screen, (135, 150, 160), inner)
    pygame.draw.circle(screen, (45, 115, 155), (cx, cy), max(2, size // 7))
    pygame.draw.circle(screen, (205, 235, 245), (cx, cy), max(1, size // 12))
    # Металлический блик вращается вместе с лезвием.
    hx = int(cx + math.cos(angle - 0.35) * size * 0.68)
    hy = int(cy + math.sin(angle - 0.35) * size * 0.68)
    pygame.draw.circle(screen, (245, 250, 255), (hx, hy), max(1, size // 10))


def main():
    global language_index
    state = "menu"
    difficulty_name = "Нормально"
    difficulty = DIFFICULTIES[difficulty_name]

    px = py = 0.0
    speed = 260
    base_max_hp = difficulty[0]
    hp = max_hp = base_max_hp
    armor_level = 0  # 0 — без брони, 1 — лёгкая, 3 — средняя, 4 — тяжёлая
    points = kills = parts = skill_points = 0

    upgrades = {"damage": 0, "fire_rate": 0, "magazine": 0}
    skills = {key: 0 for key in SKILL_NAMES}

    weapon = "Двустволка"
    owned = {"Двустволка"}
    ammo = WEAPONS[weapon]["ammo"]

    last_shot = reload_until = flash_until = 0
    recoil = 0

    pigs = []
    effects = []
    enemy_projectiles = []
    ground_waves = []
    crates = []
    next_boss = 10
    spawn_timer = 0
    game_over = False

    message = ""
    message_until = 0

    shop_rows = []
    upgrade_rows = []
    skill_rows = []

    ability_cooldowns = {
        "shurikens": 0,
        "berserk": 0,
        "telekinesis": 0,
        "dash": 0,
    }

    berserk_until = 0
    dash_until = 0
    dash_dx = dash_dy = 0

    shuriken_last_hit = {}
    drone_owned = False
    drone_last_shot = 0

    def mag_size(name):
        return max(
            1,
            round(WEAPONS[name]["ammo"] * (1 + .25*upgrades["magazine"]))
        )

    def reset():
        nonlocal px, py, hp, max_hp, base_max_hp, armor_level, points, kills, parts, skill_points
        nonlocal upgrades, skills, weapon, owned, ammo, last_shot
        nonlocal reload_until, flash_until, recoil, pigs, effects
        nonlocal next_boss, spawn_timer, game_over, ability_cooldowns
        nonlocal berserk_until, dash_until, dash_dx, dash_dy
        nonlocal shuriken_last_hit, drone_owned, drone_last_shot
        nonlocal crates, enemy_projectiles, ground_waves

        px = py = 0.0
        base_max_hp = difficulty[0]
        armor_level = 0
        hp = max_hp = base_max_hp
        points = kills = parts = skill_points = 0

        upgrades = {"damage": 0, "fire_rate": 0, "magazine": 0}
        skills = {key: 0 for key in SKILL_NAMES}

        weapon = "Двустволка"
        owned = {"Двустволка"}
        ammo = mag_size(weapon)

        last_shot = reload_until = flash_until = 0
        recoil = 0

        pigs = []
        effects = []
        enemy_projectiles = []
        ground_waves = []
        crates = []
        for _ in range(34):
            crates.append({"x": px + random.randint(-1450, 1450),
                           "y": py + random.randint(-1050, 1050),
                           "kind": random.choices(["ammo", "med", "coins", "parts", "armor"], weights=[24, 23, 22, 18, 13], k=1)[0],
                           "phase": random.random()*math.tau})
        next_boss = 10
        spawn_timer = 0
        game_over = False

        ability_cooldowns = {key: 0 for key in SKILL_NAMES}
        berserk_until = 0
        dash_until = 0
        dash_dx = dash_dy = 0
        shuriken_last_hit = {}
        drone_owned = False
        drone_last_shot = 0

    def choose_weapon(name):
        nonlocal weapon, ammo, reload_until
        weapon = name
        ammo = mag_size(name)
        reload_until = 0

    def weapon_price(name):
        """Цена оружия с учётом выбранной сложности."""
        base_price = WEAPONS[name]["price"]
        if base_price == 0:
            return 0
        return max(1, int(round(base_price * ECONOMY[difficulty_name]["price"] / 10) * 10))

    def buy_weapon(name, now):
        nonlocal points, message, message_until

        price = weapon_price(name)
        if name in owned:
            choose_weapon(name)
            message = "Выбрано: " + name
        elif points >= price:
            points -= price
            owned.add(name)
            choose_weapon(name)
            message = "Куплено: " + name
        else:
            message = f"Не хватает очков! Нужно: {price}"

        message_until = now + 1500

    def remove_dead(now):
        nonlocal hp, max_hp, points, kills, parts, skill_points, next_boss
        nonlocal message, message_until

        for pig in pigs[:]:
            if pig.hp <= 0:
                pigs.remove(pig)
                pig_reward = max(1, int(round(pig.points * ECONOMY[difficulty_name]["reward"])))
                points += pig_reward
                kills += 1
                effects.append([pig.x, pig.y, 12, pig.color])

                if pig.boss:
                    # После победы над боссом здоровье поднимается минимум до 60.
                    hp = min(max_hp, max(hp, 60))
                    bonus = random.randint(2, 4)
                    parts += bonus
                    boss_bonus = int(round(100 * ECONOMY[difficulty_name]["reward"]))
                    points += boss_bonus
                    skill_points += 1

                    message = (
                        f"БОСС ПОБЕЖДЁН! +{pig_reward + boss_bonus} очков, "
                        f"+{bonus} деталей, +1 очко навыка! Здоровье: {int(hp)}"
                    )
                    message_until = now + 3500
                    next_boss = kills + 10

    def shoot(now, mouse):
        nonlocal ammo, last_shot, reload_until, recoil, flash_until

        info = WEAPONS[weapon]
        delay = max(45, int(info["delay"] * .88**upgrades["fire_rate"]))

        if now < berserk_until:
            delay = max(35, int(delay * .65))

        if now < reload_until or now-last_shot < delay:
            return

        if ammo <= 0:
            reload_until = now + info["reload"]
            return

        ammo -= 1
        last_shot = now
        recoil = 1
        flash_until = now + 90

        damage = info["damage"] * (1 + .20*upgrades["damage"])

        # Бонус урона от уровня берсерка: 5%, 10%, 20%.
        berserk_bonus = {1: 0.05, 2: 0.10, 3: 0.20}
        if now < berserk_until:
            damage *= 1 + berserk_bonus.get(skills["berserk"], 0)

        aim = math.atan2(
            mouse[1]-HEIGHT//2,
            mouse[0]-WIDTH//2
        )

        candidates = []

        for pig in pigs:
            sx = WIDTH//2 + pig.x-px
            sy = HEIGHT//2 + pig.y-py
            dx = sx-WIDTH//2
            dy = sy-HEIGHT//2
            dist = math.hypot(dx, dy)

            if dist < 1:
                continue

            angle = math.atan2(dy, dx)
            diff = abs((angle-aim+math.pi) % math.tau-math.pi)

            if diff < .20 and abs(math.sin(diff)*dist) < pig.radius+22:
                candidates.append((dist, pig))

        candidates.sort(key=lambda item: item[0])
        target = candidates[0][1] if candidates else None

        if info["radius"]:
            ix = target.x if target else px+math.cos(aim)*350
            iy = target.y if target else py+math.sin(aim)*350
            effects.append([ix, iy, 18, GOLD])

            for pig in pigs:
                dist = math.hypot(pig.x-ix, pig.y-iy)
                if dist < info["radius"]:
                    pig.hp -= max(10, damage*(1-dist/(info["radius"]*1.5)))
                    pig.flash = 5

        elif target:
            target.hp -= damage
            target.flash = 5

            if weapon == "Два пистолета":
                target.hp -= damage*.35

            if weapon == "Двустволка" and math.hypot(
                target.x-px, target.y-py
            ) < 300:
                target.hp -= damage*.3

        remove_dead(now)

        if ammo <= 0:
            reload_until = now + info["reload"]

    def activate_skill(key, now, mx=0, my=0):
        nonlocal message, message_until
        nonlocal berserk_until, dash_until, dash_dx, dash_dy

        level = skills[key]

        if level <= 0:
            message = "Сначала разблокируй эту способность в меню N!"
            message_until = now + 1800
            return

        if now < ability_cooldowns[key]:
            message = "Способность ещё перезаряжается!"
            message_until = now + 1000
            return

        if key == "shurikens":
            # Шурикены вращаются вокруг игрока постоянно.
            # Кнопка Q активирует их на короткое время.
            ability_cooldowns[key] = now + 5000
            message = "ШУРИКЕНЫ АКТИВНЫ!"
            message_until = now + 1200

        elif key == "berserk":
            ability_cooldowns[key] = now + 15000
            berserk_until = now + 5000
            message = "БЕРСЕРК! УРОН УВЕЛИЧЕН!"
            message_until = now + 1800

        elif key == "telekinesis":
            ability_cooldowns[key] = now + 10000

            visible = []
            for pig in pigs:
                sx = WIDTH//2 + pig.x-px
                sy = HEIGHT//2 + pig.y-py
                if 0 <= sx <= WIDTH and 0 <= sy <= HEIGHT:
                    visible.append(pig)

            if visible:
                target = min(
                    visible,
                    key=lambda pig: math.hypot(pig.x-px, pig.y-py)
                )
                target.hp = 0
                effects.append([target.x, target.y, 18, BLUE])
                remove_dead(now)
                message = "ТЕЛЕКИНЕЗ! Кабанчик уничтожен!"
            else:
                message = "На экране нет кабанчиков!"

            message_until = now + 1800

        elif key == "dash":
            if mx == 0 and my == 0:
                mouse = pygame.mouse.get_pos()
                mx = mouse[0] - WIDTH//2
                my = mouse[1] - HEIGHT//2

            length = math.hypot(mx, my)
            if length < 1:
                return

            dash_dx = mx / length
            dash_dy = my / length
            dash_until = now + 180
            ability_cooldowns[key] = now + 2500

            message = "РЫВОК!"
            message_until = now + 700

    def skill_level_text(key):
        level = skills[key]
        if level == 0:
            return "ЗАКРЫТО"
        if level == 1:
            return "Уровень 1"
        if level == 2:
            return "Уровень 2"
        return "Уровень 3 — МАКС."

    running = True

    while running:
        dt = min(clock.tick(60)/1000, .05)
        now = pygame.time.get_ticks()
        mouse = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        mx = (
            int(keys[pygame.K_d] or keys[pygame.K_RIGHT])
            - int(keys[pygame.K_a] or keys[pygame.K_LEFT])
        )
        my = (
            int(keys[pygame.K_s] or keys[pygame.K_DOWN])
            - int(keys[pygame.K_w] or keys[pygame.K_UP])
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif state == "menu" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    language_index = (language_index + 1) % len(LANGUAGES)
                    pygame.display.set_caption(translate("ОХОТА НА КАБАНЧИКОВ"))
                elif event.key == pygame.K_1:
                    difficulty_name = "Легко"
                elif event.key == pygame.K_2:
                    difficulty_name = "Нормально"
                elif event.key == pygame.K_3:
                    difficulty_name = "Сложно"
                elif event.key == pygame.K_RETURN:
                    difficulty = DIFFICULTIES[difficulty_name]
                    reset()
                    state = "game"

            elif state == "game":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b and not game_over:
                        state = "shop"
                    elif event.key == pygame.K_u and not game_over:
                        state = "upgrade"
                    elif event.key == pygame.K_n and not game_over:
                        state = "skills"
                    elif event.key == pygame.K_r and not game_over:
                        reload_until = now + WEAPONS[weapon]["reload"]
                    elif event.key == pygame.K_q and not game_over:
                        activate_skill("shurikens", now, mx, my)
                    elif event.key == pygame.K_e and not game_over:
                        activate_skill("berserk", now, mx, my)
                    elif event.key == pygame.K_f and not game_over:
                        activate_skill("telekinesis", now, mx, my)
                    elif event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT) and not game_over:
                        activate_skill("dash", now, mx, my)
                    elif event.key == pygame.K_ESCAPE:
                        state = "menu"
                    elif event.key == pygame.K_g and not game_over:
                        if drone_owned:
                            message = "Дрон уже куплен!"
                        elif points >= 3000:
                            points -= 3000
                            drone_owned = True
                            message = "ДРОН КУПЛЕН! Он помогает стрелять."
                        else:
                            message = "Для дрона нужно 3000 очков!"
                        message_until = now + 2200
                    elif event.key == pygame.K_SPACE and game_over:
                        reset()

                elif (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                    and not game_over
                ):
                    shoot(now, mouse)

            elif state == "shop":
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_b, pygame.K_ESCAPE):
                        state = "game"
                    elif event.key == pygame.K_g:
                        if drone_owned:
                            message = "Дрон уже куплен!"
                        elif points >= 3000:
                            points -= 3000
                            drone_owned = True
                            message = "ДРОН КУПЛЕН! Он помогает стрелять."
                        else:
                            message = "Для дрона нужно 3000 очков!"
                        message_until = now + 2200
                    elif pygame.K_1 <= event.key <= pygame.K_9 or event.key == pygame.K_0:
                        idx = 9 if event.key == pygame.K_0 else event.key - pygame.K_1
                        names = list(WEAPONS)
                        if idx < len(names):
                            buy_weapon(names[idx], now)

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for rect, name in shop_rows:
                        if rect.collidepoint(event.pos):
                            buy_weapon(name, now)
                            break

            elif state == "upgrade":
                if event.type == pygame.KEYDOWN and event.key in (
                    pygame.K_u, pygame.K_b, pygame.K_ESCAPE
                ):
                    state = "game"

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for rect, key in upgrade_rows:
                        if rect.collidepoint(event.pos):
                            if parts > 0:
                                parts -= 1
                                upgrades[key] += 1
                                message = "Улучшено: " + UPGRADE_NAMES[key]
                            else:
                                message = "Нужны детали с босса!"
                            message_until = now + 1800
                            break

            elif state == "skills":
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_n, pygame.K_ESCAPE):
                        state = "game"

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for rect, key in skill_rows:
                        if rect.collidepoint(event.pos):
                            if skills[key] == 0:
                                if skill_points > 0:
                                    skill_points -= 1
                                    skills[key] = 1
                                    message = "Разблокировано: " + SKILL_NAMES[key]
                                else:
                                    message = "Нет очков навыков! Победи босса."
                            elif skills[key] < 3:
                                if skill_points > 0:
                                    skill_points -= 1
                                    skills[key] += 1
                                    message = (
                                        SKILL_NAMES[key] + " улучшено до уровня "
                                        + str(skills[key])
                                    )
                                else:
                                    message = "Нет очков навыков!"
                            else:
                                message = "У этой способности максимальный уровень!"

                            message_until = now + 2000
                            break

        if state == "game" and not game_over:
            # Удержание ЛКМ автоматически стреляет из любого выбранного оружия.
            # Скорострельность, патроны и перезарядка по-прежнему задаются оружием.
            if pygame.mouse.get_pressed()[0]:
                shoot(now, mouse)

            if now >= spawn_timer:
                spawn_timer = now + random.randint(650, 1300)
                if len(pigs) < 12:
                    pigs.append(Pig(difficulty, px, py))

            if kills >= next_boss and not any(p.boss for p in pigs):
                boss_index = max(0, kills // 10 - 1) % len(BOSS_TYPES)
                boss_name = BOSS_TYPES[boss_index]
                pigs.append(Pig(difficulty, px, py, True, boss_name))
                message = "ВНИМАНИЕ! " + boss_name.upper() + " ПОЯВИЛСЯ!"
                message_until = now + 2200

            if now < dash_until:
                px += dash_dx * 1150 * dt
                py += dash_dy * 1150 * dt
            elif mx or my:
                length = math.hypot(mx, my)
                px += mx/length * speed * dt
                py += my/length * speed * dt

            for pig in pigs:
                incoming = pig.update(px, py, now, enemy_projectiles, ground_waves)
                armor_reduction = {0: 0.0, 1: 0.10, 3: 0.30, 4: 0.50}.get(armor_level, 0.0)
                hp -= incoming * (1 - armor_reduction)

            # Вражеские снаряды летят к игроку; яд/огонь/плазма имеют свой вид.
            for shot in enemy_projectiles[:]:
                shot["x"] += shot["dx"] * shot["speed"] * dt
                shot["y"] += shot["dy"] * shot["speed"] * dt
                shot["life"] -= dt
                if shot["life"] <= 0:
                    enemy_projectiles.remove(shot)
                    continue
                if math.hypot(shot["x"]-px, shot["y"]-py) < shot["radius"] + 19:
                    armor_reduction = {0: 0.0, 1: 0.10, 3: 0.30, 4: 0.50}.get(armor_level, 0.0)
                    hp -= shot["damage"] * (1 - armor_reduction)
                    effects.append([shot["x"], shot["y"], 8, shot["color"]])
                    enemy_projectiles.remove(shot)

            # Ударная волна титана расширяется по земле и повреждает при пересечении.
            for wave in ground_waves[:]:
                old_radius = wave["radius"]
                wave["radius"] += wave["speed"] * dt
                distance_to_player = math.hypot(px-wave["x"], py-wave["y"])
                if not wave["hit"] and old_radius <= distance_to_player <= wave["radius"] + 10:
                    armor_reduction = {0: 0.0, 1: 0.10, 3: 0.30, 4: 0.50}.get(armor_level, 0.0)
                    hp -= wave["damage"] * (1 - armor_reduction)
                    wave["hit"] = True
                if wave["radius"] >= wave["max_radius"]:
                    ground_waves.remove(wave)

            # Сбор ящиков: аптечка, боеприпасы, монеты или детали для улучшений.
            for crate in crates[:]:
                if math.hypot(crate["x"]-px, crate["y"]-py) < 42:
                    kind = crate["kind"]
                    if kind == "med":
                        hp = min(max_hp, hp + max_hp*0.28)
                        reward_text = "АПТЕЧКА: здоровье восстановлено!"
                        reward_color = GREEN
                    elif kind == "ammo":
                        ammo = mag_size(weapon)
                        reload_until = 0
                        reward_text = "ЯЩИК БОЕПРИПАСОВ: магазин заполнен!"
                        reward_color = BLUE
                    elif kind == "coins":
                        bonus = random.randint(90, 220)
                        points += bonus
                        reward_text = f"ТАЙНИК: +{bonus} монет!"
                        reward_color = GOLD
                    elif kind == "parts":
                        bonus = random.randint(1, 2)
                        parts += bonus
                        reward_text = f"ЯЩИК ДЕТАЛЕЙ: +{bonus} деталей!"
                        reward_color = PURPLE
                    else:
                        # У брони три редкости: уровень 1, 3 и 4.
                        armor_tier = random.choices([1, 3, 4], weights=[55, 30, 15], k=1)[0]
                        armor_data = {
                            1: ("ЛЁГКАЯ", 0.10, (95, 205, 125)),
                            3: ("СРЕДНЯЯ", 0.30, (80, 165, 225)),
                            4: ("ТЯЖЁЛАЯ", 0.50, (205, 175, 95)),
                        }
                        tier_name, bonus_pct, armor_color = armor_data[armor_tier]
                        if armor_tier > armor_level:
                            old_max = max_hp
                            armor_level = armor_tier
                            max_hp = int(round(base_max_hp * (1 + bonus_pct)))
                            hp = min(max_hp, hp + (max_hp - old_max))
                            reward_text = f"БРОНЯ {tier_name}! +{int(bonus_pct*100)}% здоровья и защиты!"
                        else:
                            # Повторно найденная броня чинит текущую броню и лечит.
                            hp = min(max_hp, hp + max(15, int(base_max_hp * bonus_pct * 0.5)))
                            reward_text = f"Броня {tier_name}: запасная пластина восстановила здоровье!"
                        reward_color = armor_color
                    message = reward_text
                    message_until = now + 1900
                    effects.append([crate["x"], crate["y"], 15, reward_color])
                    crates.remove(crate)
                    crates.append({"x": px + random.choice([-1, 1])*random.randint(650, 1400),
                                   "y": py + random.randint(-950, 950),
                                   "kind": random.choices(["ammo", "med", "coins", "parts", "armor"], weights=[24, 23, 22, 18, 13], k=1)[0],
                                   "phase": random.random()*math.tau})

            # Дрон за 3000 очков стреляет по ближайшему кабанчику раз в 0,5 секунды.
            if drone_owned and pigs and now - drone_last_shot >= 500:
                target = min(pigs, key=lambda pig: math.hypot(pig.x-px, pig.y-py))
                drone_last_shot = now
                drone_damage = target.max_hp * (0.04 if target.boss else 0.50)
                target.hp -= drone_damage
                target.flash = 5
                effects.append([target.x, target.y, 8, (70, 220, 255)])
                remove_dead(now)

            hp = max(0, hp)
            if hp <= 0:
                game_over = True

            if reload_until and now >= reload_until:
                ammo = mag_size(weapon)
                reload_until = 0

            # Шурикены вращаются вокруг персонажа.
            # Уровень 1 = один, уровень 2 = два, уровень 3 = три.
            shuriken_level = skills["shurikens"]

            if shuriken_level > 0 and now < ability_cooldowns["shurikens"]:
                count = shuriken_level
                orbit_radius = 65
                angle_speed = now * 0.006

                for i in range(count):
                    angle = angle_speed + i * math.tau / count
                    sx = WIDTH//2 + math.cos(angle)*orbit_radius
                    sy = HEIGHT//2 + math.sin(angle)*orbit_radius

                    world_x = px + math.cos(angle)*orbit_radius
                    world_y = py + math.sin(angle)*orbit_radius

                    for pig in pigs:
                        dist = math.hypot(pig.x-world_x, pig.y-world_y)
                        last = shuriken_last_hit.get(id(pig), 0)

                        if dist < pig.radius + 15 and now-last > 400:
                            pig.hp -= 18 + shuriken_level*7
                            pig.flash = 4
                            shuriken_last_hit[id(pig)] = now

            remove_dead(now)

        background(px, py)

        # Ящики с припасами разбросаны по всей карте и имеют цветную маркировку.
        for crate in crates:
            sx = int(WIDTH//2 + crate["x"] - px)
            sy = int(HEIGHT//2 + crate["y"] - py)
            if -40 <= sx <= WIDTH+40 and -40 <= sy <= HEIGHT+40:
                bob = int(math.sin(now*0.004 + crate["phase"])*3)
                cy = sy + bob
                kind = crate["kind"]
                tint = {"ammo": (75, 175, 230), "med": (75, 210, 115),
                        "coins": (240, 190, 55), "parts": (185, 115, 235),
                        "armor": (205, 175, 95)}[kind]
                pygame.draw.ellipse(screen, (27, 31, 25), (sx-20, cy+12, 40, 10))
                pygame.draw.rect(screen, (36, 40, 42), (sx-17, cy-13, 34, 28), border_radius=4)
                pygame.draw.rect(screen, tint, (sx-15, cy-15, 30, 25), border_radius=3)
                pygame.draw.rect(screen, tuple(max(0, c-55) for c in tint), (sx-15, cy-2, 30, 12))
                pygame.draw.rect(screen, (215, 220, 211), (sx-3, cy-15, 6, 25))
                pygame.draw.rect(screen, (215, 220, 211), (sx-15, cy-4, 30, 5))
                pygame.draw.line(screen, (250, 250, 230), (sx-12, cy-11), (sx-5, cy-11), 2)
                pygame.draw.circle(screen, tint, (sx, cy-22), 4)
                if kind == "armor":
                    # Значок бронепластины на ящике.
                    pygame.draw.polygon(screen, (245, 235, 205), [(sx, cy-10), (sx+8, cy-6), (sx+6, cy+3), (sx, cy+8), (sx-6, cy+3), (sx-8, cy-6)])
                    pygame.draw.line(screen, (95, 90, 75), (sx, cy-6), (sx, cy+4), 2)

        for wave in ground_waves:
            wx, wy = int(WIDTH//2+wave["x"]-px), int(HEIGHT//2+wave["y"]-py)
            pygame.draw.circle(screen, wave["color"], (wx, wy), int(wave["radius"]), 4)
            pygame.draw.circle(screen, (110, 100, 78), (wx, wy), max(2, int(wave["radius"]*0.82)), 2)

        for shot in enemy_projectiles:
            sx, sy = int(WIDTH//2+shot["x"]-px), int(HEIGHT//2+shot["y"]-py)
            color = shot["color"]
            radius = shot["radius"]
            pygame.draw.circle(screen, tuple(max(0, c//3) for c in color), (sx, sy), radius+4)
            pygame.draw.circle(screen, color, (sx, sy), radius)
            pygame.draw.circle(screen, (255, 245, 220), (sx-int(2), sy-int(2)), max(2, radius//3))
            if shot["kind"] == "poison":
                pygame.draw.circle(screen, (170, 255, 95), (sx+radius//2, sy-radius//2), max(2, radius//3))
            elif shot["kind"] == "fire":
                pygame.draw.circle(screen, (255, 220, 80), (sx, sy), max(2, radius//2))
            elif shot["kind"] == "plasma":
                pygame.draw.circle(screen, (220, 255, 255), (sx, sy), radius+5, 2)

        for pig in pigs:
            pig.draw(px, py)

        for effect in effects[:]:
            x, y, life, color = effect
            if life <= 0:
                effects.remove(effect)
            else:
                sx = int(WIDTH//2+x-px)
                sy = int(HEIGHT//2+y-py)
                radius = max(2, (18-life)*3)
                pygame.draw.circle(screen, color, (sx, sy), radius, 3)
                if life > 3:
                    for spark_i in range(6):
                        a = spark_i * math.tau / 6 + life * 0.17
                        inner = radius * 0.45
                        outer = radius + 7
                        p1 = (int(sx + math.cos(a) * inner), int(sy + math.sin(a) * inner))
                        p2 = (int(sx + math.cos(a) * outer), int(sy + math.sin(a) * outer))
                        pygame.draw.line(screen, (255, 235, 150), p1, p2, 2)
                effect[2] -= 1

        if state == "menu":
            text("ОХОТА НА КАБАНЧИКОВ", WIDTH//2, 155, GOLD, BIG, True)
            text("Выбери сложность:", WIDTH//2, 250, WHITE, FONT, True)

            for i, name in enumerate(DIFFICULTIES):
                text(
                    f"{i+1}. {name}", WIDTH//2, 310+i*45,
                    GOLD if name == difficulty_name else WHITE,
                    FONT, True
                )

            text("ENTER — начать", WIDTH//2, 470, GREEN, FONT, True)
            text(
                "WASD — движение | зажми ЛКМ для автострельбы | B — магазин | U — улучшения",
                WIDTH//2, 525, WHITE, SMALL, True
            )
            text(
                "N — навыки | Q — шурикены | E — берсерк | F — телекинез | SHIFT — рывок",
                WIDTH//2, 550, BLUE, SMALL, True
            )
            economy = ECONOMY[difficulty_name]
            text(
                f"Экономика: оружие x{economy['price']:.2f} | награды x{economy['reward']:.2f}",
                WIDTH//2, 575, GOLD, SMALL, True
            )
            text("12 видов оружия и 5 разных боссов!", WIDTH//2, 600, GOLD, SMALL, True)
            text("L — язык: " + LANGUAGES[language_index], WIDTH//2, 625, BLUE, SMALL, True)

        else:
            if state == "game":
                draw_player(mouse, weapon, recoil, now < flash_until)
                if drone_owned:
                    # Дрон летает рядом с игроком и светится перед выстрелом.
                    dx = int(WIDTH//2 + math.cos(now*0.003)*58)
                    dy = int(HEIGHT//2 - 42 + math.sin(now*0.004)*12)
                    pygame.draw.line(screen, (75, 210, 255), (dx-12, dy), (dx+12, dy), 4)
                    pygame.draw.circle(screen, (30, 70, 90), (dx, dy), 13)
                    pygame.draw.circle(screen, (85, 225, 255), (dx, dy), 9, 3)
                    pygame.draw.circle(screen, WHITE, (dx, dy), 3)
                recoil = max(0, recoil-.08)

                # Видимые металлические шурикены поверх игрового мира.
                shuriken_level = skills["shurikens"]
                if shuriken_level > 0 and now < ability_cooldowns["shurikens"]:
                    count = shuriken_level
                    orbit_radius = 85
                    angle_speed = now * 0.006
                    for i in range(count):
                        angle = angle_speed + i * math.tau / count
                        sx = WIDTH // 2 + math.cos(angle) * orbit_radius
                        sy = HEIGHT // 2 + math.sin(angle) * orbit_radius
                        draw_shuriken(sx, sy, angle * 3, 23)

                pygame.draw.rect(screen, (35, 25, 25), (20, 20, 230, 24))
                pygame.draw.rect(
                    screen, GREEN,
                    (20, 20, int(230*hp/max_hp), 24)
                )
                pygame.draw.rect(screen, WHITE, (20, 20, 230, 24), 2)

                text(f"Здоровье: {int(hp)}/{max_hp}", 24, 46, WHITE, SMALL)
                armor_labels = {0: "нет", 1: "лёгкая +10%", 3: "средняя +30%", 4: "тяжёлая +50%"}
                armor_color = {0: WHITE, 1: (95, 205, 125), 3: (80, 165, 225), 4: (205, 175, 95)}.get(armor_level, WHITE)
                text(f"Броня: {armor_labels.get(armor_level, 'нет')}", 20, 286, armor_color, SMALL)
                text(f"Очки: {points}", 20, 70, GOLD)
                text(f"Детали: {parts}", 20, 98, GOLD)
                text(f"Очки навыков: {skill_points}", 20, 126, PURPLE)
                text(f"Убийства: {kills}", 20, 154)
                text(f"Оружие: {weapon}", 20, 182)
                text(f"Патроны: {ammo}/{mag_size(weapon)}", 20, 210)
                text("Дрон: куплен" if drone_owned else "Дрон: G в игре / магазин", 20, 238, BLUE if drone_owned else WHITE, SMALL)
                text("Ящики: аптечки / патроны / монеты / детали / броня", 20, 263, (235, 220, 170), SMALL)

                text("B — магазин | U — улучшения | N — навыки",
                     WIDTH-330, 20, GOLD, SMALL)

                if skills["shurikens"] > 0:
                    text(
                        f"Шурикены: уровень {skills['shurikens']}",
                        WIDTH-280, 48, PURPLE, SMALL
                    )

                if now < berserk_until:
                    text(
                        f"БЕРСЕРК! УРОН +"
                        f"{int({1: 5, 2: 10, 3: 20}.get(skills['berserk'], 0))}%",
                        WIDTH//2, 65, GOLD, FONT, True
                    )

                if reload_until > now:
                    text("ПЕРЕЗАРЯДКА...", WIDTH//2, 95, GOLD, FONT, True)

                if now < message_until:
                    text(message, WIDTH//2, 125, GOLD, FONT, True)

                # Перезарядка способностей
                y = 255
                for key, label in [
                    ("shurikens", "Q — Шурикены"),
                    ("berserk", "E — Берсерк"),
                    ("telekinesis", "F — Телекинез"),
                    ("dash", "SHIFT — Рывок"),
                ]:
                    level = skills[key]
                    if level == 0:
                        status = "ЗАКРЫТО"
                        color = RED
                    else:
                        remaining = max(
                            0, (ability_cooldowns[key]-now)/1000
                        )
                        status = "ГОТОВО" if remaining == 0 else f"{remaining:.1f} с"
                        color = GREEN if remaining == 0 else RED

                    text(label, 20, y, WHITE, SMALL)
                    text(status, 180, y, color, SMALL)
                    y += 23

                text(
                    "WASD — движение | ЛКМ — огонь | R — перезарядка",
                    WIDTH//2, HEIGHT-42, WHITE, SMALL, True
                )

                if game_over:
                    pygame.draw.rect(screen, (20, 20, 25), (250, 210, 500, 220))
                    pygame.draw.rect(screen, RED, (250, 210, 500, 220), 3)
                    text("ТЫ ПРОИГРАЛ!", WIDTH//2, 260, RED, BIG, True)
                    text(
                        f"Убийств: {kills} | Очков: {points}",
                        WIDTH//2, 325, WHITE, FONT, True
                    )
                    text("SPACE — начать заново", WIDTH//2, 380, GOLD, FONT, True)

            elif state == "shop":
                pygame.draw.rect(
                    screen, (22, 25, 31), (110, 25, 780, 600),
                    border_radius=10
                )
                text("МАГАЗИН ОРУЖИЯ", WIDTH//2, 58, GOLD, BIG, True)
                shop_rows = []
                y = 91

                for i, (name, info) in enumerate(WEAPONS.items(), 1):
                    rect = pygame.Rect(145, y, 710, 37)
                    shop_rows.append((rect, name))
                    pygame.draw.rect(screen, (55, 63, 68), rect, border_radius=5)

                    text(f"{i}. {name}", 158, y+3, WHITE, SMALL)
                    text(
                        f"Урон {info['damage']} | магазин {info['ammo']} | перезарядка {info['reload']/1000:.1f}с",
                        390, y+10, WHITE, SMALL
                    )

                    status = "КУПЛЕНО" if name in owned else f"{weapon_price(name)} очков"
                    text(
                        status, 795, y+10,
                        GREEN if name in owned else GOLD, SMALL, True
                    )
                    y += 42

                text(f"Очки: {points} | G — дрон за 3000 очков ({'КУПЛЕН' if drone_owned else 'не куплен'}) | B — закрыть",
                     WIDTH//2, 600, GOLD, SMALL, True)

            elif state == "upgrade":
                pygame.draw.rect(
                    screen, (22, 25, 31), (190, 65, 620, 540),
                    border_radius=10
                )
                text("МОДЕРНИЗАЦИЯ", WIDTH//2, 100, GOLD, BIG, True)
                text(f"Детали босса: {parts}", WIDTH//2, 145, WHITE, FONT, True)

                upgrade_rows = []
                y = 190
                desc = {
                    "damage": "Урон +20% за уровень",
                    "fire_rate": "Стрельба быстрее на 12%",
                    "magazine": "Магазин больше на 25%",
                }

                for key, title in UPGRADE_NAMES.items():
                    rect = pygame.Rect(225, y, 550, 90)
                    upgrade_rows.append((rect, key))
                    pygame.draw.rect(screen, (45, 53, 60), rect, border_radius=7)
                    text(f"{title} — уровень {upgrades[key]}", 245, y+12)
                    text(desc[key], 245, y+48, WHITE, SMALL)
                    text("1 деталь", 720, y+32, GOLD, SMALL, True)
                    y += 105

                text("Нажми на улучшение | U — закрыть",
                     WIDTH//2, 545, WHITE, SMALL, True)

            elif state == "skills":
                pygame.draw.rect(
                    screen, (22, 25, 31), (110, 35, 780, 585),
                    border_radius=10
                )

                text("ДЕРЕВО НАВЫКОВ", WIDTH//2, 68, GOLD, BIG, True)
                text(
                    f"Очки навыков: {skill_points}",
                    WIDTH//2, 108, PURPLE, FONT, True
                )
                text(
                    "Нажми на навык: открыть — 1 очко, улучшить — 1 очко",
                    WIDTH//2, 137, WHITE, SMALL, True
                )

                skill_rows = []
                y = 165

                for key, name in SKILL_NAMES.items():
                    rect = pygame.Rect(155, y, 690, 95)
                    skill_rows.append((rect, key))

                    level = skills[key]
                    unlocked = level > 0

                    pygame.draw.rect(
                        screen,
                        (48, 65, 72) if unlocked else (48, 42, 45),
                        rect,
                        border_radius=8
                    )

                    pygame.draw.rect(
                        screen,
                        GREEN if unlocked else RED,
                        rect, 2, border_radius=8
                    )

                    text(name, 175, y+8, GOLD if unlocked else WHITE)
                    text(SKILL_DESCRIPTIONS[key], 175, y+37, WHITE, SMALL)
                    text(skill_level_text(key), 175, y+64,
                         GREEN if unlocked else RED, SMALL)

                    if level == 0:
                        action = "ОТКРЫТЬ — 1 очко"
                    elif level < 3:
                        action = "УЛУЧШИТЬ — 1 очко"
                    else:
                        action = "МАКСИМУМ"

                    text(action, 725, y+38, GOLD, SMALL, True)
                    y += 105

                text(
                    "N — закрыть | Очки выдаются за победу над боссом",
                    WIDTH//2, 590, WHITE, SMALL, True
                )

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()