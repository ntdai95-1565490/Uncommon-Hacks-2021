import sys
from os import path
import pygame as pg
import random
import pickle
from settings import *
from sprites import *

class PickleHighScore:
    def __init__(self, list_of_highscores):
        self.list_of_highscores = list_of_highscores


    def saving_highscore_pickle(self):
        with open(".highscores.pickle", "wb") as p:
            pickle.dump(self.list_of_highscores, p)


class Main:
    def __init__(self):
        pg.init()
        pg.mixer.music.load(path.join(path.join(path.dirname(__file__), "Music"), "background_music.wav"))
        pg.mixer.music.set_volume(0.4)
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background = pg.image.load(path.join(path.join(path.dirname(__file__), "Images"), "background.png")).convert_alpha()
        self.background_x = 0
        self.background_x_2 = self.background.get_width()
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.reset()


    def reset(self):
        self.game_open = True
        self.game_over = False
        self.instruction_page = False
        self.highscores_page = False
        self.game_running = False
        self.is_music_playing = False
        self.list_of_button_texts = ["START GAME", "INSTRUCTIONS", "HIGHSCORES", "MUSIC ON/OFF", "EXIT GAME"]
        self.list_of_button_positions_x = None
        self.list_of_button_positions_y = None
        self.buttons_size_x = None
        self.buttons_size_y = None
        self.mouse_position = None
        self.round_count = 0
        self.list_of_highscores = []
        self.final_player_score_in_highscores = None
        self.player_name = ""


### GAME START SCREEN ###


    def game_start_screen(self):
        pg.mixer.music.play(-1)
        while self.game_open:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game_open = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    for i in range(5):
                        if i == 0 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y: 
                            self.game_running = True
                        elif i == 1 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            self.instruction_page = True
                        elif i == 2 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            self.highscores_page = True
                        elif i == 3 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            if self.is_music_playing:
                                pg.mixer.music.stop()
                                self.is_music_playing = False
                            else:
                                pg.mixer.music.play(-1)
                                self.is_music_playing = True
                        elif i == 4 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            self.game_open = False
            
            self.run_main_game()
            self.instructions_screen_page()
            self.highscores_screen()
            if self.game_open:
                self.screen.blit(self.background, (0, 0))
                self.initial_message_to_screen(self.screen)
                self.loading_buttons_on_first_page(self.screen, self.mouse_position, self.list_of_button_texts)

            pg.display.update()
            self.clock.tick(FPS)

        pg.quit()
        sys.exit()

    def initial_message_to_screen(self, screen):
        line_font = pg.font.Font('freesansbold.ttf', 60)
        line = line_font.render("Welcome to KoronaKiller!", True, YELLOW)
        line_surface = pg.Surface(line.get_size())
        line_surface.fill(BLACK)
        line_surface.blit(line, (0, 0))
        self.screen.blit(line_surface, (400, 150))

    def loading_buttons_on_first_page(self, screen, mouse_position, list_of_button_texts):
        self.mouse_position = pg.mouse.get_pos()
        self.list_of_button_positions_x = [100, 575, 1050, 300, 850]
        self.list_of_button_positions_y = [350, 350, 350, 550, 550]
        self.buttons_size_x = 350
        self.buttons_size_y = 100

        # Button Texts
        for i in range(5):
            if self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y: 
                pg.draw.rect(self.screen, RED, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y])
                pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y], 5)
            else: 
                pg.draw.rect(self.screen, GREEN, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y])
                pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y], 5)

            font = pg.font.Font('freesansbold.ttf', 40)
            text_font = font.render(self.list_of_button_texts[i], True, BLACK)
            text_font_width = text_font.get_width()
            text_font_height = text_font.get_height()
            self.screen.blit(text_font, (self.list_of_button_positions_x[i] + (self.buttons_size_x - text_font_width) // 2, self.list_of_button_positions_y[i] + (self.buttons_size_y - text_font_height) // 2))


### HIGHSCORES PAGE ###


    def highscores_screen(self):
        if self.highscores_page:
            try:
                with open(".highscores.pickle", "rb") as p:
                    pickle_objects = pickle.load(p)
                self.list_of_highscores = pickle_objects
                self.list_of_highscores.sort(reverse = True, key = lambda x: x[1])
            except EOFError:
                self.list_of_highscores = []

        while self.highscores_page:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.highscores_page = False
                    self.game_open = False
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    for i in range(4):
                        if i == 0 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            self.list_of_highscores = []
                            instance_of_PickleHighScore = PickleHighScore(self.list_of_highscores)
                            instance_of_PickleHighScore.saving_highscore_pickle()
                        elif i == 2 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            self.highscores_page = False

            self.screen.blit(self.background, (0, 0))
            self.highscores_message_to_screen(self.screen)
            self.loading_buttons_on_highscores_page(self.screen, self.mouse_position, self.list_of_button_texts, self.buttons_size_x, self.buttons_size_y)

            if self.highscores_page == False and self.game_open:
                self.reset()

            pg.display.update()
            self.clock.tick(FPS)

    def highscores_message_to_screen(self, screen):
        first_line_font = pg.font.Font('freesansbold.ttf', 60)
        line_font = pg.font.Font('freesansbold.ttf', 40)
        list_of_messages = ["TOP 10 HIGHSCORES!"]
        for index, name_score in enumerate(self.list_of_highscores):
            name_score_message = f"{index + 1}. {name_score[0]} --> {name_score[1]} points"
            list_of_messages.append(name_score_message)
        for index, message in enumerate(list_of_messages):
            if index == 0:
                line = first_line_font.render(message, True, BLACK)
            else:
                line = line_font.render(message, True, BLACK)
            line_surface = pg.Surface(line.get_size())
            line_surface.fill(YELLOW)
            line_surface.blit(line, (0, 0))
            if index == 0:
                self.screen.blit(line_surface, (470, 20))
            elif index < 6:
                self.screen.blit(line_surface, (60, 60 + 100 * index))  
            else:
                self.screen.blit(line_surface, (800, 60 + 100 * (index - 5)))

    def loading_buttons_on_highscores_page(self, screen, mouse_position, list_of_button_texts, buttons_size_x, buttons_size_y):
        self.mouse_position = pg.mouse.get_pos()
        self.list_of_button_texts = ["DELETE", "ALL SCORES", "MAIN", "PAGE"]
        self.list_of_button_positions_x = [450, 450, 750, 750]
        self.list_of_button_positions_y = [665, 705, 665, 705]
        self.buttons_size_x = 290
        self.buttons_size_y = 110

        # Button Texts
        for i in range(4):
            if i % 2 == 0 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y: 
                pg.draw.rect(self.screen, RED, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y])
                pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y], 5)
            elif i % 2 == 0: 
                pg.draw.rect(self.screen, GREEN, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y])
                pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y], 5)

            font = pg.font.Font('freesansbold.ttf', 40)
            text_font = font.render(self.list_of_button_texts[i], True, BLACK)
            text_font_width = text_font.get_width()
            text_font_height = text_font.get_height()
            self.screen.blit(text_font, (self.list_of_button_positions_x[i] + (self.buttons_size_x - text_font_width) // 2, self.list_of_button_positions_y[i] + (self.buttons_size_y - text_font_height) // 4))


### INSTRUCTIONS PAGE ###


    def instructions_screen_page(self):
        while self.instruction_page:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.instruction_page = False
                    self.game_open = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    for i in range(2):
                        if i == 0 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            self.instruction_page = False

            self.screen.blit(self.background, (0, 0))
            self.instruction_message_to_screen(self.screen)
            self.loading_buttons_on_instruction_page(self.screen, self.mouse_position, self.list_of_button_texts, self.buttons_size_x, self.buttons_size_y)

            if self.instruction_page == False and self.game_open:
                self.reset()

            pg.display.update()
            self.clock.tick(FPS)
    
    def instruction_message_to_screen(self, screen):
        first_line_font = pg.font.Font('freesansbold.ttf', 60)
        line_font = pg.font.Font('freesansbold.ttf', 50)
        list_of_messages = ["Instructions!", 
                            "To move around, use the left, right, and up arrows to move",
                            "left, right, and jump. Press space to shoot vaccine to the",
                            "viruses. If a virus touches you, you will get one life point",
                            "deducted, but if a face mask touches you, you will get one",
                            "extra life point.",
                            "For every virus that touches you, you will get one point",
                            "deducted, but you will get 5 point for every virus that",
                            "you kill with the vaccine. You will get 3 point for every",
                            "face mask that touches you as well."]

        for index, message in enumerate(list_of_messages):
            if index == 0:
                line = first_line_font.render(message, True, BLACK)
            else:
                line = line_font.render(message, True, BLACK)
            line_surface = pg.Surface(line.get_size())
            line_surface.fill(YELLOW)
            line_surface.blit(line, (0, 0))
            if index == 0:
                self.screen.blit(line_surface, (580, 20))
            elif index < 6:
                self.screen.blit(line_surface, (20, 100 + 50 * index))
            else:
                self.screen.blit(line_surface, (20, 120 + 50 * index))

    def loading_buttons_on_instruction_page(self, screen, mouse_position, list_of_button_texts, buttons_size_x, buttons_size_y):
        self.mouse_position = pg.mouse.get_pos()
        self.list_of_button_texts = ["MAIN", "PAGE"]
        self.list_of_button_positions_x = [650, 650]
        self.list_of_button_positions_y = [665, 705]
        self.buttons_size_x = 170
        self.buttons_size_y = 110

        # Button Texts
        for i in range(2):
            if i % 2 == 0 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y: 
                pg.draw.rect(self.screen, RED, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y])
                pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y], 5)
            elif i % 2 == 0: 
                pg.draw.rect(self.screen, GREEN, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y])
                pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y], 5)

            font = pg.font.Font('freesansbold.ttf', 40)
            text_font = font.render(self.list_of_button_texts[i], True, BLACK)
            text_font_width = text_font.get_width()
            text_font_height = text_font.get_height()
            self.screen.blit(text_font, (self.list_of_button_positions_x[i] + (self.buttons_size_x - text_font_width) // 2, self.list_of_button_positions_y[i] + (self.buttons_size_y - text_font_height) // 4))


### MAIN GAME ###


    def loading_sprites_main_game(self, screen):
        self.all_sprites_group = pg.sprite.Group()
        self.player = Player()
        self.all_sprites_group.add(self.player)
        self.vaccine = Vaccine()
        self.all_sprites_group.add(self.vaccine)
        self.mask = Mask()
        self.all_sprites_group.add(self.mask)
        self.enemies = []
        for i in range(3):
            instance_of_Virus = Virus(i)
            self.enemies.append(instance_of_Virus)
            self.all_sprites_group.add(instance_of_Virus)

    def run_main_game(self):
        if self.game_running:
            self.loading_sprites_main_game(self.screen)
        while self.game_running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game_running = False
                    self.game_open = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.game_running = False
                    if event.key == pg.K_LEFT:
                        self.player.player_move_horizontal = "LEFT"
                    if event.key == pg.K_RIGHT:
                        self.player.player_move_horizontal = "RIGHT"
                    if event.key == pg.K_UP:
                        self.player.player_move_vertical = "UP"
                    if event.key == pg.K_SPACE:
                        if self.vaccine.vaccine_is_on == False:
                            self.vaccine.vaccine_is_on = True
                            self.vaccine.rect.x = self.player.rect.x
                            self.vaccine.rect.y = self.player.rect.y
        
                if event.type == pg.KEYUP:
                    if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                        self.player.player_move_horizontal = None
                    if event.key == pg.K_UP:
                        self.player.player_move_vertical = None 

            self.update_main_game()
            self.draw_main_game()

            if self.player.player_life_point < 1:
                self.game_over = True
                self.game_over_screen()

            pg.display.update()
            self.clock.tick(FPS)

    def draw_main_game(self):
        self.background_x += -1
        self.background_x_2 += -1

        if self.background_x < -self.background.get_width():
            self.background_x = self.background.get_width()
        if self.background_x_2 < -self.background.get_width():
            self.background_x_2 = self.background.get_width()

        self.screen.blit(self.background, (self.background_x, 0))
        self.screen.blit(self.background, (self.background_x_2, 0))

        self.message_to_main_game_screen(self.screen)
        self.draw_health_bar_player(self.screen)
        self.all_sprites_group.draw(self.screen)

    def draw_health_bar_player(self, screen):
        BAR_LENGTH = 140
        BAR_HEIGHT = 30
        fill = (self.player.player_life_point / 5) * BAR_LENGTH
        outline_rect = pg.Rect(10, 60, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(10, 60, fill, BAR_HEIGHT)
        pg.draw.rect(self.screen, GREEN, fill_rect)
        pg.draw.rect(self.screen, BLACK, outline_rect, 5)

    def message_to_main_game_screen(self, screen):
        line_font = pg.font.Font('freesansbold.ttf', 40)
        list_of_texts = ["Health:", f"Score: {self.player.player_score}"]
        for i, text in enumerate(list_of_texts): 
            line = line_font.render(text, True, YELLOW)
            line_surface = pg.Surface(line.get_size())
            line_surface.fill(BLACK)
            line_surface.blit(line, (0, 0))
            self.screen.blit(line_surface, (10, 10 + 100 * i))

    def update_main_game(self):
        if self.player.player_score % 10 == 0:
            self.mask.appear = True
        self.collision_detection()
        self.all_sprites_group.update()

    def collision_detection(self):
        for virus in self.enemies:
            if pg.sprite.collide_mask(self.player, virus):
                virus.rect.x = random.randint(1500, 1800)
                virus.rect.y = random.randint(100, 550)
                self.player.player_life_point -= 1
                self.player.player_score -= 1

        for virus in self.enemies:
            if pg.sprite.collide_mask(self.vaccine, virus):
                virus.rect.x = random.randint(1500, 1800)
                virus.rect.y = random.randint(100, 550)
                self.vaccine.vaccine_is_on = False
                self.player.player_score += 5

        if pg.sprite.collide_mask(self.player, self.mask):
            if self.player.player_life_point < 5:
                self.player.player_life_point += 1
            self.player.player_score += 3
            self.mask.appear = False


### GAME OVER SCREEN ###


    def game_over_screen(self):
        if self.game_over:
            try:
                with open(".highscores.pickle", "rb") as p:
                    pickle_objects = pickle.load(p)
                self.list_of_highscores = pickle_objects
                if len(self.list_of_highscores) < 10:
                    self.final_player_score_in_highscores = True
                elif len(self.list_of_highscores) >= 10 and self.list_of_highscores[-1][1] < self.player.player_score:
                    self.final_player_score_in_highscores = True
                else:
                    self.final_player_score_in_highscores = False
            except EOFError:
                self.list_of_highscores = []
                self.final_player_score_in_highscores = True

        while self.game_over:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game_open = False
                    self.game_running = False
                    self.game_over = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    for i in range(6):
                        if i == 0 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            self.game_running = False
                            self.game_over = False
                        elif i == 2 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            self.game_open = False
                            self.game_running = False
                            self.game_over = False
                        elif self.final_player_score_in_highscores != None and self.final_player_score_in_highscores and i == 4 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            self.list_of_highscores.append(tuple([self.player_name, self.player.player_score]))
                            self.list_of_highscores.sort(reverse = True, key = lambda x: x[1])
                            self.list_of_highscores = self.list_of_highscores[:10]
                            instance_of_PickleHighScore = PickleHighScore(self.list_of_highscores)
                            instance_of_PickleHighScore.saving_highscore_pickle()
                            self.final_player_score_in_highscores = None
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    elif len(self.player_name) < 10:
                        self.player_name += event.unicode

            self.draw_game_win(self.screen)
            if self.game_open and self.game_over == False and self.game_running == False:
                self.reset()

            pg.display.update()
            self.clock.tick(FPS)


    def draw_game_win(self, screen):
        self.screen.blit(self.background, (0, 0))
        self.message_to_screen_game_win(self.screen)
        self.loading_buttons_on_game_win_screen(self.screen, self.mouse_position, self.list_of_button_texts, self.buttons_size_x, self.buttons_size_y)


    def message_to_screen_game_win(self, screen):
        first_line_font = pg.font.Font('freesansbold.ttf', 60)
        line_font = pg.font.Font('freesansbold.ttf', 50)
        list_of_messages = ["CONGRATULATIONS!", f"Your score is {self.player.player_score} points."]
        if self.final_player_score_in_highscores:
            list_of_messages.extend(["Your score is in the top 10 highscores.",
            "Type your name by pressing the alphabet letters", 
            "(max. 10 characters) to save your score.",
            f"{self.player_name}"])
        elif self.final_player_score_in_highscores == False:
            list_of_messages.extend(["Unfortunately, your score is not in the", 
            "top 10 highscores. Therefore, your score",
            "cannot be saved. Try harder next time."])
        elif self.final_player_score_in_highscores == None:
            list_of_messages.extend(["Your score has been saved!", "You can check it in the Highscores menu on the main page."])

        for index, message in enumerate(list_of_messages):
            if index == 0:
                line = first_line_font.render(message, True, YELLOW)
            elif self.final_player_score_in_highscores and index == 5:
                line = first_line_font.render(message, True, BLACK)
            else:
                line = line_font.render(message, True, YELLOW)
            line_surface = pg.Surface(line.get_size())
            if self.final_player_score_in_highscores and index == 5:
                line_surface.fill(YELLOW)
            else:
                line_surface.fill(BLACK)
            line_surface.blit(line, (0, 0))
            if index == 0:
                self.screen.blit(line_surface, (400, 20))
            elif index == 1:
                self.screen.blit(line_surface, (440, 160))
            elif self.final_player_score_in_highscores and index == 5:
                self.screen.blit(line_surface, (480, 540))
            else:
                self.screen.blit(line_surface, (20, 160 + index * 60))


    def loading_buttons_on_game_win_screen(self, screen, mouse_position, list_of_button_texts, buttons_size_x, buttons_size_y):
        self.mouse_position = pg.mouse.get_pos()
        self.list_of_button_texts = ["MAIN", "PAGE", "EXIT", "GAME"]
        self.list_of_button_positions_x = [560, 560, 740, 740]
        self.list_of_button_positions_y = [665, 705, 665, 705]
        self.buttons_size_x = 170
        self.buttons_size_y = 110

        if self.final_player_score_in_highscores:
            self.list_of_button_texts.extend(["SAVE", "SCORE"])
            self.list_of_button_positions_x.extend([1060, 1060])
            self.list_of_button_positions_y.extend([510, 550])
            # Button Texts
            for i in range(4, 6):
                if i % 2 == 0 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y: 
                    pg.draw.rect(self.screen, RED, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y])
                    pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y], 5)
                elif i % 2 == 0: 
                    pg.draw.rect(self.screen, GREEN, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y])
                    pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y], 5)

                font = pg.font.Font('freesansbold.ttf', 40)
                text_font = font.render(self.list_of_button_texts[i], True, BLACK)
                text_font_width = text_font.get_width()
                text_font_height = text_font.get_height()
                self.screen.blit(text_font, (self.list_of_button_positions_x[i] + (self.buttons_size_x - text_font_width) // 2, self.list_of_button_positions_y[i] + (self.buttons_size_y - text_font_height) // 4))

        # Button Texts
        for i in range(4):
            if i % 2 == 0 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y: 
                pg.draw.rect(self.screen, RED, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y])
                pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y], 5)
            elif i % 2 == 0: 
                pg.draw.rect(self.screen, GREEN, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y])
                pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y], 5)

            font = pg.font.Font('freesansbold.ttf', 40)
            text_font = font.render(self.list_of_button_texts[i], True, BLACK)
            text_font_width = text_font.get_width()
            text_font_height = text_font.get_height()
            self.screen.blit(text_font, (self.list_of_button_positions_x[i] + (self.buttons_size_x - text_font_width) // 2, self.list_of_button_positions_y[i] + (self.buttons_size_y - text_font_height) // 4))



if __name__ == "__main__":
    instance_of_Main = Main()
    instance_of_Main.game_start_screen()