import math

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.gridspec as grid_spec
import seaborn as sns

class Visualizations():

    def __init__(self, fontSize=12, fontWeight="normal", fontFamily="serif"):
        self.fontSize = fontSize
        self.fontWeight = fontWeight
        self.fontFamily = fontFamily
        
        self.colorBlue = "#0f4c81"
        self.colorBlack = "black"
        self.colorGray = "gray"
        self.figFaceColor = "#fafafa"
        
        self.defaultFigSize = (5, 4)
        self.defaultAlpha = 0.8
        self.defaultLineWidth = 1
    
    def computeGridSize(self, variables, nrows=None, ncols=None):
        if (nrows is None) & (ncols is None):
            ncols = math.ceil(math.sqrt(len(variables)))
            nrows = math.ceil(len(variables) / ncols)
        elif (nrows is None):
            nrows = math.ceil(len(variables) / ncols)
        else:
            ncols = math.ceil(len(variables) / nrows)
        return (nrows, ncols)

    def drawKDEPlot(self, data, variable, title, figSize=None, showGrid=True, ax=None):       
        if ax is None:
            if figSize is None:
                figSize = self.defaultFigSize
            fig = plt.figure(figsize=figSize, facecolor=self.figFaceColor, tight_layout=True)
            ax = fig.add_subplot(1, 1, 1)
        
        sns.kdeplot(ax=ax, x=data[variable], color=self.colorBlue, shade=True, linewidth=self.defaultLineWidth, \
            ec=self.colorBlack, alpha=self.defaultAlpha, zorder=3, legend=False)
        if showGrid:
            plt.grid(which="major", axis="x", zorder=0, color=self.colorGray, linestyle=":", dashes=(1,5))
        plt.xlabel(variable, fontsize=self.fontSize, fontweight=self.fontWeight, fontfamily=self.fontFamily)
        plt.title(title, fontsize=self.fontSize+2, fontweight=self.fontWeight, fontfamily=self.fontFamily)

    def drawMultipleKDEPlots(self, data, figSize, title, nrows=None, ncols=None, variables=None, showGrid=True):
        if variables is None:
            variables = list(data.columns[data.dtypes != object])
        nrows, ncols = self.computeGridSize(variables=variables, nrows=nrows, ncols=ncols)
        
        fig = plt.figure(figsize=figSize, facecolor=self.figFaceColor, tight_layout=True)
        fig.suptitle(title, fontsize=self.fontSize+4, fontweight=self.fontWeight, fontfamily=self.fontFamily)
        for i, variable in enumerate(variables):
            locals()["ax" + str(i)] = fig.add_subplot(nrows, ncols, i + 1)
            self.drawKDEPlot(data=data, variable=variable, title=variable, showGrid=showGrid, ax=locals()["ax" + str(i)])

        