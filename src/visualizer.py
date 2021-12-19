from matplotlib import pyplot as plt
import multiprocessing
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib import animation

class Visualizer:

    # constructor
    def __init__(self):
        """ 
        constructor for visualizer class,
        reads ../data/raw/lattices.txt and puts every lattice
        into self.lattices
        """

        # self.lattices is 3-dimensional and holds all states
        self.lattices = []

        # create empty 2d array
        lattice = []

        # open raw data and read line for line
        with open("../data/raw/lattices.txt") as file:
            for row in file:

                # every lattice is seperated with one line containing ","
                if "," in row:
                    
                    # put current lattice into lattices
                    self.lattices.append(lattice)

                    # reset lattice
                    lattice = []
                    continue
                
                # append rows into lattice
                lattice.append(list(map(int, row.rstrip().split(" "))))

    def plot_lattice(self, lattice):
        """
        function used by plot_lattices
        """

        plt.imshow(lattice, cmap = "Greys")
        plt.show()

    def plot_lattices(self, save = False):
        """
        plot all lattices in lattices.txt
        default to NOT save plots
        """
        
        if save:
            # iterating over self.lattices
            for i, lattice in enumerate(self.lattices):

                # plotting lattice
                fig = plt.figure()
                plt.imshow(lattice, cmap = "Greys")

                # saving figure
                filename = "../data/processed/lattice_" + str(i) + ".pdf"
                plt.savefig(filename, dpi = 600)
        else:
            # plot all lattices using multiprocessing pool 
            pool = multiprocessing.Pool()
            pool.map(self.plot_lattice, self.lattices)
            pool.close()

    def animate_lattices(self, save = False):
        """
        animation of all lattices inside self.lattices
        default to NOT save animation
        """

        # function used for updating plot
        def animate(i):
            im.set_array(self.lattices[i])
            return im,
        
        # initial conditions for animation
        nFrames = len(self.lattices)
        fig = plt.figure()
        im = plt.imshow(self.lattices[0], cmap = "Greys")

        # animate self.lattices
        anim = FuncAnimation(fig, animate, frames = nFrames, interval = 25, blit = True)

        # if save==True use ffmpegwriter to save animation
        if save:
            save_path = "../data/processed/lattice_animation.mp4"
            anim.save(save_path, writer=animation.FFMpegWriter(fps = 60))

        # else show the animation without saving
        else:
            plt.show()

if __name__ == '__main__':
    visualizer = Visualizer()
    visualizer.animate_lattices(save = True)
    visualizer.plot_lattices(save = True)