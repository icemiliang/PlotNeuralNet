import sys
sys.path.append('../')
from pycore.tikzeng import *

width = 3.5

arch = [ 
    to_head('..'), 
    to_cor(),
    to_begin(),

    to_input('../examples/fcn8s/cats.jpg', to="(-5, 0, 0)", width=6.5, height=6.5),
    to_input('../examples/fcn8s/cats.jpg', to="(-5, 10, 0)", width=6.5, height=6.5),

    to_ConvReluNew(name='cr_a0', s_filer=304, y_filer=224, n_filer=64, offset="(-2, 10, 0)", to="(0,0,0)", width=4, height=32, depth=32),


    to_ConvReluNew(name='cr_b0', s_filer=304, y_filer=224, n_filer=64, offset="(-2, 0, 0)", to="(0, 0, 0)", width=4, height=32, depth=32),
    to_ConvRelu(name='cr_a00', s_filer=500, n_filer=64, offset="(0, 0, 0)", to="(cr_b0-east)", width=4, height=32, depth=32),
    to_skipNew(of='cr_a0', to="cr_a00", pos=2),

    # conv1
    to_ConvReluNew(
        name="cr_{}".format('b1'), offset="(1, 0, 0)", to="(0,0, 0)".format('b0'),
        s_filer=152, y_filer=112, n_filer=256, width=width, height=32, depth=32,
    ),
    to_Pool(
        name="{}".format('pool_b1'), offset="(0,0,0)", to="(cr_{}-east)".format('b1'),
        width=1, height=int(32 * 3 / 4), depth=int(32 * 3 / 4), opacity=0.5
    ),

    # conv2
    to_ConvReluNew(
        name="cr_{}".format('b2'), offset="(1, 0, 0)", to="({}-east)".format('pool_b1'),
        s_filer=256, n_filer=512, width=width, height=25, depth=25,
    ),
    to_Pool(
        name="{}".format('pool_b2'), offset="(0,0,0)", to="(cr_{}-east)".format('b2'),
        width=1, height=int(25 * 3 / 4), depth=int(25 * 3 / 4), opacity=0.5
    ),

    # conv3
    to_ConvReluNew(
        name="cr_{}".format('b3'), offset="(1, 0, 0)", to="({}-east)".format('pool_b2'),
        s_filer=256, n_filer=1024, width=width, height=20, depth=20,
    ),
    to_Pool(
        name="{}".format('pool_b3'), offset="(0,0,0)", to="(cr_{}-east)".format('b3'),
        width=1, height=int(20 * 3 / 4), depth=int(20 * 3 / 4), opacity=0.5
    ),

    # conv4
    to_ConvReluNew(
        name="cr_{}".format('b4'), offset="(1, 0, 0)", to="({}-east)".format('pool_b3'),
        s_filer=256, n_filer=2048, width=width, height=16, depth=16,
    ),
    to_Pool(
        name="{}".format('pool_b4'), offset="(0,0,0)", to="(cr_{}-east)".format('b4'),
        width=1, height=int(16 * 3 / 4), depth=int(16 * 3 / 4), opacity=0.5
    ),

    # to_skipNew(of='cr_c0', to="b0", pos=1.3),
    # to_skipNew1(of='cr_c0', to="b0", pos=1.3),


    # to_connection("{}".format('cr_a0'), "b00"),
    to_connection("{}".format('cr_a00'), "cr_{}".format('b1')),
    to_connection("{}".format('pool_b1'), "cr_{}".format('b2')),
    to_connection("{}".format('pool_b2'), "cr_{}".format('b3')),
    to_connection("{}".format('pool_b3'), "cr_{}".format('b4')),

    # Bottleneck
    # block-005
    to_ConvReluNew(name='cr_b5', s_filer=32, n_filer=512, offset="(1,0,0)", to="(pool_b4-east)", width=8, height=8, depth=8, caption="Bottleneck"),
    to_connection("pool_b4", "cr_b5"),

    # Decoder
    # convt2
    to_UnPool(name='unpool_{}'.format('b6'), offset="(1.5,0,0)", to="({}-east)".format('cr_b5'),
                  width=1, height=16, depth=16, opacity=0.5),
    to_ConvRes(name='cr_res_{}'.format('b6'), offset="(0,0,0)", to="(unpool_{}-east)".format('b6'),
               s_filer=64, n_filer=2048, width=width, height=16, depth=16,
               opacity=0.5),
    to_Conv(name='cr_{}'.format('b6'), offset="(0,0,0)", to="(cr_res_{}-east)".format('b6'),
            s_filer=64, n_filer=2048, width=width, height=16, depth=16),

    # convt3
    to_UnPool(name='unpool_{}'.format('b7'), offset="(1.5, 0, 0)", to="({}-east)".format('cr_b6'),
              width=1, height=20, depth=20, opacity=0.5),
    to_ConvRes(name='cr_res_{}'.format('b7'), offset="(0, 0, 0)", to="(unpool_{}-east)".format('b7'),
               s_filer=128, n_filer=1024, width=width, height=20, depth=20, opacity=0.5),
    to_Conv(name='cr_{}'.format('b7'), offset="(0,0,0)", to="(cr_res_{}-east)".format('b7'),
            s_filer=128, n_filer=1024, width=width, height=20, depth=20),

    # convt4
    to_UnPool(name='unpool_{}'.format('b8'), offset="(1.5, 0, 0)", to="({}-east)".format('cr_b7'),
              width=1, height=25, depth=25, opacity=0.5),
    to_ConvRes(name='cr_res_{}'.format('b8'), offset="(0, 0, 0)", to="(unpool_{}-east)".format('b8'),
               s_filer=256, n_filer=512, width=width, height=25, depth=25, opacity=0.5),
    to_Conv(name='cr_{}'.format('b8'), offset="(0,0,0)", to="(cr_res_{}-east)".format('b8'),
            s_filer=256, n_filer=512, width=width, height=25, depth=25),

    # convt5
    to_UnPool(name='unpool_{}'.format('b9'), offset="(1.5, 0, 0)", to="({}-east)".format('cr_b8'),
              width=1, height=32, depth=32, opacity=0.5),
    to_ConvRes(name='cr_res_{}'.format('b9'), offset="(0, 0, 0)", to="(unpool_{}-east)".format('b9'),
               s_filer=256, n_filer=256, width=width, height=32, depth=32, opacity=0.5),
    to_Conv(name='cr_{}'.format('b9'), offset="(0,0,0)", to="(cr_res_{}-east)".format('b9'),
            s_filer=256, n_filer=256, width=width, height=32, depth=32),

    # convt6
    to_UnPool(name='unpool_{}'.format('b10'), offset="(1.5, 0, 0)", to="({}-east)".format('cr_b9'),
              width=1, height=32, depth=32, opacity=0.5),
    to_ConvRes(name='cr_res_{}'.format('b10'), offset="(0, 0, 0)", to="(unpool_{}-east)".format('b10'),
               s_filer=256, n_filer=64, width=width, height=32, depth=32, opacity=0.5),
    to_Conv(name='cr_{}'.format('b10'), offset="(0,0,0)", to="(cr_res_{}-east)".format('b10'),
            s_filer=256, n_filer=64, width=width, height=32, depth=32),

    to_ConvRelu(name="last", s_filer=1, n_filer=1, offset="(0.75,0,0)", to="(cr_b10-east)", width=4, height=32, depth=32),

    to_skip(of='cr_b4', to='cr_b6', pos=1.35),
    to_skip(of='cr_b3', to='cr_b7', pos=1.35),
    to_skip(of='cr_b2', to='cr_b8', pos=1.35),
    to_skip(of='cr_b1', to='cr_b9', pos=1.35),
    to_skip(of='cr_a00', to='cr_b10', pos=1.55),

    to_connection("cr_{}".format('b5'), "unpool_{}".format('b6')),
    to_connection("cr_{}".format('b6'), "unpool_{}".format('b7')),
    to_connection("cr_{}".format('b7'), "unpool_{}".format('b8')),
    to_connection("cr_{}".format('b8'), "unpool_{}".format('b9')),
    to_connection("cr_{}".format('b9'), "unpool_{}".format('b10')),
    to_connection("cr_b10", "last"),


    to_end() 
    ]


if __name__ == '__main__':
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex')

