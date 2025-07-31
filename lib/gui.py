import pygame as pg
from typing import Callable

from lib.util import is_alphanumeric
from lib.string_tree import StringTree

'''
    An abstract class representing any object that can be rendered to
    the screen
'''
class GuiElement:
    surface: pg.Surface
    rect: pg.Rect
    def __init__(self):
        pass

    def mouse_movement(self, pressed: bool, dx: float, dy: float):
        pass

    def on_click(self, mpos: list[float]):
        pass

    def key_press(self, key: pg.event.Event):
        pass

    def render(self):
        pass

    def was_pressed(self, mpos: list[float]) -> bool:
        return False

'''
    A 'null' GuiElement
'''
class BlankElement(GuiElement):
    def was_pressed(self, mpos: list[float]) -> bool:
        return False

'''
    Just a text box
'''
class Text(GuiElement):
    def __init__(self, coords: list[float], text: str, font: pg.font.Font) -> None:
        self.surface = font.render(text, True, (0, 0,0), None)
        self.rect = self.surface.get_rect()
        self.rect.move_ip(coords)

    def was_pressed(self, mpos: list[float]) -> bool:
        return self.rect.collidepoint(mpos)

'''
    An element that calls a function which interacted with
'''
class Button(GuiElement):
    def __init__(self, rect: pg.Rect, surface: pg.Surface, onclick: Callable) -> None:
        self.rect = rect
        self.surface = surface
        self.onclick = onclick

    def on_click(self, mpos: list[float]):
        if self.was_pressed(mpos):
            self.onclick()

    def was_pressed(self, mpos: list[float]) -> bool:
        return self.rect.collidepoint(mpos)

'''
    An image that can be scrolled across by moving the mouse to the edge
'''
class ScrollingImage(GuiElement):
    def __init__(self, rect: pg.Rect, image: pg.Surface, offset: list[float]) -> None:
        self.rect = rect
        self.surface = pg.Surface((rect.right - rect.left, rect.bottom - rect.top), pg.SRCALPHA)
        self.image = image
        self.offset = offset
        self.surface.blit(self.image, self.offset)

    def mouse_movement(self, pressed: bool, dx: float, dy: float):
        if pressed: self.scroll(dx, dy)

    def render(self):
        self.surface.fill((0,0,0,0))
        self.surface.blit(self.image, self.offset)

    def scroll(self, dx: float, dy: float):
        self.offset[0] += dx
        self.offset[1] += dy
        if self.offset[0] < -(self.image.get_width()-self.surface.get_width()): self.offset[0] = -(self.image.get_width()-self.surface.get_width())
        if self.offset[0] > 0: self.offset[0] = 0
        if self.offset[1] > 0: self.offset[1] = 0
        if self.offset[1] < -(self.image.get_height() - self.surface.get_height()): self.offset[1] = -(self.image.get_height() - self.surface.get_height())
        self.render()

    def was_pressed(self, mpos: list[float]) -> bool:
        return self.rect.collidepoint(mpos)

'''
    An element composed of other elements
'''
class Frame(GuiElement):
    def __init__(self, rect: pg.Rect, background: pg.Surface, *elements: GuiElement) -> None:
        self.rect = rect
        self.surface = background
        self.background = background
        self.elements = list(elements)
        self.scoped_element = BlankElement()
        self.update_surface()

    def update_surface(self):
        self.surface.blit(self.background, (0,0))
        for el in self.elements:
            self.surface.blit(el.surface, (el.rect.left, el.rect.top))

    def on_click(self, mpos: list[float]):
        mpos = [mpos[0] - self.rect.left, mpos[1] - self.rect.top]
        if not self.scoped_element.was_pressed(mpos):
            for el in self.elements:
                if el.was_pressed(mpos):
                    self.scoped_element = el
        self.scoped_element.on_click(mpos)
        self.update_surface()

    def mouse_movement(self, pressed: bool, dx: float, dy: float):
        self.scoped_element.mouse_movement(pressed, dx, dy)

    def key_press(self, key: pg.event.Event):
        self.scoped_element.key_press(key)
        self.update_surface()

    def was_pressed(self, mpos: list[float]) -> bool:
        return self.rect.collidepoint(mpos)

'''
    An element that can be typed into
'''
class TypeBar(GuiElement):
    def __init__(self, rect: pg.Rect, text: str) -> None:
        self.rect = rect
        self.surface = pg.Surface((rect.right - rect.left, rect.bottom - rect.top))
        self.font = pg.font.SysFont("arial", 20)
        self.text = text
        self.render()

    def render(self):
        self.surface.fill((255,255,255))
        self.surface.blit(self.font.render(self.text, True, (0,0,0), None), (0,0))

    def key_press(self, key: pg.event.Event):
        if is_alphanumeric(key.unicode):
            self.text += key.unicode
        elif key.unicode == '\x08':
            self.text = self.text[:len(self.text)-1]
        self.render()

    def was_pressed(self, mpos: list[float]) -> bool:
        return self.rect.collidepoint(mpos)

'''
    A type bar that has default answers which it will display as a user is typing
'''
class SearchBar(GuiElement):
    def __init__(self, rect: pg.Rect, default: str, valid_answers: list[str]) -> None:
        self.rect = rect
        self.surface = pg.Surface((rect.right - rect.left, rect.bottom - rect.top))
        self.valid_answers = StringTree(valid_answers)
        self.name_hint = ""
        self.input = ""
        self.default = default
        self.font = pg.font.SysFont("arial", 20)
        self.render()

    ''' Change the words which the bar will allow you to type / predict '''
    def update_valid_answers(self, new_answers: list[str]):
        self.valid_answers = StringTree(new_answers)

    def render(self):
        self.surface.fill((255,255,255))
        if self.input == '':
            self.surface.blit(self.font.render(self.default, True, (0,0,0), None), (0,0))
            return
        prediction = self.valid_answers.predict_string(self.input)
        self.surface.blit(self.font.render(prediction, True, (122, 122, 12), None), (0,0))
        self.surface.blit(self.font.render(self.input, True, (0,0,0), None), (0,0))

    def key_press(self, key: pg.event.Event):
        if is_alphanumeric(key.unicode):
            self.input += key.unicode
        elif key.unicode == '\x08':
            self.input = self.input[:len(self.input)-1]
        elif key.unicode == '\t':
            self.input = self.valid_answers.predict_string(self.input)
        self.render()

    def was_pressed(self, mpos: list[float]) -> bool:
        return self.rect.collidepoint(mpos)
