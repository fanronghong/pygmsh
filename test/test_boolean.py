#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pygmsh
import pytest

from helpers import compute_volume


@pytest.mark.skipif(
    pygmsh.get_gmsh_major_version() < 3,
    reason='requires Gmsh >= 3'
    )
def test_union():
    geom = pygmsh.opencascade.Geometry(
        characteristic_length_min=0.1,
        characteristic_length_max=0.1,
        )

    rectangle = geom.add_rectangle(-1.0, -1.0, 0.0, 2.0, 2.0)
    disk_w = geom.add_disk(-1.0, 0.0, 0.0, 0.5)
    disk_e = geom.add_disk(+1.0, 0.0, 0.0, 0.5)
    geom.boolean_union([rectangle, disk_w, disk_e])

    ref = 4.780361
    points, cells, _, _, _ = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(points, cells) - ref) < 1.0e-2 * ref
    return points, cells


@pytest.mark.skipif(
    pygmsh.get_gmsh_major_version() < 3,
    reason='requires Gmsh >= 3'
    )
def test_intersection():
    geom = pygmsh.opencascade.Geometry(
        characteristic_length_min=0.1,
        characteristic_length_max=0.1,
        )

    rectangle = geom.add_rectangle(-1.0, -1.0, 0.0, 2.0, 2.0)
    disk_w = geom.add_disk(-1.0, 0.0, 0.0, 0.5)
    disk_e = geom.add_disk(+1.0, 0.0, 0.0, 0.5)
    geom.boolean_intersection([rectangle, disk_w, disk_e])

    ref = 0.7803612
    points, cells, _, _, _ = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(points, cells) - ref) < 1.0e-2 * ref
    return points, cells


@pytest.mark.skipif(
    pygmsh.get_gmsh_major_version() < 3,
    reason='requires Gmsh >= 3'
    )
def test_difference():
    geom = pygmsh.opencascade.Geometry(
        characteristic_length_min=0.1,
        characteristic_length_max=0.1,
        )

    rectangle = geom.add_rectangle(-1.0, -1.0, 0.0, 2.0, 2.0)
    disk_w = geom.add_disk(-1.0, 0.0, 0.0, 0.5)
    disk_e = geom.add_disk(+1.0, 0.0, 0.0, 0.5)
    geom.boolean_difference([rectangle], [disk_w, disk_e])

    ref = 3.2196387
    points, cells, _, _, _ = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(points, cells) - ref) < 1.0e-2 * ref
    return points, cells


if __name__ == '__main__':
    import meshio
    meshio.write('boolean.vtu', *test_difference())
