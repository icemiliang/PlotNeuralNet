import os


def to_head(projectpath):
    pathlayers = os.path.join(projectpath, 'layers/').replace('\\', '/')
    return r"""
            \documentclass[border=8pt, multi, tikz]{standalone} 
            \usepackage{import}
            \subimport{""" + pathlayers + r"""}{init}
            \usetikzlibrary{positioning}
            \usetikzlibrary{3d} %for including external image 
            """


def to_cor():
    return r"""
            \def\ConvColor{rgb:yellow,5;red,2.5;white,5}
            \def\ConvReluColor{rgb:yellow,5;red,5;white,5}
            \def\PoolColor{rgb:red,1;black,0.3}
            \def\UnpoolColor{rgb:blue,2;green,1;black,0.3}
            \def\FcColor{rgb:blue,5;red,2.5;white,5}
            \def\FcReluColor{rgb:blue,5;red,5;white,4}
            \def\SoftmaxColor{rgb:magenta,5;black,7}   
            """


def to_begin():
    return r"""
            \newcommand{\copymidarrow}{\tikz \draw[-Stealth,line width=0.8mm,draw={rgb:blue,4;red,1;green,1;black,3}] 
            (-0.3,0) -- ++(0.3,0);}
            
            \begin{document}
            \begin{tikzpicture}
            \tikzstyle{connection}=[ultra thick,every node/.style={sloped,allow upside down},draw=\edgecolor,opacity=0.7]
            \tikzstyle{copyconnection}=[ultra thick,every node/.style={sloped,allow upside down},draw={rgb:blue,4;red,1;green,1;black,3},opacity=0.7]
            """


# layers definition
def to_input(pathfile, to='(-3,0,0)', width=8, height=8, name="temp"):
    return r"""
            \node[canvas is zy plane at x=0] (""" + name + """) at """ + to + """ {\includegraphics[width=""" + \
           str(width)+"cm" + """,height=""" + str(height)+"cm" + """]{""" + pathfile + """}};
            """


# Conv
def to_Conv(name, s_filer=256, n_filer=64, offset="(0,0,0)", to="(0,0,0)",
            width=1, height=40, depth=40, caption=" "):
    return r"""
            \pic[shift={""" + offset + """}] at """ + to + """ 
                {Box={
                    name=""" + name + """,
                    caption=""" + caption + r""",
                    xlabel={{""" + str(n_filer) + """, }},
                    zlabel=""" + str(s_filer) + """,
                    fill=\ConvColor,
                    height=""" + str(height) + """,
                    width=""" + str(width) + """,
                    depth=""" + str(depth) + """
                    }
                };
            """


# Conv
def to_ConvNew(name, s_filer=256, y_filer=256, n_filer=64, offset="(0,0,0)", to="(0,0,0)",
            width=1, height=40, depth=40, caption=" "):
    return r"""
            \pic[shift={""" + offset + """}] at """ + to + """ 
                {Box={
                    name=""" + name + """,
                    caption=""" + caption + r""",
                    xlabel={{""" + str(n_filer) + """, }},
                    ylabel=""" + str(y_filer) + """,
                    zlabel=""" + str(s_filer) + """,
                    fill=\ConvColor,
                    height=""" + str(height) + """,
                    width=""" + str(width) + """,
                    depth=""" + str(depth) + """
                    }
                };
            """


# Conv,Conv,relu
# Bottleneck
def to_ConvConvRelu(name, s_filer=256, n_filer=(64,64), offset="(0,0,0)", to="(0,0,0)",
                    width=(2, 2), height=40, depth=40, caption=" "):
    return r"""
            \pic[shift={ """ + offset + """ }] at """ + to + """ 
                {RightBandedBox={
                    name=""" + name + """,
                    caption=""" + caption + """,
                    xlabel={{ """ + str(n_filer[0]) + """, """ + str(n_filer[1]) + """ }},
                    zlabel=""" + str(s_filer) + """,
                    fill=\ConvColor,
                    bandfill=\ConvReluColor,
                    height=""" + str(height) + """,
                    width={ """ + str(width[0]) + """ , """ + str(width[1]) + """ },
                    depth=""" + str(depth) + """
                    }
                };
            """


# Pool
def to_Pool(name, offset="(0,0,0)", to="(0,0,0)", width=1, height=32, depth=32, opacity=0.5, caption=" "):
    return r"""
            \pic[shift={ """ + offset + """ }] at """ + to + """ 
                {Box={
                    name=""" +name+ """,
                    caption=""" + caption + r""",
                    fill=\PoolColor,
                    opacity=""" + str(opacity) + """,
                    height=""" + str(height) + """,
                    width=""" + str(width) + """,
                    depth=""" + str(depth) + """
                    }
                };
            """


# unpool4, 
def to_UnPool(name, offset="(0,0,0)", to="(0,0,0)", width=1, height=32, depth=32, opacity=0.5, caption=" "):
    return r"""
            \pic[shift={ """ + offset + """ }] at """ + to + """ 
                {Box={
                    name=""" + name + r""",
                    caption=""" + caption + r""",
                    fill=\UnpoolColor,
                    opacity=""" + str(opacity) + """,
                    height=""" + str(height) + """,
                    width=""" + str(width) + """,
                    depth=""" + str(depth) + """
                    }
                };
            """


def to_ConvRes(name, s_filer=256, n_filer=64, offset="(0,0,0)", to="(0,0,0)",
               width=6, height=40, depth=40, opacity=0.2, caption=" "):
    return r"""
            \pic[shift={ """ + offset + """ }] at """ + to + """ 
                {RightBandedBox={
                    name=""" + name + """,
                    caption=""" + caption + """,
                    xlabel={{ """ + str(n_filer) + """, }},
                    zlabel=""" + str(s_filer) + r""",
                    fill={rgb:white,1;black,3},
                    bandfill={rgb:white,1;black,2},
                    opacity=""" + str(opacity) + """,
                    height=""" + str(height) + """,
                    width=""" + str(width) + """,
                    depth=""" + str(depth) + """
                    }
                };
            """


def to_ConvResNew(name, s_filer=256, y_filer=256, n_filer=64, offset="(0,0,0)", to="(0,0,0)",
               width=6, height=40, depth=40, opacity=0.2, caption=" "):
    return r"""
            \pic[shift={ """ + offset + """ }] at """ + to + """ 
                {RightBandedBox={
                    name=""" + name + """,
                    caption=""" + caption + """,
                    xlabel={{ """ + str(n_filer) + """, }},
                    ylabel=""" + str(y_filer) + r""",
                    zlabel=""" + str(s_filer) + r""",
                    fill={rgb:white,1;black,3},
                    bandfill={rgb:white,1;black,2},
                    opacity=""" + str(opacity) + """,
                    height=""" + str(height) + """,
                    width=""" + str(width) + """,
                    depth=""" + str(depth) + """
                    }
                };
            """


# ConvSoftMax
def to_ConvSoftMax(name, s_filer=40, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, caption=" "):
    return r"""
            \pic[shift={""" + offset + """}] at """ + to + """ 
                {Box={
                    name=""" + name + """,
                    caption=""" + caption + """,
                    zlabel=""" + str(s_filer) + """,
                    fill=\SoftmaxColor,
                    height=""" + str(height) + """,
                    width=""" + str(width) + """,
                    depth=""" + str(depth) + """
                    }
                };
            """


# SoftMax
def to_SoftMax(name, s_filer=10, offset="(0,0,0)", to="(0,0,0)",
               width=1.5, height=3, depth=25, opacity=0.8, caption=" "):
    return r"""
            \pic[shift={""" + offset + """}] at """ + to + """ 
                {Box={
                    name=""" + name + """,
                    caption=""" + caption + """,
                    xlabel={{" ","dummy"}},
                    zlabel=""" + str(s_filer) + """,
                    fill=\SoftmaxColor,
                    opacity=""" + str(opacity) + """,
                    height=""" + str(height) + """,
                    width=""" + str(width) + """,
                    depth=""" + str(depth) + """
                    }
                };
            """


def to_connection(of, to):
    return r"""
            \draw [connection]  (""" + of + """-east)    -- node {\midarrow} (""" + to + """-west);
            """


def to_skipNew(of, to, pos=1.25):
    return r"""
            \path (""" + of + """-southeast) -- (""" + of + """-east) coordinate[pos=""" + str(pos) + """] (""" + of + """-top) ;
            \path (""" + to + """-south)  -- (""" + to + """-north)  coordinate[pos=""" + str(pos) + """] (""" + to + """-top) ;
            \draw [copyconnection]  (""" + of + """-east)  
            -- node {\copymidarrow}(""" + to + """-top)
            -- node {\copymidarrow} (""" + to + """-north);
            """


def to_skip(of, to, pos=1.25):
    return r"""
            \path (""" + of + """-southeast) -- (""" + of + """-northeast) coordinate[pos=""" + str(pos) + """] (""" + of + """-top) ;
            \path (""" + to + """-south)  -- (""" + to + """-north)  coordinate[pos=""" + str(pos) + """] (""" + to + """-top) ;
            \draw [copyconnection]  (""" + of + """-northeast)  
            -- node {\copymidarrow}(""" + of + """-top)
            -- node {\copymidarrow}(""" + to + """-top)
            -- node {\copymidarrow} (""" + to + """-north);
            """


def to_end():
    return r"""
            \end{tikzpicture}
            \end{document}
            """


def to_generate(arch, pathname="file.tex"):
    with open(pathname, "w") as f: 
        for c in arch:
            print(c)
            f.write(c)


# Conv,Conv,relu
# Bottleneck
def to_ConvRelu(name, s_filer=256, n_filer=64, offset="(0,0,0)", to="(0,0,0)",
                width=2, height=40, depth=40, caption=" "):
    return r"""
            \pic[shift={ """ + offset + """ }] at """ + to + """ 
                {RightBandedBox={
                    name=""" + name + """,
                    caption=""" + caption + """,
                    xlabel={{ """ + str(n_filer) + """ }},
                    zlabel=""" + str(s_filer) + """,
                    fill=\ConvColor,
                    bandfill=\ConvReluColor,
                    height=""" + str(height) + """,
                    width={ """ + str(width) + """ },
                    depth=""" + str(depth) + """
                    }
                };
            """


def to_ConvReluNew(name, s_filer=256, y_filer=256, n_filer=64, offset="(0,0,0)", to="(0,0,0)",
                width=2, height=40, depth=40, caption=" "):
    return r"""
            \pic[shift={ """ + offset + """ }] at """ + to + """ 
                {RightBandedBox={
                    name=""" + name + """,
                    caption=""" + caption + """,
                    xlabel={{ """ + str(n_filer) + """ }},
                    ylabel=""" + str(y_filer) + """,
                    zlabel=""" + str(s_filer) + """,
                    fill=\ConvColor,
                    bandfill=\ConvReluColor,
                    height=""" + str(height) + """,
                    width={ """ + str(width) + """ },
                    depth=""" + str(depth) + """
                    }
                };
            """


# define new block
def block_2ConvPool(name, botton, top, s_filer=256, n_filer=64, offset="(1,0,0)", size=(32, 32, 3.5), opacity=0.5):
    return '\n'.join([
        to_ConvConvRelu(
            name="ccr_{}".format(name),
            s_filer=str(s_filer),
            n_filer=(n_filer, n_filer),
            offset=offset,
            to="({}-east)".format(botton),
            width=(size[2], size[2]),
            height=size[0],
            depth=size[1],
            ),
        to_Pool(
            name="{}".format(top),
            offset="(0,0,0)",
            to="(ccr_{}-east)".format(name),
            width=1,
            height=size[0] - int(size[0]/4),
            depth=size[1] - int(size[0]/4),
            opacity=opacity, ),
        to_connection(
            "{}".format(botton),
            "ccr_{}".format(name)
            )
    ])


# define new block
def block_3ConvPool(name, botton, top, s_filer=256, n_filer=(64, 64, 64), offset="(1,0,0)", size=(32, 32, 3.5), opacity=0.5):
    return '\n'.join([
        to_ConvRes(name='ccr_res_{}'.format(name), offset=offset, to="(unpool_{}-east)".format(name),
                   s_filer=str(s_filer), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1],
                   opacity=opacity),
        to_Pool(
            name="{}".format( top ),
            offset="(0,0,0)",
            to="(ccr_{}-east)".format( name ),
            width=1,
            height=size[0] - int(size[0]/4),
            depth=size[1] - int(size[0]/4),
            opacity=opacity, ),
        to_connection(
            "{}".format(botton),
            "ccr_{}".format(name)
            )
    ])


def block_Unconv(name, botton, top, s_filer=256, n_filer=64, offset="(1,0,0)", size=(32,32,3.5), opacity=0.5):
    return '\n'.join([
        to_UnPool(name='unpool_{}'.format(name), offset=offset, to="({}-east)".format(botton),
                  width=1, height=size[0], depth=size[1], opacity=opacity),
        to_ConvRes(name='ccr_res_{}'.format(name), offset="(0,0,0)", to="(unpool_{}-east)".format(name),
                   s_filer=str(s_filer), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1],
                   opacity=opacity),
        to_Conv(name='ccr_{}'.format(name), offset="(0,0,0)", to="(ccr_res_{}-east)".format(name),
                s_filer=str(s_filer), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1]),
        to_ConvRes(name='ccr_res_c_{}'.format(name), offset="(0,0,0)", to="(ccr_{}-east)".format(name),
                   s_filer=str(s_filer), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1],
                   opacity=opacity),
        to_Conv(name='{}'.format(top), offset="(0,0,0)", to="(ccr_res_c_{}-east)".format(name),
                s_filer=str(s_filer), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1]),
        to_connection(
            "{}".format(botton),
            "unpool_{}".format(name)
            )
    ])


def block_Res(num, name, botton, top, s_filer=256, n_filer=64, offset="(0,0,0)", size=(32, 32, 3.5), opacity=0.5):
    lys = ''
    layers = [['{}_{}'.format(name, i) for i in range(num-1)], top]

    for name in layers:
        ly = '\n'.join([to_Conv(
            name='{}'.format(name),
            offset=offset,
            to="({}-east)".format(botton),
            s_filer=str(s_filer),
            n_filer=str(n_filer),
            width=size[2],
            height=size[0],
            depth=size[1],
            ),
            to_connection(
                "{}".format(botton),
                "{}".format(name)
                )
            ])
        botton = name
        lys += ly

    lys += to_skip(of=layers[1], to=layers[-2], pos=1.25)

    return lys
