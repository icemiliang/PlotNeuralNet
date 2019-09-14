import sys
sys.path.append('../')
from pycore.tikzeng import *

width = 3.5

arch = [ 
    to_head('..'), 
    to_cor(),
    to_begin(),

    to_input('./icra/rgb.png', to="(-10, 0, 0)", width=6.5, height=6.5),
    to_ConvReluNewColor(name='cr_a0', s_filer=304, y_filer=224, n_filer=64, offset="(-8, 0, 0)", to="(0,0,0)", width=4, height=32, depth=32),

    to_input('./icra/sparse_depth.png', to="(-4, 0, 0)", width=6.5, height=6.5),
    to_ConvReluNewColor(name='cr_b0', s_filer=304, y_filer=224, n_filer=64, offset="(-2, 0, 0)", to="(0, 0, 0)", width=4, height=32, depth=32),
    to_ConvRelu(name='cr_a00', s_filer=304, n_filer=64, offset="(0, 0, 0)", to="(cr_b0-east)", width=4, height=32, depth=32),
    to_skip(of='cr_a0', to="cr_a00", pos=1.4),

    # conv1
    to_ConvReluNew(
        name="cr_{}".format('b1'), offset="(1.5, 0, 0)", to="(0,0, 0)".format('b0'),
        s_filer=304, y_filer=224, n_filer=256, width=width*1.2, height=32, depth=32,
    ),
    to_Pool(
        name="{}".format('pool_b1'), offset="(0,0,0)", to="(cr_{}-east)".format('b1'),
        width=1, height=int(32 * 3 / 4), depth=int(32 * 3 / 4), opacity=0.5
    ),

    # conv2
    to_ConvReluNew(
        name="cr_{}".format('b2'), offset="(1.5, 0, 0)", to="({}-east)".format('pool_b1'),
        s_filer=152, y_filer=112, n_filer=512, width=width*1.5, height=25, depth=25,
    ),

    to_Pool(
        name="{}".format('pool_b2'), offset="(0,0,0)", to="(cr_{}-east)".format('b2'),
        width=1, height=int(25 * 3 / 4), depth=int(25 * 3 / 4), opacity=0.5
    ),

    # conv3
    to_ConvReluNew(
        name="cr_{}".format('b3'), offset="(1.5, 0, 0)", to="({}-east)".format('pool_b2'),
        s_filer=76, y_filer=56, n_filer=1024, width=width*1.8, height=20, depth=20,
    ),
    to_Pool(
        name="{}".format('pool_b3'), offset="(0,0,0)", to="(cr_{}-east)".format('b3'),
        width=1, height=int(20 * 3 / 4), depth=int(20 * 3 / 4), opacity=0.5
    ),

    # conv4
    to_ConvReluNew(
        name="cr_{}".format('b4'), offset="(1.5, 0, 0)", to="({}-east)".format('pool_b3'),
        s_filer=38, y_filer=28, n_filer=2048, width=width*2, height=16, depth=16,
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
    to_ConvReluNewColor(name='cr_b5', s_filer=19, y_filer=14, n_filer=512, offset="(1.5,0,0)", to="(pool_b4-east)", width=width*2.2, height=8, depth=8, caption=""),
    to_connection("pool_b4", "cr_b5"),

    # Decoder
    # convt2
    to_UnPoolNew(name='unpool_{}'.format('b6'), offset="(2.0,0,0)", to="({}-east)".format('cr_b5'),
                 y_filer=28, width=1, height=16,  depth=16, opacity=0.5),
    to_ConvResSimple(name='cr_res_{}'.format('b6'), offset="(0,0,0)", to="(unpool_{}-east)".format('b6'),
                     n_filer=2048, width=width*2, height=16, depth=16,
                     opacity=0.5),
    to_ConvReluSimple(name='cr_{}'.format('b6'), offset="(0,0,0)", to="(cr_res_{}-east)".format('b6'),
                      s_filer=64, n_filer=2048, width=width*2, height=16, depth=16),

    # convt3
    to_UnPoolNew(name='unpool_{}'.format('b7'), offset="(1.2, 0, 0)", to="({}-east)".format('cr_b6'),
                 y_filer=56, width=1, height=20, depth=20, opacity=0.5),
    to_ConvResSimple(name='cr_res_{}'.format('b7'), offset="(0, 0, 0)", to="(unpool_{}-east)".format('b7'),
                     n_filer=1024, width=width*1.8, height=20, depth=20, opacity=0.5),
    to_ConvReluSimple(name='cr_{}'.format('b7'), offset="(0,0,0)", to="(cr_res_{}-east)".format('b7'),
                      s_filer=128, n_filer=1024, width=width*1.8, height=20, depth=20),

    # convt4
    to_UnPoolNew(name='unpool_{}'.format('b8'), offset="(1.5, 0, 0)", to="({}-east)".format('cr_b7'),
                 y_filer=112, width=1, height=25, depth=25, opacity=0.5),
    to_ConvResSimple(name='cr_res_{}'.format('b8'), offset="(0, 0, 0)", to="(unpool_{}-east)".format('b8'),
                     n_filer=512, width=width*1.5, height=25, depth=25, opacity=0.5),
    to_ConvReluSimple(name='cr_{}'.format('b8'), offset="(0,0,0)", to="(cr_res_{}-east)".format('b8'),
                      s_filer=256, n_filer=512, width=width*1.5, height=25, depth=25),

    # convt5
    to_UnPoolNew(name='unpool_{}'.format('b9'), offset="(2, 0, 0)", to="({}-east)".format('cr_b8'),
                 y_filer=224, width=1, height=32, depth=32, opacity=0.5),
    to_ConvResSimple(name='cr_res_{}'.format('b9'), offset="(0, 0, 0)", to="(unpool_{}-east)".format('b9'),
                     n_filer=256, width=width*1.2, height=32, depth=32, opacity=0.5),
    to_ConvReluSimple(name='cr_{}'.format('b9'), offset="(0,0,0)", to="(cr_res_{}-east)".format('b9'),
                      s_filer=256, n_filer=256, width=width*1.2, height=32, depth=32),

    # convt6
    to_UnPoolNew(name='unpool_{}'.format('b10'), offset="(2, 0, 0)", to="({}-east)".format('cr_b9'),
                 y_filer=224, width=1, height=32, depth=32, opacity=0.5),
    to_ConvResSimple(name='cr_res_{}'.format('b10'), offset="(0, 0, 0)", to="(unpool_{}-east)".format('b10'),
                     n_filer=64, width=width, height=32, depth=32, opacity=0.5),
    to_ConvReluSimple(name='cr_{}'.format('b10'), offset="(0,0,0)", to="(cr_res_{}-east)".format('b10'),
                      s_filer=256, n_filer=64, width=width, height=32, depth=32),

    to_ConvReluNew(name="last", s_filer=304, y_filer=224, n_filer=1, offset="(2.5,0,0)", to="(cr_b10-east)",
                   width=4, height=32, depth=32),
    to_SoftMaxNew(name="d2n", s_filer=304, y_filer=224, n_filer=3, offset="(2.5, 0, 0)", to="(last-east)",
                  width=4, height=32, depth=32, opacity=0.5),
    

    to_skip(of='cr_b4', to='cr_b6', pos=1.25),
    to_skip(of='cr_b3', to='cr_b7', pos=1.25),
    to_skip(of='cr_b2', to='cr_b8', pos=1.25),
    to_skip(of='cr_b1', to='cr_b9', pos=1.25),
    to_skip(of='cr_a00', to='cr_b10', pos=1.4),

    to_connection("cr_{}".format('b5'), "unpool_{}".format('b6')),
    to_connection("cr_{}".format('b6'), "unpool_{}".format('b7')),
    to_connection("cr_{}".format('b7'), "unpool_{}".format('b8')),
    to_connection("cr_{}".format('b8'), "unpool_{}".format('b9')),
    to_connection("cr_{}".format('b9'), "unpool_{}".format('b10')),
    to_connection("cr_b10", "last"),


    to_input('./icra/estimated_depth.png', to="(last-east)", width=6.5, height=6.5),
    to_connection("last", "d2n"),
    to_input('./icra/estimated_normal.png', to="(d2n-east)", width=6.5, height=6.5),

    to_UnPool(name='legend_unpool', offset="(-12, 10, 0)", to="(unpool_{}-east)".format('b9'),
              width=1, height=16, depth=16, opacity=0.5, caption="Unpooling"),

    to_ConvReluNewColorLegend(name='legend_conv', offset="(3, 0,0)", to="(legend_unpool-east)",
                              width=4, height=16, depth=16, caption="Convolution"),

    to_ConvResSimpleSimple(name='legend_deconv', offset="(3, 0, 0)", to="(legend_conv-east)".format('d10'),
                           width=width, height=16, depth=16, opacity=0.5, caption="Deconvolution"),

    to_ConvSimple(name='legend_resnet'.format('d10'), offset="(3, 0, 0)", to="(legend_deconv-east)".format('d10'),
                  width=width, height=16, depth=16, caption="ResNet Block"),

    to_Pool(name='legend_pool', offset="(3, 0, 0)", to="(legend_resnet-east)", width=1, height=16, depth=16, opacity=0.5, caption="Pooling"),

    to_relu(name='legend_relu', offset="(3, 0, 0)", to="(legend_pool-east)", width=1, height=16, depth=16, opacity=0.5, caption="ReLU"),

    to_SoftMaxSimple(name="d2n", offset="(2.5, 0, 0)", to="(legend_relu-east)",
                     width=4, height=16, depth=16, opacity=0.5, caption="d2n"),

    to_end() 
        ]


if __name__ == '__main__':
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex')

