from .edges import pair
from .faces import parse


def run(document):
    tolerance = document['tolerance']
    if type(tolerance) is not int or not 0 <= tolerance <= 255:
        raise ValueError('tolerance must be an integer within 0..255')
    report = []
    for corners, (a, b) in pair(parse(document)):
        mismatches = [{'index': i, 'values': [x, y], 'difference': abs(x-y)}
                      for i, (x, y) in enumerate(zip(a[3], b[3])) if abs(x-y) > tolerance]
        report.append({'corners': corners, 'members': [{'face': m[0], 'side': m[1], 'reversed': m[2]}
                                                       for m in (a, b)], 'mismatches': mismatches})
    return {'seams': report, 'matched': sum(not edge['mismatches'] for edge in report)}
