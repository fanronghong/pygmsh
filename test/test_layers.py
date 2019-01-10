# -*- coding: utf-8 -*-

import pygmsh

from helpers import compute_volume


def draw_inGmsh(points=None, lines=None, polygons=None, tetrahedrons=None, file="./jfoewfjlsjfsfesfaoew.geo"):
    """
    利用Gmsh进行可视化
    file的默认是随机取的，避免重名
    """
    import os
    import numpy as np
    with open(file, "w") as f:
        points_ = ""
        lines_ = ""
        pts_idx = 0
        lins_idx = 0

        if points is not None and isinstance(points, (list, np.ndarray)):
            if isinstance(points, list):
                points = np.vstack(points)
            for pt in points:
                points_ += "Point ({idx}) = {{{x}, {y}, {z}}};\n".format(idx=pts_idx, x=pt[0],
                                                                         y=pt[1], z=pt[2])
                pts_idx += 1


        if lines is not None and isinstance(lines, (list, np.ndarray)):
            if isinstance(lines, np.ndarray):
                assert lines.shape == (2, 3)
                lines = [lines]
            for ln in lines:
                assert ln.shape == (2, 3)
                pts = []
                for pt in ln:
                    points_ += "Point ({idx}) = {{{x}, {y}, {z}}};\n".format(idx=pts_idx, x=pt[0],
                                                                             y=pt[1], z=pt[2])
                    pts.append(pts_idx)
                    pts_idx += 1

                lines_ += "Line ({idx}) = {{{idx1}, {idx2}}};\n".format(idx=lins_idx,
                                                                        idx1=pts[0], idx2=pts[1])
                lins_idx += 1


        if polygons is not None and isinstance(polygons, (list, np.ndarray)):
            if isinstance(polygons, np.ndarray):
                polygons = [polygons]
            for poly in polygons:
                pts = []
                for pt in poly:
                    points_ += "Point ({idx}) = {{{x}, {y}, {z}}};\n".format(idx=pts_idx, x=pt[0],
                                                                             y=pt[1], z=pt[2])
                    pts.append(pts_idx)
                    pts_idx += 1
                for i in range(len(pts)):
                    lines_ += "Line ({idx}) = {{{idx1}, {idx2}}};\n".format(idx=lins_idx,
                                                                            idx1=pts[i], idx2=pts[(i+1)%len(pts)])
                    lins_idx += 1


        if tetrahedrons is not None and isinstance(tetrahedrons, (list, np.ndarray)):
            if isinstance(tetrahedrons, np.ndarray):
                tetrahedrons = [tetrahedrons]
            for tet in tetrahedrons:
                pts = []
                for pt in tet:
                    points_ += "Point ({idx}) = {{{x}, {y}, {z}}};\n".format(idx=pts_idx, x=pt[0], y=pt[1], z=pt[2])
                    pts.append(pts_idx)
                    pts_idx += 1
                for ln in combinations(pts, 2):
                    lines_ += "Line ({idx}) = {{{idx1}, {idx2}}};\n".format(idx=lins_idx, idx1=ln[0], idx2=ln[1])
                    lins_idx += 1


        f.writelines(points_)
        f.writelines(lines_)

    # 也可用 os.popen(), 但是是非阻塞的
    os.system("/home/fan/Softwares/gmsh-3.0.5-Linux/bin/gmsh {}".format(file))
    os.remove(file)




def test(lcar=0.05):
    geom = pygmsh.built_in.Geometry()

    # Draw a cross with a circular hole
    circ = geom.add_circle([0.0, 0.0, 0.0], 0.1, lcar=lcar, make_surface=False)
    poly = geom.add_polygon(
        [
            [+0.0, +0.5, 0.0],
            [-0.1, +0.1, 0.0],
            [-0.5, +0.0, 0.0],
            [-0.1, -0.1, 0.0],
            [+0.0, -0.5, 0.0],
            [+0.1, -0.1, 0.0],
            [+0.5, +0.0, 0.0],
            [+0.1, +0.1, 0.0],
        ],
        lcar=lcar,
        holes=[circ],
    )

    axis = [0, 0, 1.0]

    geom.extrude(poly, translation_axis=axis, num_layers=1)

    ref = 0.16951514066385628
    points, cells, _, _, _ = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(points, cells) - ref) < 1.0e-2 * ref
    return points, cells


if __name__ == "__main__":
    import meshio

    meshio.write_points_cells("layers.vtu", *test())
