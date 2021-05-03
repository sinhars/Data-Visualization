import math

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.gridspec as grid_spec
import seaborn as sns

class Visualizations():

    def __init__(self, palette="viridis", fontSize=12, fontWeight="normal", fontFamily="sans-serif"):
        self.fontSize = fontSize
        self.fontWeight = fontWeight
        self.fontFamily = fontFamily
        
        self.snsPalette = palette
        self.colorBlack = "black"
        self.colorGray = "gray"
        self.figFaceColor = "#fafafa"
        self.figBackgroundColor = "#fafafa"
        
        self.defaultFigSize = (5, 4)
        self.defaultAlpha = 0.8
        self.defaultLineWidth = 1
        self.wideLineWidth = 1.5
    
    def computeGridSize(self, variables, nrows=None, ncols=None):
        if (nrows is None) & (ncols is None):
            ncols = math.ceil(math.sqrt(len(variables)))
            nrows = math.ceil(len(variables) / ncols)
        elif (nrows is None):
            nrows = math.ceil(len(variables) / ncols)
        else:
            ncols = math.ceil(len(variables) / nrows)
        return (nrows, ncols)

    def drawMultiplePlots(self, plotFunction, data, figSize, title, nrows=None, ncols=None, variables=None, **kwargs):
        if variables is None:
            variables = list(data.columns[data.dtypes != object])
        nrows, ncols = self.computeGridSize(variables=variables, nrows=nrows, ncols=ncols)
        
        fig = plt.figure(figsize=figSize, facecolor=self.figFaceColor, tight_layout=True)
        fig.suptitle(title, fontsize=self.fontSize+4, fontweight=self.fontWeight, fontfamily=self.fontFamily)
        for i, variable in enumerate(variables):
            locals()["ax" + str(i)] = fig.add_subplot(nrows, ncols, i + 1)
            plotFunction(data=data, variable=variable, title=variable, ax=locals()["ax" + str(i)], **kwargs)

    def setPlotProperties(self, g, title, xlabel):
        g.set_xlabel(xlabel, fontsize=self.fontSize, fontweight=self.fontWeight, fontfamily=self.fontFamily)
        g.set_title(title, fontsize=self.fontSize+2, fontweight=self.fontWeight, fontfamily=self.fontFamily)
        g.set_facecolor(self.figBackgroundColor)
        for s in ["top", "right", "left"]:
            g.spines[s].set_visible(False)

    def drawKDEPlot(self, data, variable, title, figSize=None, showGrid=True, ax=None):       
        if ax is None:
            if figSize is None:
                figSize = self.defaultFigSize
            fig = plt.figure(figsize=figSize, facecolor=self.figFaceColor, tight_layout=True)
            ax = fig.add_subplot(1, 1, 1)
        g = sns.kdeplot(ax=ax, x=data[variable], palette=self.snsPalette, fill=True, linewidth=self.defaultLineWidth, \
            ec=self.colorBlack, alpha=self.defaultAlpha, zorder=3, legend=False)
        self.setPlotProperties(g, title=title, xlabel=variable)
        if showGrid:
            plt.grid(which="major", axis="x", zorder=0, color=self.colorGray, linestyle=":", dashes=(1,5))
        

    def drawMultipleKDEPlots(self, data, figSize, title, variables=None, showGrid=True, nrows=None, ncols=None):
        self.drawMultiplePlots(plotFunction=self.drawKDEPlot, data=data, figSize=figSize, title=title, \
            nrows=nrows, ncols=ncols, variables=variables, showGrid=showGrid)

    def drawKDEPlotsByCategory(self, data, variable, category, title, figSize=None, showGrid=True, ax=None):       
        if ax is None:
            if figSize is None:
                figSize = self.defaultFigSize
            fig = plt.figure(figsize=figSize, facecolor=self.figFaceColor, tight_layout=True)
            ax = fig.add_subplot(1, 1, 1)
        
        g = sns.kdeplot(ax=ax, x=data[variable], hue=data[category], palette=self.snsPalette, fill=True, \
            alpha=self.defaultAlpha, linewidth=self.defaultLineWidth, multiple="stack", zorder=3)
        self.setPlotProperties(g, title=title, xlabel=variable)
        if showGrid:
            plt.grid(which="major", axis="x", zorder=0, color=self.colorGray, linestyle=":", dashes=(1,5))

    def drawMultipleKDEPlotsByCategory(self, data, category, figSize, title, variables=None, showGrid=True, nrows=None, ncols=None):
        self.drawMultiplePlots(plotFunction=self.drawKDEPlotsByCategory, data=data, figSize=figSize, title=title, \
            nrows=nrows, ncols=ncols, variables=variables, category=category, showGrid=showGrid)