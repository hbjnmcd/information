import pygame
import sys
import random
from player import Player
from static_object import StaticObject
import res  # Импортируем файл с путями к изображениям
from subjects import Apple

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 30
MAP_WIDTH, MAP_HEIGHT = 1400, 1100

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Приключения Алисы")
        self.clock = pygame.time.Clock()
        self.player = Player(res.alice)
        self.static_objects = []
        self.camera_offset = [WIDTH // 2, HEIGHT // 2]
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False

        self.apples = pygame.sprite.Group()
        self.apple_count = 0
        self.apples_collected = 0
        self.create_apples(10)

        self.font = pygame.font.Font(None, 36)

        self.dialog_active = False
        self.current_dialog = ""
        self.interactable_objects = ['friend_girl', 'friend_man', 'old_man']
        self.dialog_trigger_range = 20

        self.dialogues = {
            "old_man": [
                "Привет, молодая леди! Как ты сегодня?",
                "Здесь много интересных мест, не правда ли?",
                "Береги себя, Алиса!"
            ],
            "friend_man": [
                "Эй, Алиса! Давно не виделись!",
                "Слышала, что Анджела учудила?.",
                "Как твои дела?"
            ],
            "friend_girl": [
                "Привет, Алиса! Как поживаешь?",
                "Я слышала, ты собираешь яблоки!",
                "Не забудь рассказать мне о своих приключениях!"
            ]
        }
        self.game_over = False

        # Создаем статичные объекты
        self.create_static_objects()
        self.create_interactive_objects()

    def create_interactive_objects(self):
        # Генерация случайных интерактивных объектов
            self.add_interactive_object(res.old_man, 118, 151, "old_man")
            self.add_interactive_object(res.friend_girl, 115, 151, "friend_girl")
            self.add_interactive_object(res.friend_man, 73, 151, "friend_man")

    def add_interactive_object(self, image_path, object_width, object_height, name):
        position = self.generate_random_position(object_width, object_height)
        new_object = StaticObject(image_path, position, interactive=True, name=name)
        self.static_objects.append(new_object)

    def create_static_objects(self):
        for _ in range(3):
            self.add_static_object(res.tree2, 250, 239)  # Размеры дерева (ширина, высота)
        for _ in range(2):
            self.add_static_object(res.bush, 108, 100)  # Размеры куста (ширина, высота)
        for _ in range(5):
            self.add_static_object(res.flower, 20, 22)  # Размеры куста (ширина, высота)

        self.add_static_object(res.alices_house, 326, 300)
        self.add_static_object(res.barn, 372, 300)

    def add_static_object(self, image_path, object_width, object_height):
        position = self.generate_random_position(object_width, object_height)
        new_object = StaticObject(image_path, position)
        self.static_objects.append(new_object)

    def generate_random_position(self, object_width, object_height):
        while True:
            x = random.randint(0, MAP_WIDTH - object_width)
            y = random.randint(0, MAP_HEIGHT - object_height)
            if not self.is_position_occupied(x, y, object_width, object_height):
                return x, y

    def is_position_occupied(self, x, y, object_width, object_height):
        for static_object in self.static_objects:
            if (x < static_object.rect.x + static_object.rect.width and
                    x + object_width > static_object.rect.x and
                    y < static_object.rect.y + static_object.rect.height and
                    y + object_height > static_object.rect.y):
                return True
        return False

    def create_apples(self, count):
        for _ in range(count):
            apple = Apple()
            print(f"Создано яблоко на позиции: {apple.rect.x}, {apple.rect.y}")
            # Проверка на пересечение с статичными объектами
            while self.check_collision_with_static_objects(apple):
                apple = Apple()  # Создаем новое яблоко, если есть пересечение
                print(f'у яблока {_} пересечение, сейчас создам новое, координаты {apple.rect.x}, {apple.rect.y}')
            self.apples.add(apple)

    def check_collision_with_static_objects(self, apple):
        # Проверка на пересечение с статическими объектами
        for static_object in self.static_objects:
            if apple.rect.colliderect(static_object.rect):
                return True
        return False

    def collect_apple(self):
        self.apple_count += 1
        if self.apple_count >= 10:
            self.game_over = True

    # Добавление для диалога
    def check_interaction(self):
        for obj in self.static_objects:
            if obj.interactive:  # Проверяем, является ли объект интерактивным
                if self.player.rect.colliderect(obj.rect.inflate(self.dialog_trigger_range, self.dialog_trigger_range)):
                    return obj  # Возвращаем объект, с которым можно взаимодействовать
        return None

    # Добавление для диалога
    def draw_dialog(self):
        if self.dialog_active:
            dialog_rect = pygame.Rect(0, HEIGHT - 100, WIDTH, 100)
            pygame.draw.rect(self.screen, (0, 0, 0), dialog_rect)

            # Отображение основного текста диалога
            self.render_multiline_text(self.current_dialog, self.font, (255, 255, 255), dialog_rect)

            # Добавляем текст для выхода из диалога
            exit_text = self.font.render("Для выхода нажмите ESC", True, (255, 255, 255))
            self.screen.blit(exit_text, (450, HEIGHT - 30))  # Позиция текста

    def render_multiline_text(self, text, font, color, rect):
        lines = []
        words = text.split(' ')
        current_line = ''

        for word in words:
            test_line = current_line + word + ' '
            test_surface = font.render(test_line, True, color)
            if test_surface.get_width() > rect.width:
                lines.append(current_line)
                current_line = word + ' '
            else:
                current_line = test_line
        lines.append(current_line)  # Добавляем последнюю строку

        for i, line in enumerate(lines):
            line_surface = font.render(line, True, color)
            self.screen.blit(line_surface, (rect.x + 10, rect.y + 10 + i * (font.get_height() + 5)))  # Отступы

    def draw_background(self):
        # Заполнение фона зеленым цветом (трава)
        self.screen.fill((0, 128, 0))  # Зеленый цвет

    def _check_events(self):
        # Отслеживание событий клавиатуры и мыши.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if not self.dialog_active:  # Проверяем, активен ли диалог
                    self._check_keydown_events(event)
                else:
                    if event.key == pygame.K_ESCAPE:  # Закрытие диалога
                        self.dialog_active = False
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.moving_left = True
        elif event.key == pygame.K_UP:
            self.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.moving_down = True
        # добавление для диалога
        elif event.key == pygame.K_e and self.check_interaction():
            interactive_object = self.check_interaction()
            if interactive_object:
                self.dialog_active = True
                character_name = interactive_object.name  # Предполагается, что у объекта есть атрибут name
                self.current_dialog = random.choice(self.dialogues[character_name])
        elif event.key == pygame.K_ESCAPE:  # Например, нажмите ESC для выхода из диалога
            self.dialog_active = False
        elif event.key == pygame.K_r and self.game_over:
            self.reset_game()

        elif event.key == pygame.K_q:
            pygame.quit()
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.moving_left = False
        elif event.key == pygame.K_UP:
            self.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.moving_down = False

    def update_player(self):
        if self.game_over:  # Если игра завершена, выходим из метода
            return
        dx, dy = 0, 0
        if not self.dialog_active:  # Проверяем, активен ли диалог
            if self.moving_right:
                dx += 10
            if self.moving_left:
                dx -= 10
            if self.moving_up:
                dy -= 10
            if self.moving_down:
                dy += 10
        # Обновление позиции игрока в зависимости от состояния флагов

        # Обновляем позицию игрока
        self.player.move(dx, dy)

        # Ограничиваем движение игрока в пределах карты
        self.player.rect.x = max(0, min(self.player.rect.x, MAP_WIDTH - self.player.rect.width))
        self.player.rect.y = max(0, min(self.player.rect.y, MAP_HEIGHT - self.player.rect.height))

        # Обновляем смещение камеры
        self.camera_offset[0] = self.player.rect.centerx - WIDTH // 2
        self.camera_offset[1] = self.player.rect.centery - HEIGHT // 2

        # Ограничиваем смещение камеры в пределах карты
        self.camera_offset[0] = max(0, min(self.camera_offset[0], MAP_WIDTH - WIDTH))
        self.camera_offset[1] = max(0, min(self.camera_offset[1], MAP_HEIGHT - HEIGHT))

    def _check_apple_collisions(self):
        collisions = pygame.sprite.spritecollide(self.player, self.apples, True)  # Удаляем собранные яблоки
        for apple in collisions:
            self.collect_apple()

            print(f"Собрано яблоко! Всего яблок: {self.apple_count}")
            print(f"Яблоко собрано на позиции: {apple.rect.x}, {apple.rect.y}")

    def draw_score(self):
        # Отображение счетчика собранных яблок
        score_text = self.font.render(f"Собрано яблок: {self.apple_count}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))  # Рисуем текст в верхнем левом углу

    def draw_game_over_message(self):
        font = pygame.font.Font(None, 74)  # Шрифт для сообщения
        game_over_text = font.render("Вы собрали все яблоки!", True, (255, 255, 255))
        restart_text = font.render("Начать новую игру? (R)", True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))

        # Рассчитываем размеры большого прямоугольника
        rect_width = max(game_over_rect.width, restart_rect.width) + 40  # Ширина прямоугольника с отступами
        rect_height = game_over_rect.height + restart_rect.height + 60  # Высота прямоугольника с отступами
        rect_x = (WIDTH - rect_width) // 2  # Центрируем по X
        rect_y = (HEIGHT - rect_height) // 2  # Центрируем по Y

        # Рисуем черный прямоугольник
        pygame.draw.rect(self.screen, (0, 0, 0), (rect_x, rect_y, rect_width, rect_height))

        # Отображаем тексты внутри прямоугольника
        game_over_text_rect = game_over_text.get_rect(center=(WIDTH // 2, rect_y + rect_height // 2 - 20))
        restart_text_rect = restart_text.get_rect(center=(WIDTH // 2, rect_y + rect_height // 2 + 20))

        self.screen.blit(game_over_text, game_over_text_rect)  # Отображаем первый текст
        self.screen.blit(restart_text, restart_text_rect)  # Отображаем второй текст

    def reset_game(self):
        self.apple_count = 0  # Сбрасываем счетчик яблок
        self.apples.empty()  # Очищаем группу яблок
        self.create_apples(10)  # Создаем новые яблоки
        self.static_objects.clear()  # Очищаем статичные объекты
        self.create_static_objects()
        self.interactable_objects.clear()  # Очищаем статичные объекты
        self.create_interactive_objects()
        self.game_over = False  # Сбрасываем состояние игры

    def run_game(self):
        game_over = False

        while not game_over:
            self._check_events()
            self.update_player()  # Обновляем позицию игрока
            self._check_apple_collisions()

            # Рендеринг
            self.draw_background()  # Рисуем фон

            # Рисуем статичные объекты
            for obj in self.static_objects:
                obj.draw(self.screen, self.camera_offset)

            for apple in self.apples:
                screen_x = apple.rect.x - self.camera_offset[0]
                screen_y = apple.rect.y - self.camera_offset[1]
                self.screen.blit(apple.image, (screen_x, screen_y))

            # Отрисовка игрока
            self.player.draw(self.screen, self.camera_offset)

            # Отображение счета
            self.draw_score()
            # Добавление для диалога

            if self.check_interaction():
                interaction_text = self.font.render("'E'", True, (255, 255, 255))
                self.screen.blit(interaction_text, (WIDTH - 50, 10))

            self.draw_dialog()

            if self.game_over:
                self.draw_game_over_message()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run_game()

