from dataclasses import dataclass


AXES = {(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)}


@dataclass(frozen=True)
class Face:
    name: str
    right: tuple
    down: tuple
    normal: tuple
    pixels: tuple


def axis(values):
    vector = tuple(values)
    if any(type(v) is not int for v in vector) or vector not in AXES:
        raise ValueError('frame axes must be signed unit axes')
    return vector


def cross(a, b):
    x, y, z = a
    u, v, w = b
    return y*w-z*v, z*u-x*w, x*v-y*u


def parse(document):
    faces = []
    names, normals = set(), set()
    size = document['size']
    if type(size) is not int or not 2 <= size <= 128:
        raise ValueError('face size must be 2 through 128')
    for row in document['faces']:
        name = row['id']
        right, down, normal = (axis(row[key]) for key in ('right', 'down', 'normal'))
        if not isinstance(name, str) or not name or name in names:
            raise ValueError('face IDs must be unique nonempty strings')
        if cross(right, down) != normal or normal in normals:
            raise ValueError(f'invalid or repeated face orientation: {name}')
        grid = tuple(tuple(values) for values in row['pixels'])
        if len(grid) != size or any(len(values) != size for values in grid) or any(
            type(value) is not int or not 0 <= value <= 255 for values in grid for value in values
        ):
            raise ValueError(f'invalid pixel grid: {name}')
        names.add(name)
        normals.add(normal)
        faces.append(Face(name, right, down, normal, grid))
    if normals != AXES:
        raise ValueError('all six face normals must be represented')
    return faces
