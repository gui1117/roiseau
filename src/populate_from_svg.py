"""Module to populate a world from an svg file"""

import svg.path
import xml.etree.ElementTree as ElementTree
import units

def populate_with_file(world, svg_file):
    """
    Populate world from svg file

    world: World
    svg_file: filename string

    WARNING: this function is not safe against `billion laughs` and `quadratic blowup` attack,
    decoding untrusted source can result in consumming all CPU and memory.
    see https://docs.python.org/3/library/xml.html#xml-vulnerabilities
    """
    tree = ElementTree.parse(svg_file)
    root = tree.getroot()
    for child in root.findall('{http://www.w3.org/2000/svg}g'):
        for path in child.findall('{http://www.w3.org/2000/svg}path'):
            populate_with_path_element(world, path)

def populate_with_path_element(world, element):
    """
    Populate world from an svg path element.

    The unit will be choosen using the color of the stroke.
    """
    for attr in element.get('style').split(';'):
        key, value = attr.split(':')
        if key != 'stroke':
            continue
        path_d = svg.path.parse_path(element.get('d'))
        if value == '#000000':
            populate_wall_from_path_d(world, path_d)
        elif value == '#ff0000':
            populate_deadly_wall_from_path_d(world, path_d)
        elif value == '#00ff00':
            populate_player_from_path_d(world, path_d)


def populate_wall_from_path_d(world, path):
    """Instantiate a wall using an svg path element d attribute"""
    for line in path[1:]:
        x1 = line.point(0).real
        y1 = -line.point(0).imag
        x2 = line.point(1).real
        y2 = -line.point(1).imag
        units.Wall(world, (x1, y1), (x2, y2))

def populate_deadly_wall_from_path_d(world, path):
    """Instantiate a wall using an svg path element d attribute"""
    for line in path[1:]:
        x1 = line.point(0).real
        y1 = -line.point(0).imag
        x2 = line.point(1).real
        y2 = -line.point(1).imag
        units.DeadlyWall(world, (x1, y1), (x2, y2))

def populate_player_from_path_d(world, path):
    """Instantiate a player using an svg path element d attribute"""
    x = path[0].point(0).real
    y = -path[0].point(0).imag
    units.Player(world, (x, y))