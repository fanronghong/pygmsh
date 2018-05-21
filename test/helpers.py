# -*- coding: utf-8 -*-
#
import math
import numpy


def prune_nodes(points, cells):
    # Only points/cells that actually used
    uvertices, uidx = numpy.unique(cells, return_inverse=True)
    cells = uidx.reshape(cells.shape)
    points = points[uvertices]
    return points, cells


def get_simplex_volumes(pts, cells):
    '''Signed volume of a simplex in nD. Note that signing only makes sense for
    n-simplices in R^n.
    '''
    assert numpy.all(numpy.abs(pts[:, 2]) < 1.0e-14)
    pts = pts[:, :2]

    n = pts.shape[1]
    assert cells.shape[1] == n+1

    p = pts[cells]
    p = numpy.concatenate([p, numpy.ones(list(p.shape[:2]) + [1])], axis=-1)
    return numpy.abs(numpy.linalg.det(p) / math.factorial(n))


def compute_volume(points, cells):
    if 'tetra' in cells:
        vol = math.fsum(
            get_simplex_volumes(*prune_nodes(points, cells['tetra']))
            )
    elif 'triangle' in cells or 'quad' in cells:
        vol = 0.0
        if 'triangle' in cells:
            # triangles
            vol += math.fsum(get_simplex_volumes(
                *prune_nodes(points, cells['tetra'])
                ))
        if 'quad' in cells:
            # quad: treat as two triangles
            quads = cells['quad'].T
            split_cells = numpy.column_stack([
                [quads[0], quads[1], quads[2]],
                [quads[0], quads[2], quads[3]],
                ]).T
            vol += math.fsum(get_simplex_volumes(
                *prune_nodes(points, split_cells)
                ))
    else:
        assert 'line' in cells
        segs = numpy.diff(points[cells['line']], axis=1).squeeze()
        vol = numpy.sum(numpy.sqrt(numpy.einsum('...j, ...j', segs, segs)))

    return vol


def plot(filename, points, cells):
    import matplotlib.pyplot as plt
    pts = points[:, :2]
    for e in cells['triangle']:
        for idx in [[0, 1], [1, 2], [2, 0]]:
            X = pts[e[idx]]
            plt.plot(X[:, 0], X[:, 1], '-k')
    plt.gca().set_aspect('equal', 'datalim')
    plt.axis('off')

    # plt.show()
    plt.savefig(filename, transparent=True)
    return
