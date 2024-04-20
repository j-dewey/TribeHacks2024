import pygame as pg

class GuiElement:
    def mouse_movement(self, pressed: bool, dx: float, dy: float):
        pass

    def key_press(self, key: str):
        pass

    def was_pressed(self, mpos: list[float]) -> bool:
        print(self.rect, mpos)
        return self.rect.collidepoint(mpos)

class BlankElement(GuiElement):
    def was_pressed(self, mpos: list[float]) -> bool:
        return False

class ScrollingImage(GuiElement):
    def __init__(self, rect: pg.Rect, image: pg.Surface) -> None:
        self.rect = rect
        self.surface = pg.Surface((rect.right - rect.left, rect.bottom - rect.top))
        self.image = image
        self.offset = [0,0]
        self.surface.blit(self.image, self.offset)

    def mouse_movement(self, pressed: bool, dx: float, dy: float):
        if pressed: self.scroll(dx, dy)

    def scroll(self, dx: float, dy: float):
        self.offset[0] += dx
        self.offset[1] += dy
        self.surface.blit(self.image, self.offset)