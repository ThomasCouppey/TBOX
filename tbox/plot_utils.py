"""Matplotlib plotting helpers and style constants."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch
from matplotlib.legend_handler import HandlerTuple
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, to_rgba
from matplotlib.transforms import Affine2D
from matplotlib.path import Path
from matplotlib.figure import SubFigure
from matplotlib import font_manager

__all__ = [
    "COLOR_MODEL",
    "on_color",
    "off_color",
    "u_color",
    "m_color",
    "ax_color",
    "mod_colors",
    "c_kwgs",
    "f_kwgs",
    "f_kwgs2",
    "c_kwgs_small",
    "f_kwgs_small",
    "f_kwgs2_small",
    "compute_alpha",
    "set_plt_Raleway",
    "set_plt",
    "set_axes",
    "set_zeros_axis",
    "valid_diameter",
    "plot_config",
    "set_axis_param",
    "add_fancy_frame",
    "HandlerTupleVertical",
    "gradient_image_custom",
    "linear_cmap",
    "rainbowarrow",
]

COLOR_MODEL = {
    "HH": "#F9DEDE",
    'Rattay_Aberham': "#75140C",
    'Sundt': "#A4312A",
    'Tigerholm': "#EA3322",
    'Schild_94': "#E78E80",
    'Schild_97': "#F2A683",
    'MRG': "#000085",
    'Gaines_motor': "#458EF7",
    'Gaines_sensory': "#6F94E5",
}


def set_plt_Raleway():
    """Configure Matplotlib to use a local Raleway font installation."""
    font_dirs = ['/Users/thomascouppey/Documents/Fonts/Raleway/']
    font_files = font_manager.findSystemFonts(fontpaths=font_dirs)

    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)

    plt.rcParams['font.family'] = "Raleway"
    plt.rcParams.update({\
    "font.size": 15,\
    })

def set_plt(font_size=12,**kwgs):
    """Apply the default TBOX Matplotlib style.

    Parameters
    ----------
    font_size : int or float, default=12
        Base Matplotlib font size.
    **kwgs
        Additional ``matplotlib.rcParams`` values to override after applying
        the default style.
    """
    plt.rcParams.update({\
    "text.usetex": True,\
    "font.family": "serif",\
    "font.serif": ["Palatino"],\
    "font.size": font_size,\
    "font.weight":"bold",\
    "axes.labelweight":"bold",\
    
    })
    plt.rcParams.update(kwgs)



## Variables
on_color = "#99FF33"
off_color = "#EDB170"
u_color = "#CE0000"
m_color = "#004C99"
ax_color = "#880088"


mod_colors = {
    "3D": "#9673A6",
    "single_val": "#99004C",
    "avg_ind": "#990099",
    "2Davg_ind": "#004C99",
    "avg_inter": "#660099",
    "U":"#CE0000",
    "M":"#004C99",
}


c_kwgs ={
    "color":"#4E8AC6",
    "linestyle":"-",
    "linewidth":6,
}
f_kwgs ={
    "color":"#E18230",
    "linestyle":"--",
    "linewidth":4,
}
f_kwgs2 = {
    "linestyle":":",
    "linewidth":5,
    "color":"#E7AE46",
}

c_kwgs_small ={
    "color":"#4E8AC6",
    "linestyle":"-",
    "linewidth":6-2,
}
f_kwgs_small ={
    "color":"#E18230",
    "linestyle":"--",
    "linewidth":4-2,
}
f_kwgs2_small = {
    "linestyle":":",
    "linewidth":5-2,
    "color":"#E7AE46",
}

def compute_alpha(i_, n_):
    """Return the default alpha value for an item index."""
    return 1/(i_+1)

def set_axes(axs:plt.Axes|list, to_rmv:list=["all"], to_add:list=[]):
    """Hide or add axis lines on one or more Matplotlib axes.

    Parameters
    ----------
    axs : plt.Axes or list
        Axis object or iterable of axis objects to update.
    to_rmv : list, optional
        Axis names to remove. ``["all"]`` hides the whole axis.
    to_add : list, optional
        Axisartist axis names to show and draw with arrow tips.
    """
    if np.iterable(axs):
        for ax in axs:
            set_axes(ax, to_rmv=to_rmv, to_add=to_add)
    else:
        ax = axs
        if "all" in to_rmv:
            ax.set_axis_off()
        else:
            for direction in to_rmv:
                # adds X and Y-axis from the origin
                ax.axis[direction].set_visible(False)
        for direction in to_add:
            # adds arrows at the ends of each axis
            ax.axis[direction].set_axisline_style("-|>")
            # adds X and Y-axis from the origin
            ax.axis[direction].set_visible(True)


def set_zeros_axis(ax:plt.Axes):
    """Show x=0 and y=0 axis lines with arrow tips."""
    set_axes(ax, to_add=["xzero", "yzero"])


def valid_diameter(mydict, model="", filter_monotony=True):
    """Return indices with positive, optionally monotonic, speed values.

    Parameters
    ----------
    mydict : dict
        Mapping containing a ``"speed"`` entry indexed by model name.
    model : str, default=""
        Model key used to select speed values.
    filter_monotony : bool, default=True
        If ``True``, keep only positive values whose speed does not decrease
        from the previous sample.
    """
    speed = np.array(mydict["speed"][model])
    if filter_monotony:
        indices = np.argwhere((speed>0) & (np.diff(speed, prepend=speed[0]) >= 0))
        if speed[indices[0]] > speed[indices[1]]:
            indices[0] = indices[1] - 1
    else:
        indices = np.argwhere((speed>0))

    return indices


def plot_config(ax, **kwgs):
    """Apply common axis configuration options to a Matplotlib axis.

    Supported keyword arguments include ``xscale``, ``yscale``, ``xlim``,
    ``ylim``, ``xlabel``, ``ylabel``, ``grid``, and ``legend``.
    """
    if "xscale" in kwgs:
        ax.set_xscale(kwgs["xscale"])
    if "yscale" in kwgs:
        ax.set_yscale(kwgs["yscale"])
    if "xlim" in kwgs:
        ax.set_xlim(kwgs["xlim"])
    if "ylim" in kwgs:
        ax.set_ylim(kwgs["ylim"])
    if "ylabel" in kwgs:
        ax.set_ylabel(kwgs["ylabel"])
    if "xlabel" in kwgs:
        ax.set_xlabel(kwgs["xlabel"])
    if "grid" in kwgs:
        if kwgs["grid"] == "fancy":
            ax.grid(which='minor',color='lightgray')
            ax.grid(which='major',color='dimgray')
        elif kwgs["grid"]:
            ax.grid()
    if "legend" in kwgs:
        if kwgs["legend"]:
            ax.legend()

def set_axis_param(obj:plt.Axes|np.ndarray|plt.Figure):
    """Apply bold labels, darker ticks, and simplified spines to axes."""
    if np.iterable(obj):
        for _ax in obj:
            set_axis_param(_ax)
    elif isinstance(obj,plt.Figure):
        set_axis_param(obj.axes)
    else:
        obj.tick_params(width = 2, color = '0.2', labelcolor = '0.2')
        obj.set_xlabel(obj.get_xlabel(), weight = 'bold', color = '0.2')
        obj.set_ylabel(obj.get_ylabel(), weight = 'bold', color = '0.2')
        obj.spines[['bottom', 'left']].set_linewidth(2)
        obj.spines[['bottom', 'left']].set_color('0.2')
        obj.spines[['top', 'right']].set_visible(False)

def add_fancy_frame(fig, facecolor=(0, 0, 0, 0.0), edgecolor=(0, 0, 0, 1), pad=0.05):
    """Add a rounded frame patch around a figure or subfigure.

    Parameters
    ----------
    fig : matplotlib.figure.Figure or matplotlib.figure.SubFigure
        Figure-like object to decorate.
    facecolor, edgecolor : color, optional
        Frame fill and stroke colors.
    pad : float, default=0.05
        Padding used both for the rounded box style and frame position.
    """
    boxstyle=f"round,pad={pad}"
    if isinstance(fig, plt.Figure):
        s = fig.get_size_inches()
    elif isinstance(fig, SubFigure):
        bbox = fig.get_tightbbox()
        s = (bbox.width, bbox.height)
    mutation_aspect=s[0]/s[1]
    kwargs = {
        'facecolor': facecolor,
        'edgecolor': edgecolor,
        "boxstyle":boxstyle,
        "mutation_aspect": mutation_aspect,
    }
    fancy = FancyBboxPatch((pad/2,pad/2), 1-pad,1-pad, transform=fig.transFigure, figure=fig, **kwargs)
    fig.patches.extend([fancy])
    return fancy


class HandlerTupleVertical(HandlerTuple):
    """Legend handler that stacks tuple entries vertically."""

    def __init__(self, space_coef=1,**kwargs):
        """Create a vertical tuple legend handler.

        Parameters
        ----------
        space_coef : float, default=1
            Multiplier applied to the vertical space allocated to each entry.
        **kwargs
            Forwarded to ``matplotlib.legend_handler.HandlerTuple``.
        """
        HandlerTuple.__init__(self,**kwargs)
        self.space_coef = space_coef


    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize, trans):
        """Create vertically stacked legend artists."""
        # How many lines are there.
        numlines = len(orig_handle)
        handler_map = legend.get_legend_handler_map()

        # divide the vertical space where the lines will go
        # into equal parts based on the number of lines
        height_y = self.space_coef*(height / numlines)
        height_y_ofsett = (height_y*numlines - height)

        leglines = []
        for i, handle in enumerate(orig_handle):
            handler = legend.get_legend_handler(handler_map, handle)

            legline = handler.create_artists(legend, handle,
                                             xdescent,
                                             (2*i + 1)*height_y-height_y_ofsett,
                                             width,
                                             2*height,
                                             fontsize, trans)
            leglines.extend(legline)

        return leglines
    
def gradient_image_custom(ax, direction=1, cmap_range=(0, 1), orientation=(0,1),**kwargs):
    """
    Draw a gradient image based on a colormap.

    Parameters
    ----------
    ax : Axes
        The Axes to draw on.
    direction : float
        The direction of the gradient. This is a number in
        range 0 (=vertical) to 1 (=horizontal).
    cmap_range : float, float
        The fraction (cmin, cmax) of the colormap that should be
        used for the gradient, where the complete colormap is (0, 1).
    orientation : tuple, default=(0, 1)
        Kept for compatibility with existing calls. The current implementation
        uses ``direction`` for the gradient orientation.
    **kwargs
        Other parameters are passed on to `.Axes.imshow()`.
        In particular, *cmap*, *extent*, and *transform* may be useful.
    """
    phi = direction * np.pi / 2
    v = np.array([np.cos(phi), np.sin(phi)])
    X = np.array([[v @ [1, 0], v @ [1, 1]],
                [v @ [0, 0], v @ [0, 1]]])

                    
    a, b = cmap_range
    X = a + (b - a) / X.max() * X
    # X = X.T
    im = ax.imshow(X, interpolation='bicubic', clim=(0, 1),
                   aspect='auto', **kwargs)
    return im




def linear_cmap(c1:str|tuple, c2:str|tuple, n=50,callback=None):
    """Create a linear colormap between two colors.

    Parameters
    ----------
    c1, c2 : str or tuple
        Matplotlib-compatible colors used as start and end colors.
    n : int, default=50
        Number of colors in the generated colormap.
    callback : callable, optional
        Function receiving and returning the RGBA value array before the
        colormap is created.
    """
    c1=to_rgba(c1)
    c2=to_rgba(c2)
    vals = np.vstack([
        np.linspace(c1[0], c2[0], n),
        np.linspace(c1[1], c2[1], n),
        np.linspace(c1[2], c2[2], n),
        np.linspace(c1[3], c2[3], n),
    ])
    if callback is not None:
        vals = callback(vals)
    return ListedColormap(vals.T)

def rainbowarrow(ax, start, end, cmap="viridis", n=50,lw=3, headw=100):
    """Draw an arrow with a color gradient along its shaft.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axis on which to draw the arrow.
    start, end : tuple
        ``(x, y)`` coordinates for the arrow start and end.
    cmap : str or tuple, default="viridis"
        Matplotlib colormap name, or a ``(start_color, end_color)`` tuple used
        to build a linear colormap.
    n : int, default=50
        Number of segments used for the gradient shaft.
    lw : float, default=3
        Shaft line width.
    headw : float or None, default=100
        Marker size for the arrow head. If ``None``, it is derived from
        ``lw``.
    """
    if headw is None:
        headw = (2*lw)**2
    if isinstance(cmap, tuple):
        cmap = linear_cmap(*cmap, n=n)
    else:
        cmap = plt.get_cmap(cmap,n)
    # Arrow shaft: LineCollection
    x = np.linspace(start[0],end[0],n)
    y = np.linspace(start[1],end[1],n)
    points = np.array([x,y]).T.reshape(-1,1,2)
    segments = np.concatenate([points[:-1],points[1:]], axis=1)
    lc = LineCollection(segments, cmap=cmap, linewidth=lw)
    lc.set_array(np.linspace(0,1,n))
    ax.add_collection(lc)
    # Arrow head: Triangle
    tricoords = headw*np.array([(0,-0.4),(0.5,0),(0,0.4),(0,-0.4)])

    angle = np.arctan2(end[1]-start[1],end[0]-start[0])
    rot = Affine2D().rotate(angle)
    tricoords2 = rot.transform(tricoords)
    tri = Path(tricoords2, closed=True)
    ax.scatter(end[0],end[1], c=1, s=headw, marker=tri, cmap=cmap,vmin=0)
    ax.autoscale_view()
