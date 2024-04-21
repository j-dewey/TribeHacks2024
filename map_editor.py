import pygame as pg
from graph import Node
from gui import Button, ScrollingImage, Frame, TypeBar, Text
from util import circle_col, dist

class DebugVertex:
    def __init__(self, x: float, y: float, name: str, node: Node):
        self.coords = [x,y]
        self.node = node
        self.name = name

scrolling_image = None
editor_overlay = None
drawn_path_overlay = None
vertex_frame = None
win_height = None

edit_modes = ["Vertex", "Edge", "Pan"]
edit_mode = 0

traversal_nodes: dict[str:Node] = {}
vertices: list[DebugVertex] = []
edges: list[tuple[int]] = []
selected_node = -1
edge_connections = []

def overlay_overlay():
    # overlay overlay on overlay
    global editor_overlay, drawn_path_overlay
    editor_overlay.surface.blit(drawn_path_overlay, editor_overlay.offset)

def draw_path(path: list[Node]):
    global drawn_path_overlay
    drawn_path_overlay.fill((0,0,0,0)) 
    for i in range(len(path)-1):
        v1 = path[i].gui_inter.coords
        v2 = path[i+1].gui_inter.coords
        pg.draw.circle(drawn_path_overlay, (255,0,0), v1, 5)
        pg.draw.line(drawn_path_overlay, (255,0,0), v1, v2, 3)
        pg.draw.circle(drawn_path_overlay, (255,0,0), v2, 5)

def save_map_data():
    global vertices, edges
    file = open('map.map', 'w')
    file.write(str('\\vertex'))
    for v in vertices:
        file.write(str(f'\n{v.coords[0]} {v.coords[1]} {v.name}'))
    file.write('\n\\connections')
    for e in edges:
        d = dist(vertices[e[0]].coords, vertices[e[1]].coords)
        file.write('\n{} {} {}'.format(e[0], e[1], d))
    file.close()

def load_map_data():
    global vertices, edges, traversal_nodes
    file = open('map.map', 'r')
    data = file.read().split('\n')
    reading_indices = False
    for line in data:
        if line == '\\vertex': continue
        if line == '\\connections': 
            reading_indices = True
            continue
        parts = line.split(' ')
        p1 = parts[0]
        p2 = parts[1]
        p3 = ' '.join(parts[2::])
        if not reading_indices:
            node = Node(p3)
            if not (len(p3) >= 7 and p3[:6] == 'Vertex'):
                traversal_nodes[p3] = node
            vertices.append(DebugVertex(float(p1), float(p2), p3, node))
            node.gui_inter = vertices[len(vertices)-1]
        if reading_indices:
            edges.append((int(p1), int(p2)))
            v1 = vertices[int(p1)].node
            v2 = vertices[int(p2)].node
            v1.connect(v2, float(p3))
    rerender_vertices()

def load_things(view: ScrollingImage, overlay: ScrollingImage, wheight: float):
    global scrolling_image, editor_overlay, win_height, edit_mode, drawn_path_overlay
    edit_mode = 2
    scrolling_image = view
    editor_overlay = overlay
    drawn_path_overlay = pg.Surface(overlay.image.get_size(), pg.SRCALPHA)
    win_height = wheight
    load_map_data()

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
    for e in edges:
        v0 = vertices[e[0]]
        v1 = vertices[e[1]]
        pg.draw.line(editor_overlay.image, (122,122,122), v0.coords, v1.coords, 2)
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
    global edit_mode, editor_overlay, vertices, selected_node, edge_connections, edges
    if edit_mode == 0:
        for i, v in enumerate(vertices):
            pos = [v.coords[0] + editor_overlay.offset[0], abs(v.coords[1] + editor_overlay.offset[1] - win_height) + 50]
            if circle_col(pos, 5, mpos):
                selected_node = i
                update_vertex_frame()
                return
        adjusted_y = abs(mpos[1] - win_height) + 50 # need to account for bar at bottom
        adjusted_coords = [mpos[0] + abs(editor_overlay.offset[0]), adjusted_y - editor_overlay.offset[1]]
        vertices.append(DebugVertex(adjusted_coords[0], adjusted_coords[1], "Vertex" + str(len(vertices))))
        selected_node = len(vertices)-1
        pg.draw.circle(editor_overlay.image, (0,0,0), adjusted_coords, 5)
        update_vertex_frame()
        editor_overlay.render()
    if edit_mode == 1:
        for i, v in enumerate(vertices):
            pos = [v.coords[0] + editor_overlay.offset[0], abs(v.coords[1] + editor_overlay.offset[1] - win_height) + 50]
            if circle_col(pos, 5, mpos):
                selected_node = i
                update_vertex_frame()
                edge_connections.append(i)
                break
        if len(edge_connections) == 2:
            edges.append(edge_connections)
            pg.draw.line(editor_overlay.image, (122,122,122), vertices[edge_connections[0]].coords, vertices[edge_connections[1]].coords, 2)
            editor_overlay.render()
            edge_connections = []
                

def scrolling_image_mouse_move_override(pressed: bool, dx: float, dy: float):
    global scrolling_image, editor_overlay
    if pressed and edit_mode == 2: 
        scrolling_image.scroll(dx, dy)
        editor_overlay.scroll(dx, dy)

def toggle_edit_mode(mode_btn: Button, font: pg.font.Font):
    global edit_mode
    edit_mode = (edit_mode + 1) % len(edit_modes)
    mode_btn.surface = font.render("Mode: " + edit_modes[edit_mode], True, (255,255,255), (122,122,122))