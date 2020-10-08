'''
Created on: ********

Author: Yi Zheng, Department of Electrical Engineering, DTU

Some confused syntax is tested in this file.
'''


# Understanding multiple inheritance
# class Base(object):
#     def __init__(self):
#         print ("enter Base")
#         print ("leave Base")
# 
# class A(Base):
#     def __init__(self):
#         print ('enter A')
#         Base().__init__()
#         print ('leave A')
# 
# class B(Base):
#     def __init__(self):
#         print ('enter B')
#         Base().__init__()
#         print ('leave B')
# 
# class C(A, B):
#     def __init__(self):
#         print ('enter C')
#         A().__init__()
#         B().__init__()
#         print ('leave C')

class Base(object):
    def __init__(self):
        print("enter Base")
        print("leave Base")


class A(Base):
    def __init__(self):
        self.name = 'Jerry'
        print('enter A')
        super().__init__()
        print('leave A')


class B(Base):
    def __init__(self):
        print('enter B')
        super().__init__()
        print('leave B')


class C(A, B):
    def __init__(self):
        print('enter C')
        super(C, self).__init__()
        print('leave C')

class D(A):
    love = 1
    def __init__(self):
        self.name = 'Tom'

class NoInit():
    def greeting(self):
        print('hi')


def HSL2RGB(h, s, l):
    u"HSL -> RGB，返回一个元组，格式为：(r, g, b)"

    if s > 0:
        v_1_3 = 1.0 / 3
        v_1_6 = 1.0 / 6
        v_2_3 = 2.0 / 3

        q = l * (1 + s) if l < 0.5 else l + s - (l * s)
        p = l * 2 - q
        hk = h / 360.0  # h 规范化到值域 [0, 1) 内
        tr = hk + v_1_3
        tg = hk
        tb = hk - v_1_3

        rgb = [
            tc + 1.0 if tc < 0 else
            tc - 1.0 if tc > 1 else
            tc
            for tc in (tr, tg, tb)
        ]

        rgb = [
            p + ((q - p) * 6 * tc) if tc < v_1_6 else
            q if v_1_6 <= tc < 0.5 else
            p + ((q - p) * 6 * (v_2_3 - tc)) if 0.5 <= tc < v_2_3 else
            p
            for tc in rgb
        ]

        rgb = tuple(int(i * 256) for i in rgb)

    # s == 0 的情况
    else:
        rgb = 1, 1, 1

    return rgb
import numpy as np
import math
from scipy.stats import weibull_min, rv_continuous
# Test self-defined random variables
class gaussian_gen(rv_continuous):
    def _pdf(self, x):
        return np.exp(-x**2/2.)/np.sqrt(2.0*np.pi)

if __name__ == '__main__':
    test = 10
    if test == 1:
        # Multiple inheritance
        C()
        # -
        d = D()
        print(D.love)
        print(d.name)
    elif test == 10:
        # pso
        def myfun(x):
            x1 = x[0]
            x2 = x[1]
            return x1**2 +x2**2
        def mycon(x):
            x1 = x[0]
            x2 = x[1]
            return [x1**2-10,math.exp(x2)-6e6]
        from pyswarm import pso
        g,fg = pso(myfun, [2,6],[100,100],f_ieqcons=mycon)
        print(f'Extreme point is {g} and corresponding value is {fg}')

    elif test == 9:
        # decorator and partial function
        from functools import wraps

        def decorator(func):
            @wraps(func)
            def new_func(*args):
                print('Hi, xiongdi')
                print('Jianghu')
                return(func(*args)+10)
            return new_func


        # @decorator
        def sum(*args):
            s = 0
            for i in args:
                s = s+i
            return s

        print(sum(2,3,4,5))
        print(sum.__name__)

        from functools import partial


        def sum(*args):
            s = 0
            for n in args:
                s = s + n
            return s


        sum_add_10 = partial(sum, 10)  # 10 作用在sum第一个参数的位置
        sum_add_10_20 = partial(sum, 10, 20)  # 10 20 分别作用在sum第一个和第二个参数的位置
        print('A____________我们看下原函数sum的函数地址入口：')
        print(sum)
        print('B______我们看下partial函数返回函数的地址入口：')
        print(partial(sum, 10))
        print(sum_add_10(1, 2, 3, 4, 5))  # --> 10 + 1 + 2 + 3 + 4 + 5 = 25
        print(sum_add_10_20(1, 2, 3, 4, 5))  # --> 10 + 20 + 1 + 2 + 3 + 4 + 5 = 45

    elif test == 2:
        # lambda function lambda arguments: return value
        plus_one = lambda x: x + 1
        print(plus_one(3))
        # This is not a good way to define a function. It should only be used when you don't need a named function.
    elif test == 3:
        a = NoInit()
        a.greeting()
    elif test == 4:
        # np.random.seed(seed=1)
        a = np.random.uniform()
        b = np.random.weibull(4)
        # Simulating wind speed via weibull distribution
        n = 1  # number of samples
        k = 2  # shape factor should be calculated from the wind data, not available now
        lam = 5  # scale,should be calculated from the wind data, not available now
        v_wind = weibull_min.rvs(k, loc=0, scale=lam, size=n)
    elif test == 5:
        # Show alternative colors
        from matplotlib.patches import Rectangle
        import matplotlib.pyplot as plt
        import matplotlib.colors as mcolors


        def plot_colortable(colors, title, sort_colors=True, emptycols=0):

            cell_width = 212
            cell_height = 22
            swatch_width = 48
            margin = 12
            topmargin = 40

            # Sort colors by hue, saturation, value and name.
            if sort_colors is True:
                by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgb(color))),
                                 name)
                                for name, color in colors.items())
                names = [name for hsv, name in by_hsv]
            else:
                names = list(colors)

            n = len(names)
            ncols = 4 - emptycols
            nrows = n // ncols + int(n % ncols > 0)

            width = cell_width * 4 + 2 * margin
            height = cell_height * nrows + margin + topmargin
            dpi = 72

            fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)
            fig.subplots_adjust(margin / width, margin / height,
                                (width - margin) / width, (height - topmargin) / height)
            ax.set_xlim(0, cell_width * 4)
            ax.set_ylim(cell_height * (nrows - 0.5), -cell_height / 2.)
            ax.yaxis.set_visible(False)
            ax.xaxis.set_visible(False)
            ax.set_axis_off()
            ax.set_title(title, fontsize=24, loc="left", pad=10)

            for i, name in enumerate(names):
                row = i % nrows
                col = i // nrows
                y = row * cell_height

                swatch_start_x = cell_width * col
                text_pos_x = cell_width * col + swatch_width + 7

                ax.text(text_pos_x, y, name, fontsize=14,
                        horizontalalignment='left',
                        verticalalignment='center')

                ax.add_patch(
                    Rectangle(xy=(swatch_start_x, y - 9), width=swatch_width,
                              height=18, facecolor=colors[name])
                )

            return fig


        plot_colortable(mcolors.BASE_COLORS, "Base Colors",
                        sort_colors=False, emptycols=1)
        plot_colortable(mcolors.TABLEAU_COLORS, "Tableau Palette",
                        sort_colors=False, emptycols=2)

        plot_colortable(mcolors.CSS4_COLORS, "CSS Colors")

        # Optionally plot the XKCD colors (Caution: will produce large figure)
        # xkcd_fig = plot_colortable(mcolors.XKCD_COLORS, "XKCD Colors")
        # xkcd_fig.savefig("XKCD_Colors.png")

        plt.show()
    elif test == 6:
        # play with this argument **kwargs
        def print_list(**kwargs):
            print(kwargs)
            for i in kwargs.values():
                print(i)
            try:
                a = kwargs['c']
                return a
            except KeyError:
                print('Undefined keyword')
        print(print_list( b = 34, a = 35))
        pass
    elif test == 7:
        # 3D plot
        import matplotlib.pyplot as plt
        import numpy as np

        # Fixing random state for reproducibility
        np.random.seed(19680801)


        def randrange(n, vmin, vmax):
            """
            Helper function to make an array of random numbers having shape (n, )
            with each number distributed Uniform(vmin, vmax).
            """
            return (vmax - vmin) * np.random.rand(n) + vmin


        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        n = 100

        # For each set of style and range settings, plot n random points in the box
        # defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
        for m, zlow, zhigh in [('o', -50, -25), ('^', -30, -5)]:
            xs = randrange(n, 23, 32)
            ys = randrange(n, 0, 100)
            zs = randrange(n, zlow, zhigh)
            ax.scatter(xs, ys, zs, marker=m)

        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        plt.show()
    elif test == 8:
        a = HSL2RGB(0.1,0.2,0.15)
        print(a)