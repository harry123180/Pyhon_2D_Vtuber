class LapMeshDeform():
    def __init__(self, verts, faces):
        self.verts = verts  # numpy array with shape of [n_v, 3], n_v is the number of  vertices
        self.faces = faces  # numpy array with shape of [n_f, 3], n_f is the number of vertices

    def _compute_edge(self):
        '''
        given faces with numpy array of [n_f, 3], return its edges[num_edge, 2], in addition edges[:, 0] < edges[:, 1].
        we do this sorting operation in edges' array for removing duplicated elements.
        For example self.faces[[0, 1, 2],
                               [0, 3, 1],
                               [0, 2, 4],
                              ]
        The returned edges will be: [[0, 1],
                                     [0, 2],
                                     [0, 3],
                                     [0, 4],
                                     [1, 2],
                                     [1, 3],
                                     [2, 4],
                                    ]

        Args:
            self.faces: numpy array with size of [n_f, 3], n_f is the number of faces.

        Return:
            uni_all_edge: numpy array with size of [n_e, 2], n_e is the number of edges.

        '''
        # get the edges of triangles. numpy array with shape [n_f, 2]
        edge_v0v1 = self.faces[:, [0, 1]]  # edge of v0---v1
        edge_v0v2 = self.faces[:, [0, 2]]  # edge of v0---v2
        edge_v1v2 = self.faces[:, [1, 2]]  # edge of v1---v2

        # sorting the vertex index in edges for the purpose of removing duplicated elements.
        # for example if edge_v0v1[i, :] = [4, 1]. we will change edge_v0v1[i, :] to be [1, 4]
        edge_v0v1.sort()
        edge_v0v2.sort()
        edge_v1v2.sort()

        all_edge = np.vstack((edge_v0v1, edge_v0v2, edge_v1v2))  # numpy array with shape [n_f*3, 2]

        # remove duplicated edges
        uni_all_edge = np.unique(all_edge, axis=0)

        return uni_all_edge

    def uniform_laplacian(self):
        '''
        computing the uniform laplacian matrix L, L is an n by n matrix sparse matrix.
        See the reference of <<Differential Representations for Mesh Processing>>
                   --  =   1 ,       if i=j
        L[i, j] --|    =  -wij,      wij = 1/|N(i)|if (i, j) belong to an edge of a face
                   --  =   0       , others.

        Args:
            self.faces: numpy array with shape of [n_f, 3], mesh's faces.
            self.verts: numpy array with shape of [n_v, 3], mesh's vertices.
                        we only used its n_v to create [n_v, n_v] sparse matrix.

        Return:
            lap_matrix: the returned Laplacian matrix, it is a spare matrix.

        '''
        # initial the laplacian matrix(i.e. L) of self.faces. with the shape of [n_v, n_v], n_v is the number of vertices
        lap_matrix = sparse.lil_matrix((self.verts.shape[0], self.verts.shape[0]), dtype=np.float32)

        # get the edges with sorted index. the edges_sorted is with the shape of [n_e, 2]
        edges_sorted = self._compute_edge()
        lap_matrix[edges_sorted[:, 0], edges_sorted[:, 1]] = 1  # L[i, j] = 1, for edge i----j
        lap_matrix[edges_sorted[:, 1], edges_sorted[:, 0]] = 1  # L[j, i] = 1, for edge i----j
        lap_matrix = normalize(lap_matrix, norm='l1',
                               axis=1) * -1  # normaliz the L[i, j], for edge i----j . to -1/|N(i)|

        unit_diagonal = identity(self.verts.shape[0], dtype=np.float32)  # L[i,j] = 1, if i=j
        lap_matrix += unit_diagonal

        return lap_matrix

    def cot_laplacian(self, area_normalize=True):
        '''
        computing the uniform laplacian matrix L, L is an n by n matrix sparse matrix.
        See the reference of <<Differential Representations for Mesh Processing>> for definition of the cot weight.
                   --  =   1 ,       if i=j
        L[i, j] --|    =  -wij,    wij = (cotαij + cotβij)/4A(i). 4A(i) = 0.5*sum_(k in N(i)) (cotαkj + cotβkj)|vi-vk|^2
                   --  =   0       , others.

        This operation of cot_laplacian use the area normalize. It's sum of weight not equal to 1.
        To compute the size of Voronoi regions : A(i)
        I follow the reference https://stackoverflow.com/questions/13882225/compute-the-size-of-voronoi-regions-from-delaunay-triangulation
        The cotαik*|vi-vk| = H, H is the length of perpendicular line from vertices of αik to edge vi---vk.
        so 0.5*cotαik*|vi-vk|^2 is the area of triangle which contain edge of vi---vk, and angle of αkj.

        Args:
            self.faces: numpy array with shape of [n_f, 3], mesh's faces.
            self.verts: numpy array with shape of [n_v, 3], mesh's vertices.
                        we only used its n_v to create [n_v, n_v] sparse matrix.
            area_normalize: True for wij = (cotαij + cotβij)/4A(i) depicted above.
                            False for wij = (cotαij + cotβij)/sum_(k in N(i)) (cotαkj + cotβkj)

        Return:
            lap_matrix: the returned Laplacian matrix, it is a spare matrix.
        '''
        # initial the laplacian matrix(i.e. L) of self.faces. with the shape of [n_v, n_v], n_v is the number of vertices
        lap_matrix = sparse.lil_matrix((self.verts.shape[0], self.verts.shape[0]), dtype=np.float32)
        sum_area_vert = np.zeros([self.verts.shape[0], 1])

        # get the vertex index of edges of triangles. numpy array with shape [n_f, 2].
        edge_v0v1 = self.faces[:, [0, 1]]  # edge of v0---v1
        edge_v0v2 = self.faces[:, [0, 2]]  # edge of v0---v2
        edge_v1v2 = self.faces[:, [1, 2]]  # edge of v1---v2

        # compute length of edges, numpy array, shape is (n_f, )
        length_edge_v0v1 = np.linalg.norm(self.verts[edge_v0v1[:, 0], :] - self.verts[edge_v0v1[:, 1], :], axis=1)
        length_edge_v0v2 = np.linalg.norm(self.verts[edge_v0v2[:, 0], :] - self.verts[edge_v0v2[:, 1], :], axis=1)
        length_edge_v1v2 = np.linalg.norm(self.verts[edge_v1v2[:, 0], :] - self.verts[edge_v1v2[:, 1], :], axis=1)

        # compute area of each triangle see the reference https://pythonguides.com/find-area-of-a-triangle-in-python/
        # faces_area is numpy array with shape: (n_f, )
        average_edge_len = (length_edge_v0v1 + length_edge_v0v2 + length_edge_v1v2) / 2.0
        faces_area = (average_edge_len * (average_edge_len - length_edge_v0v1) * (
                    average_edge_len - length_edge_v0v2) * (average_edge_len - length_edge_v1v2)) ** 0.5

        # compute the cot value of angle, the angle is face towards to edges.
        # cot value is numpy array with shape of (n_f, )
        cot_value_angle_face_v0v1 = (length_edge_v1v2 ** 2 + length_edge_v0v2 ** 2 - length_edge_v0v1 ** 2) / (
                    4 * faces_area)
        cot_value_angle_face_v0v2 = (length_edge_v1v2 ** 2 + length_edge_v0v1 ** 2 - length_edge_v0v2 ** 2) / (
                    4 * faces_area)
        cot_value_angle_face_v1v2 = (length_edge_v0v2 ** 2 + length_edge_v0v1 ** 2 - length_edge_v1v2 ** 2) / (
                    4 * faces_area)

        # sum the triangles' area of vertices belong to.
        # the sum_area_vert is numpy array, shape is (n_v, 1)
        for i in range(faces_area.shape[0]):
            sum_area_vert[self.faces[i, 0]] += faces_area[i]
            sum_area_vert[self.faces[i, 1]] += faces_area[i]
            sum_area_vert[self.faces[i, 2]] += faces_area[i]

        # cot laplacian matrix
        for j in range(edge_v0v1.shape[0]):
            lap_matrix[edge_v0v1[j, 0], edge_v0v1[j, 1]] += cot_value_angle_face_v0v1[j]
            lap_matrix[edge_v0v1[j, 1], edge_v0v1[j, 0]] += cot_value_angle_face_v0v1[j]
            lap_matrix[edge_v0v2[j, 0], edge_v0v2[j, 1]] += cot_value_angle_face_v0v2[j]
            lap_matrix[edge_v0v2[j, 1], edge_v0v2[j, 0]] += cot_value_angle_face_v0v2[j]
            lap_matrix[edge_v1v2[j, 0], edge_v1v2[j, 1]] += cot_value_angle_face_v1v2[j]
            lap_matrix[edge_v1v2[j, 1], edge_v1v2[j, 0]] += cot_value_angle_face_v1v2[j]

        lap_matrix_nonormalize = lap_matrix.copy()
        if area_normalize:
            # normalize wij with the size of Voronoi regions: 4A(i) = 0.5*sum_(k in N(i)) (cotαkj + cotβkj)|vi-vk|^2
            for k in range(self.verts.shape[0]):
                if sum_area_vert[k, :] != 0:
                    lap_matrix[k, :] = lap_matrix[k, :] / (sum_area_vert[k, :])
            lap_matrix = lap_matrix * -1
        else:
            # normalize wij with uniform value: sum_(k in N(i)) (cotαkj + cotβkj)
            lap_matrix = normalize(lap_matrix, norm='l1', axis=1)
            lap_matrix = lap_matrix * -1

        unit_diagonal = identity(self.verts.shape[0], dtype=np.float32)  # L[i,j] = 1, if i=j
        lap_matrix += unit_diagonal

        return lap_matrix
