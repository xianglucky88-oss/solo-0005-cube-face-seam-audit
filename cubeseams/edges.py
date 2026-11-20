def corner(face, r, d):
    return tuple(n + r*u + d*v for n, u, v in zip(face.normal, face.right, face.down))


def strips(face):
    grid = face.pixels
    return (
        ('top', corner(face, -1, -1), corner(face, 1, -1), grid[0]),
        ('bottom', corner(face, -1, 1), corner(face, 1, 1), grid[-1]),
        ('left', corner(face, -1, -1), corner(face, -1, 1), tuple(row[0] for row in grid)),
        ('right', corner(face, 1, -1), corner(face, 1, 1), tuple(row[-1] for row in grid)),
    )


def pair(faces):
    edges = {}
    for face in faces:
        for side, start, end, values in strips(face):
            reverse = start > end
            key = (end, start) if reverse else (start, end)
            edges.setdefault(key, []).append((face.name, side, reverse, values[::-1] if reverse else values))
    return [(key, sorted(members)) for key, members in sorted(edges.items())]
