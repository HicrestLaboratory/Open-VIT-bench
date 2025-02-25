import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from cvit_utils import plot_tensor
from timm.models.vision_transformer import Attention

print("Test Attention")

q = torch.tensor([[ 10.683,  89.343,   1.357,  96.640, -15.336,  25.409,  81.756,  70.704,  59.554],
                  [-15.408,   5.589,  40.406, -33.149,  87.516,  39.967, -16.463, -15.939,  52.466],
                  [-21.562,  61.519, -18.507, -85.862,  -4.034,   2.061,  41.918,  56.919,   4.792],
                  [ 23.872, -25.749, -11.222,   8.105, -89.181, -70.443, -97.221,  64.483,  -6.130],
                  [-71.273, -29.771, -69.692,  77.304, -41.330, -52.530, -82.077,  43.219,  77.663],
                  [ 34.523,  -5.194,  19.180, -21.882, -70.777,  39.502,  41.381,  93.513,  53.350],
                  [-76.041,  12.314,  60.924, -26.943,  54.629,  44.305, -16.375, -26.094,   8.616],
                  [ 36.569, -63.386, -91.981,  78.485, -39.200, -69.473,  -5.494,  38.069,  99.182],
                  [-39.245,   0.757,   7.034,   2.644,  35.657,  39.007,  12.231, -93.085,  20.562]])

k = torch.tensor([[-40.072,  -2.105,  27.082,  75.188,  62.613,  24.838, -80.834, -24.090, -57.363],
                  [-41.413, -96.189,  30.341,  50.168, -38.371,  96.502,  55.461,   4.063,  -5.361],
                  [ -6.208,  10.236,  59.886, -23.829, -48.915,  67.866, -71.103, -74.610, -84.870],
                  [ 95.320,  72.598, -21.577,  41.456,  72.554,  67.606,  56.197,  21.433,  92.993],
                  [ 67.088,  52.852, -82.890, -34.409,  91.781,  44.721,  80.905,  19.534,  15.171],
                  [ 34.538,  45.051,  41.691,   6.312, -72.914,  44.676,  40.149,  22.954, -44.347],
                  [ 89.788, -89.460,  16.085, -24.871, -63.189,  65.415,  93.307,  -5.767, -71.973],
                  [ 33.537, -68.666,  31.120,  36.170, -95.952,  80.698,  63.668,  54.968,  58.846],
                  [ 72.515,  25.198, -48.494,  62.938, -82.543, -42.199, -15.541,  30.660,  13.691]])

v = torch.tensor([[ 46.986,  36.217, -66.016,  15.741,  99.295, -33.009,  41.357, -99.659, -83.984],
                  [ 19.741,  41.692,  64.741, -27.820,  24.778,  32.410, -60.687,  55.242,  38.252],
                  [ 84.492, -67.885,  55.806,  62.139,  77.436,  51.055,  93.846,  71.584,  10.566],
                  [-11.748,  94.143, -83.041, -25.757,  -3.531,  37.203, -64.958, -31.857, -78.966],
                  [ 94.771, -75.157,  -0.000, -80.273,  12.879,  93.749, -22.231, -74.826, -43.230],
                  [-70.122,  88.141, -23.500, -55.115, -47.370,  20.998,  31.659,  70.931,  87.863],
                  [ 74.169,  46.647, -33.576,  54.161,  86.444,  47.087, -69.304,  85.867,  51.749],
                  [ 31.724,  99.774, -72.390,  11.810,  83.240,  51.025,   5.434, -20.235, -48.621],
                  [-63.371, -52.724, -54.284, -59.674,  -3.220,  63.446,  29.383,  78.809,  61.121]])

qb = torch.tensor([25.520, -55.048, 18.023, -67.021, -32.237, -48.541, 22.058, 44.724, 26.756])
kb = torch.tensor([-81.514, 22.635, -47.512, 39.962, 58.785, 17.168, 72.982, -23.437, -77.859])
vb = torch.tensor([98.347, 83.871, -21.256, -1.405, 26.923, 51.001, -32.017, 68.441, 66.097])

qkv = torch.cat((q, k, v), 0) # concatenation in channel dimension
print("### qkv")
plot_tensor(qkv)
qkv_b = torch.cat((qb, kb, vb), 0)
print("### qkv_b")
plot_tensor(qkv_b)

qng = torch.tensor([-0.142, -0.239, 0.876])
print("### qng")
plot_tensor(qng)
qnb = torch.tensor([-0.622, 0.738, -0.715])
print("### qnb")
plot_tensor(qnb)

kng = torch.tensor([0.261, -0.697, 0.582])
print("### kng")
plot_tensor(kng)
knb = torch.tensor([-0.585, -0.340, 0.959])
print("### knb")
plot_tensor(knb)

p = torch.tensor([[ 87.276, -20.017,  56.643, -49.470, -89.123,   6.129,  89.767,  96.505,  41.137],
                  [ 74.217,  93.854,  98.381,   5.639,  44.879,  90.131,  94.985, -52.945,  -0.943],
                  [ -5.100,  -5.592, -67.294,  83.153, -44.525,  22.836, -18.303, -28.262, -78.600],
                  [-58.353, -33.894, -30.743, -65.329,  85.584,  42.308,  58.404, -35.063, -67.784],
                  [-99.184, -69.551, -22.957,  88.280, -98.521,  23.592,   5.139,  72.286, -70.658],
                  [ 32.686, -52.631,  84.961,  88.724, -60.253, -37.420,  90.035, -72.894,  67.491],
                  [-69.409,  32.986,  48.424,  28.448, -67.917, -64.531, -58.772, -87.479,  -5.406],
                  [-66.338,  88.649, -58.952,  22.904, -38.855,  64.769,  70.668,  -0.777,  91.613],
                  [ 56.344, -27.664, -76.090,   1.096, -10.926,  69.634,  42.049, -10.555,  13.941]])
print("### p")
plot_tensor(p)

pb = torch.tensor([39.776, 40.790, 49.829, -97.071, 2.287, 40.050, 57.575, 55.555, -77.701])
print("### pb")
plot_tensor(pb)

attn = Attention(
    dim=9, num_heads=3, qkv_bias=True, qk_norm=True, attn_drop=0.0,
    proj_drop=0.0, norm_layer=nn.LayerNorm)
attn.qkv.weight.data = qkv
attn.qkv.bias.data = qkv_b
attn.q_norm.weight.data = qng
attn.q_norm.bias.data = qnb
attn.k_norm.weight.data = kng
attn.k_norm.bias.data = knb
attn.proj.weight.data = p
attn.proj.bias.data = pb

x = torch.tensor([[[ -0.703,  -0.155,   0.869,  -0.876,  -0.116,   0.148,  -0.865,  -0.431,  -0.442],
                   [  0.335,   0.172,   0.187,  -0.907,   0.904,  -0.837,  -0.622,   0.454,  -0.883],
                   [ -0.464,   0.737,  -0.623,   0.004,  -0.188,   0.945,  -0.351,  -0.552,   0.301],
                   [  0.760,   0.513,   0.895,  -0.060,   0.869,  -0.955,  -0.402,  -0.071,  -0.962],
                   [ -0.832,  -0.235,   0.727,  -0.438,   0.710,  -0.460,  -0.787,   0.725,  -0.743],
                   [ -0.889,   0.982,   0.762,  -0.097,   0.207,  -0.988,  -0.610,   0.722,   0.416],
                   [  0.038,  -0.314,   0.475,  -0.502,   0.638,  -0.355,  -0.609,  -0.231,  -0.272]],

                  [[  0.533,  -0.786,  -0.958,   0.928,  -0.281,   0.966,   0.095,   0.865,   0.446],
                   [ -0.912,   0.476,   0.139,  -0.204,  -0.546,   0.614,   0.496,   0.985,   0.227],
                   [  0.564,  -0.304,  -0.318,   0.477,   0.369,   0.052,   0.042,   0.076,  -0.579],
                   [  0.265,  -0.826,  -0.396,  -0.484,   0.481,  -0.182,   0.770,  -0.362,  -0.601],
                   [  0.806,   0.902,  -0.803,   0.431,  -0.398,  -0.146,  -0.262,   0.269,  -0.887],
                   [ -0.026,  -0.604,  -0.381,   0.490,   0.022,   0.256,  -0.408,  -0.321,   0.330],
                   [ -0.307,  -0.789,  -0.262,   0.662,  -0.323,  -0.478,  -0.487,  -0.490,   0.682]]])
print("### x")
plot_tensor(x)

y = attn.forward(x)
print("### y = attn(x)")
plot_tensor(y)
