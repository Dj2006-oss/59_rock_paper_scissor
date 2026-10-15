
import pygame


class ChoiceButton:
    def __init__(self, choice_name, rect, color, hover_color):
        self.choice_name = choice_name
        self.rect = rect
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont(None, 26)
        self.icon_font = pygame.font.SysFont(None, 34)

        self.icons = {
            "ROCK": "✊",
            "PAPER": "✋",
            "SCISSORS": "✌",
        }

    def contains(self, pos):
        return self.rect.collidepoint(pos)

    def render(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse_pos)

        bg_color = self.hover_color if hovered else self.color

        pygame.draw.rect(
            surface,
            bg_color,
            self.rect,
            border_radius=8,
        )
        pygame.draw.rect(
            surface,
            (230, 230, 235),
            self.rect,
            width=2,
            border_radius=8,
        )

        icon = self.icons.get(self.choice_name, "")
        icon_surf = self.icon_font.render(
            icon, True, (255, 255, 255)
        )
        text_surf = self.font.render(
            self.choice_name, True, (255, 255, 255)
        )

        # Display the icon above the choice label.
        surface.blit(
            icon_surf,
            (
                self.rect.centerx - icon_surf.get_width() // 2,
                self.rect.y + 3,
            ),
        )
        surface.blit(
            text_surf,
            (
                self.rect.centerx - text_surf.get_width() // 2,
                self.rect.bottom - text_surf.get_height() - 3,
            ),
        )
