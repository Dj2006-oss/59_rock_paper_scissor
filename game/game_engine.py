
import random
import pygame
from game.button import ChoiceButton


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.choices = ["ROCK", "PAPER", "SCISSORS"]
        self.player_history = []

        btn_w, btn_h = 130, 50
        gap = 20
        total_w = 3 * btn_w + 2 * gap
        start_x = (width - total_w) // 2
        btn_y = height - 85

        self.buttons = [
            ChoiceButton(
                "ROCK",
                pygame.Rect(start_x, btn_y, btn_w, btn_h),
                (160, 50, 50),
                (200, 70, 70),
            ),
            ChoiceButton(
                "PAPER",
                pygame.Rect(
                    start_x + btn_w + gap, btn_y, btn_w, btn_h
                ),
                (40, 100, 170),
                (60, 130, 210),
            ),
            ChoiceButton(
                "SCISSORS",
                pygame.Rect(
                    start_x + 2 * (btn_w + gap),
                    btn_y,
                    btn_w,
                    btn_h,
                ),
                (180, 140, 30),
                (220, 180, 50),
            ),
        ]

        self.player_choice = None
        self.cpu_choice = None

        self.result_text = "Make your move!"
        self.result_color = (220, 225, 235)

        self.player_score = 0
        self.cpu_score = 0
        self.target_score = 5
        self.match_over = False

        self.restart_rect = pygame.Rect(
            self.width // 2 - 75,
            self.height - 75,
            150,
            45,
        )

        self.round_resolved_time = 0
        self.display_duration = 1800
        self.showing_result = False

        self.font_title = pygame.font.SysFont(None, 36)
        self.font_hud = pygame.font.SysFont(None, 26)
        self.font_arena = pygame.font.SysFont(None, 32)

    def determine_winner(self, player, cpu):
        if player == cpu:
            return "TIE"

        rules = {
            ("ROCK", "SCISSORS"): "PLAYER",
            ("SCISSORS", "PAPER"): "PLAYER",
            ("PAPER", "ROCK"): "PLAYER",
            ("SCISSORS", "ROCK"): "CPU",
            ("PAPER", "SCISSORS"): "CPU",
            ("ROCK", "PAPER"): "CPU",
        }

        return rules.get((player, cpu), "TIE")

    def get_cpu_choice(self):
        # Play randomly until enough player choices are recorded.
        if len(self.player_history) < 3:
            return random.choice(self.choices)

        # Consider the player's last 10 choices.
        recent_choices = self.player_history[-10:]

        most_common = max(
            self.choices,
            key=recent_choices.count,
        )

        # Choose the move that beats the player's most common move.
        counters = {
            "ROCK": "PAPER",
            "PAPER": "SCISSORS",
            "SCISSORS": "ROCK",
        }

        return counters[most_common]

    def play_round(self, choice):
        self.player_choice = choice
        self.player_history.append(choice)
        self.cpu_choice = self.get_cpu_choice()

        outcome = self.determine_winner(
            self.player_choice,
            self.cpu_choice,
        )

        if outcome == "PLAYER":
            self.player_score += 1
            self.result_text = (
                f"You Win! {self.player_choice} beats "
                f"{self.cpu_choice}."
            )
            self.result_color = (80, 230, 120)

        elif outcome == "CPU":
            self.cpu_score += 1
            self.result_text = (
                f"You Lose! {self.cpu_choice} beats "
                f"{self.player_choice}."
            )
            self.result_color = (240, 80, 80)

        else:
            self.result_text = (
                f"It's a Draw! Both picked {self.player_choice}."
            )
            self.result_color = (240, 210, 80)

        # Check whether either side has won the match.
        if self.player_score >= self.target_score:
            self.match_over = True
            self.result_text = "YOU WON THE MATCH!"
            self.result_color = (80, 230, 120)

        elif self.cpu_score >= self.target_score:
            self.match_over = True
            self.result_text = "CPU WON THE MATCH!"
            self.result_color = (240, 80, 80)

        self.showing_result = True
        self.round_resolved_time = pygame.time.get_ticks()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.match_over:
                if self.restart_rect.collidepoint(event.pos):
                    self.player_score = 0
                    self.cpu_score = 0
                    self.player_history = []

                    self.player_choice = None
                    self.cpu_choice = None

                    self.result_text = "Make your move!"
                    self.result_color = (190, 195, 205)

                    self.match_over = False
                    self.showing_result = False

                return

            if not self.showing_result:
                for btn in self.buttons:
                    if btn.contains(event.pos):
                        self.play_round(btn.choice_name)
                        break

    def update(self):
        now = pygame.time.get_ticks()

        if (
            self.showing_result
            and not self.match_over
            and now - self.round_resolved_time
            >= self.display_duration
        ):
            self.player_choice = None
            self.cpu_choice = None

            self.result_text = "Make your move!"
            self.result_color = (190, 195, 205)
            self.showing_result = False

    def render(self, screen):
        screen.fill((24, 28, 36))

        title_surf = self.font_title.render(
            "Rock Paper Scissors",
            True,
            (245, 245, 245),
        )
        screen.blit(
            title_surf,
            (
                self.width // 2 - title_surf.get_width() // 2,
                14,
            ),
        )

        player_surf = self.font_hud.render(
            f"Player Score: {self.player_score}",
            True,
            (100, 180, 255),
        )
        cpu_surf = self.font_hud.render(
            f"CPU Score: {self.cpu_score}",
            True,
            (255, 120, 120),
        )

        screen.blit(player_surf, (35, 52))
        screen.blit(
            cpu_surf,
            (self.width - cpu_surf.get_width() - 35, 52),
        )

        pygame.draw.line(
            screen,
            (45, 52, 66),
            (25, 82),
            (self.width - 25, 82),
            2,
        )

        player_text = (
            self.player_choice if self.player_choice else "--"
        )
        cpu_text = self.cpu_choice if self.cpu_choice else "--"

        player_pick_surf = self.font_arena.render(
            f"Your Pick: {player_text}",
            True,
            (225, 225, 230),
        )
        cpu_pick_surf = self.font_arena.render(
            f"CPU Pick: {cpu_text}",
            True,
            (225, 225, 230),
        )

        screen.blit(
            player_pick_surf,
            (
                self.width // 2 - player_pick_surf.get_width() // 2,
                115,
            ),
        )
        screen.blit(
            cpu_pick_surf,
            (
                self.width // 2 - cpu_pick_surf.get_width() // 2,
                155,
            ),
        )

        result_surf = self.font_arena.render(
            self.result_text,
            True,
            self.result_color,
        )
        screen.blit(
            result_surf,
            (
                self.width // 2 - result_surf.get_width() // 2,
                205,
            ),
        )

        for btn in self.buttons:
            btn.render(screen)

        # Display the restart button after the match ends.
        if self.match_over:
            pygame.draw.rect(
                screen,
                (50, 150, 90),
                self.restart_rect,
                border_radius=8,
            )

            restart_text = self.font_hud.render(
                "RESTART",
                True,
                (255, 255, 255),
            )

            screen.blit(
                restart_text,
                (
                    self.restart_rect.centerx
                    - restart_text.get_width() // 2,
                    self.restart_rect.centery
                    - restart_text.get_height() // 2,
                ),
            )
