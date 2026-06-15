import matplotlib.pyplot as plt

from tbox import plot_config


def test_plot_config_applies_ylim():
    fig, ax = plt.subplots()
    try:
        plot_config(ax, ylim=(1, 2))

        assert ax.get_ylim() == (1, 2)
    finally:
        plt.close(fig)

