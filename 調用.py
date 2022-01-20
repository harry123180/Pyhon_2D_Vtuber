import LMP as lp
import numpy as np
import sksparse.cholmod import cholesky_AAt


def demo(verts, faces, idx_verts, vert_anchor, idx_anchor_in_mesh):
    # verts是顶点 numpy 数组 ：[nv, 3], nv是顶点数量
    # faces是面片 numpy 数组： [nf, 3]，nf是面片数量
    # idx_verts ： verts顶点的索引 可以用 np.arrange(verts.shape[0])表示
    # vert_anchor: verts中锚点将要变换到新的位置（欧式坐标系）
    # idx_anchor_in_mesh： 锚点在idx_verts中的索引
    lap = LapMeshDeform(verts, faces)
    L = lap.uniform_laplacian()
    # L  = lap.cot_laplacian(area_normalize=False)
    verts_sparse = sparse.lil_matrix(verts)
    # delta矩阵
    delta = L.dot(verts_sparse)

    # add anchor points
    # 锚点在整体网格索引idx_verts中的索引
    real_idx = idx_verts[idx_anchor_in_mesh]

    # 锚点约束项权重
    w_anchor = 0.6
    # 拉普拉斯矩阵的锚点
    L_anchor = sparse.lil_matrix((vert_anchor.shape[0], verts.shape[0]), dtype=np.float32)
    for i in range(real_idx.shape[0]):
        L_anchor[i, real_idx[i]] = w_anchor
    L_anchor = L_anchor.tocsr()

    # δ矩阵的锚点
    delta_anchor = vert_anchor * w_anchor
    delta_anchor = sparse.csr_matrix(delta_anchor)

    # 构造矩阵A
    A = vstack((L, L_anchor))
    # 构造矩阵B
    B = vstack((delta, delta_anchor))
    # B = sparse.lil_matrix(B)

    # 解超定线性方程
    factor = cholesky_AAt(A.T)
    x = factor(A.T * B)

    # new_verts就是最终形变结果
    new_verts = x.toarray()
    return new_verts
