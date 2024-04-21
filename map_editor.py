import pygame as pg
from gui import Button, ScrollingImage, Frame, TypeBar, Text
from util import circle_col

class DebugVertex:
    def __init__(self, x: float, y: float, name: str):
        self.coords = [x,y]
        self.node = None
        self.name = name

scrolling_image = None
editor_overlay = None
vertex_frame = None
win_height = None

edit_modes = ["Vertex", "Edge", "Pan"]
edit_mode = 0

vertices: list[DebugVertex] = []
selected_node = -1

def load_things(view: ScrollingImage, overlay: ScrollingImage, wheight: float):
    global scrolling_image, editor_overlay, win_height
    scrolling_image = view
    editor_overlay = overlay
    win_height = wheight

def generate_vertex_edit_frame(w_width: float, f_width: float) -> Frame:
    global vertex_frame
    def submit_vertex_data():
        global vertices, selected_node
        v = vertices[selected_node]
        v.name = name_typer.text
        v.coords[0] = float(x_typer.text)
        v.coords[1] = float(y_typer.text)
        rerender_vertices()
    def delete_vertex_data():
        global vertices, selected_node
        del(vertices[selected_node])
        if selected_node >= len(vertices): selected_node = len(vertices)-1
        update_vertex_frame()
        rerender_vertices()

    font = pg.font.SysFont("arial", 30)
    name_typer = TypeBar(pg.Rect(10, 10, f_width - 30, 40), 'SelectedVertex')
    x_pos_text = Text((10, 60),"X:", font)
    x_typer = TypeBar(pg.Rect(50, 60, 70, 40), "0.0")
    y_pos_text = Text((130, 60),"Y:", font)
    y_typer = TypeBar(pg.Rect(170, 60, 70, 40), "0.0")
    submit_btn_sprite = font.render("Submit", True, (255,255,255), (122, 122, 122))
    submit_btn = Button(pg.Rect(50, 220, 300, 400), submit_btn_sprite, submit_vertex_data)
    delete_btn_sprite = font.render("Delete", True,(255,255,255), (122,122,122) )
    delete_btn = Button(pg.Rect(200, 220, 300, 400), delete_btn_sprite, delete_vertex_data)
    frame_bg = pg.Surface((f_width, 400))
    frame_bg.fill((61, 61, 61))
    vertex_frame = Frame(pg.Rect(w_width, 350, f_width, 400), frame_bg, name_typer, x_pos_text, x_typer, y_pos_text, y_typer, submit_btn, delete_btn)
    return vertex_frame

def rerender_vertices():
    global vertices, editor_overlay
    editor_overlay.image.fill((0,0,0,0))
    for v in vertices:
        pg.draw.circle(editor_overlay.image, (0,0,0), v.coords, 5)
    editor_overlay.render()

def update_vertex_frame():
    global vertex_frame, vertices, selected_node
    name_typer = vertex_frame.elements[0]
    x_typer = vertex_frame.elements[2]
    y_typer = vertex_frame.elements[4]
    name_typer.text = vertices[selected_node].name
    x_typer.text = str(vertices[selected_node].coords[0])
    y_typer.text = str(vertices[selected_node].coords[1])
    name_typer.render()
    x_typer.render()
    y_typer.render()
    vertex_frame.update_surface()

def scrolling_image_on_click_override(mpos: list[float]):
    global edit_mode, editor_overlay, vertices, selected_node
    if edit_mode == 0:
        for i, v in enumerate(vertices):
            pos = [v.coords[0] + editor_overlay.offset[0], abs(v.coords[1] + editor_overlay.offset[1] - win_height) + 50]
            print(pos, 5, mpos)
            if circle_col(pos, 5, mpos):
                selected_node = i
                print("found node")
                update_vertex_frame()
                return
        adjusted_y = abs(mpos[1] - win_height) + 50 # need to account for bar at bottom
        adjusted_coords = [mpos[0] + abs(editor_overlay.offset[0]), adjusted_y - editor_overlay.offset[1]]
        vertices.append(DebugVertex(adjusted_coords[0], adjusted_coords[1], "Vertex" + str(len(vertices))))
        selected_node = len(vertices)-1
        pg.draw.circle(editor_overlay.image, (0,0,0), adjusted_coords, 5)
        update_vertex_frame()
        editor_overlay.render()

def scrolling_image_mouse_move_override(pressed: bool, dx: float, dy: float):
    global scrolling_image, editor_overlay
    if pressed and edit_mode == 2: 
        scrolling_image.scroll(dx, dy)
        editor_overlay.scroll(dx, dy)

def toggle_edit_mode(mode_btn: Button, font: pg.font.Font):
    global edit_mode
    edit_mode = (edit_mode + 1) % len(edit_modes)
    mode_btn.surface = font.render("Mode: " + edit_modes[edit_mode], True, (255,255,255), (122,122,122))