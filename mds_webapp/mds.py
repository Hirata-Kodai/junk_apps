import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse


class ScatterWithHoveringPlotter:
    def __init__(self, embed, raw_data):
        '''
        embed(np.ndarray): - 2-dim coordinate data on embedding space
        raw_data(array-like): - raw data corresponding to embed
        '''
        self.fig, self.ax = plt.subplots()
        self.sc = plt.scatter(*embed.T, s=3)
        self.annot = self.ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                                      bbox=dict(boxstyle="round", fc="w"),
                                      arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)
        self.raw_data = raw_data
        assert embed.shape[0] == len(raw_data)

    def _update_annot(self, ind):
        i = ind["ind"][0]
        pos = self.sc.get_offsets()[i]
        self.annot.xy = pos
        text = self.raw_data[i]
        self.annot.set_text(text)

    def _hover(self, event):
        vis = self.annot.get_visible()
        if event.inaxes == self.ax:
            cont, ind = self.sc.contains(event)
            if cont:
                self._update_annot(ind)
                self.annot.set_visible(True)
                self.fig.canvas.draw_idle()
            else:
                if vis:
                    self.annot.set_visible(False)
                    self.fig.canvas.draw_idle()

    def show(self):
        self.fig.canvas.mpl_connect("motion_notify_event", self._hover)
        plt.show()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('embed_file', type=str)
    ap.add_argument('search_file', type=str)
    args = ap.parse_args()

    D_transformed = np.load(args.embed_file)
    haiku_df = pd.read_csv(args.search_file)
    haikus = haiku_df['本文']
    # plot color map
    plotter = ScatterWithHoveringPlotter(D_transformed, haikus)
    plotter.show()


if __name__ == '__main__':
    main()
