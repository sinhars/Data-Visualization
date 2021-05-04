import math

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.gridspec as grid_spec
import seaborn as sns

class Visualizations():

    def __init__(self, snsPalette="Paired", fontSize=12, fontWeight="normal", fontFamily="sans-serif"):
        self.fontSize = fontSize
        self.fontWeight = fontWeight
        self.fontFamily = fontFamily
        
        self.snsPalette = snsPalette
        sns.set_palette(snsPalette)

        self.colorWhite = "white"
        self.colorBlack = "black"
        self.colorGray = "gray"
        self.figFaceColor = "#fafafa"
        self.plotFaceColor = "#fafafa"
        
        self.defaultFigSize = (4, 3)
        self.defaultAlpha = 0.6
        self.defaultLineWidth = 1
        self.wideLineWidth = 1.5
    
    def initializePlot(self, ax, figSize):
        if ax is None:
            if figSize is None:
                figSize = self.defaultFigSize
            fig = plt.figure(figsize=figSize, facecolor=self.figFaceColor, tight_layout=True)
            ax = fig.add_subplot(1, 1, 1)
        return (ax)

    def setPlotProperties(self, g, ax, title, xlabel=None, ylabel=None, showGrid=True, hideYAxis=False, hideLegendTitle=False):
        g.set_facecolor(self.plotFaceColor)
        g.set_title(title, fontsize=self.fontSize+2, fontweight=self.fontWeight, fontfamily=self.fontFamily)
        g.set_xlabel(xlabel, fontsize=self.fontSize, fontweight=self.fontWeight, fontfamily=self.fontFamily)
        g.set_ylabel(xlabel, fontsize=self.fontSize, fontweight=self.fontWeight, fontfamily=self.fontFamily)
        if hideYAxis & (g.get_yaxis() is not None):
            g.get_yaxis().set_visible(False)
            g.spines["left"].set_visible(False)
        if hideLegendTitle & (g.get_legend() is not None):
            g.get_legend().set_title(None)
        if showGrid:
            ax.grid(axis="x", which="major", zorder=0, color=self.colorGray, linestyle=":", dashes=(1,5))
        for s in ["top", "right"]:
            g.spines[s].set_visible(False)

    def computeGridSize(self, xs, nrows=None, ncols=None):
        if (nrows is None) & (ncols is None):
            ncols = math.ceil(math.sqrt(len(xs)))
            nrows = math.ceil(len(xs) / ncols)
        elif (nrows is None):
            nrows = math.ceil(len(xs) / ncols)
        else:
            ncols = math.ceil(len(xs) / nrows)
        return (nrows, ncols)

    def drawMultiplePlots(self, plotFunction, data, xs=None, title=None, figSize=None, nrows=None, ncols=None, **kwargs):
        if xs is None:
            xs = list(data.columns[data.dtypes != object])
        nrows, ncols = self.computeGridSize(xs=xs, nrows=nrows, ncols=ncols)
        if figSize is None:
            figSize = tuple([self.defaultFigSize[0] * ncols, self.defaultFigSize[1] * nrows])
        fig = plt.figure(figsize=figSize, facecolor=self.figFaceColor, tight_layout=True)
        fig.suptitle(title, fontsize=self.fontSize+4, fontweight=self.fontWeight, fontfamily=self.fontFamily)
        for i, x in enumerate(xs):
            locals()["ax" + str(i)] = fig.add_subplot(nrows, ncols, i + 1)
            plotFunction(data=data, x=x, title=x, ax=locals()["ax" + str(i)], **kwargs)

    def drawKDEPlot(self, data, x, title=None, figSize=None, showGrid=True, ax=None):       
        ax = self.initializePlot(ax=ax, figSize=figSize)
        g = sns.kdeplot(ax=ax, data=data, x=x, fill=True, linewidth=self.defaultLineWidth, \
            ec=self.colorBlack, alpha=self.defaultAlpha, zorder=3, legend=False)
        self.setPlotProperties(g, ax, title=title, xlabel=x, showGrid=showGrid, hideYAxis=True)        

    def drawMultipleKDEPlots(self, data, figSize, title=None, xs=None, showGrid=True, nrows=None, ncols=None):
        self.drawMultiplePlots(plotFunction=self.drawKDEPlot, data=data, figSize=figSize, title=title, \
            nrows=nrows, ncols=ncols, xs=xs, showGrid=showGrid)

    def drawKDEPlotsByCategory(self, data, x, category, title=None, figSize=None, showGrid=True, ax=None):       
        ax = self.initializePlot(ax=ax, figSize=figSize)
        g = sns.kdeplot(ax=ax, data=data, x=x, hue=category, palette=self.snsPalette, fill=True, \
            alpha=self.defaultAlpha, linewidth=self.defaultLineWidth, multiple="stack", zorder=3)
        self.setPlotProperties(g, ax, title=title, showGrid=showGrid, hideYAxis=True, hideLegendTitle=True)

    def drawMultipleKDEPlotsByCategory(self, data, category, xs=None, title=None, figSize=None, showGrid=True, nrows=None, ncols=None):
        self.drawMultiplePlots(plotFunction=self.drawKDEPlotsByCategory, data=data, figSize=figSize, title=title, \
            nrows=nrows, ncols=ncols, xs=xs, category=category, showGrid=showGrid)

    def drawRegressionPlot(self, data, x, y, title=None, figSize=None, ax=None):
        ax = self.initializePlot(ax=ax, figSize=figSize)
        g = sns.regplot(ax=ax, data=data, x=x, y=y, line_kws={"color":self.colorBlack}, \
            scatter_kws={"edgecolors":[self.colorWhite], "alpha":self.defaultAlpha, "linewidth": 0.5})
        self.setPlotProperties(g, ax, title=title, showGrid=False, hideLegendTitle=True)

    def drawBarPlot(self, data, x, y, category=None, title=None, figSize=None, ax=None):
        ax = self.initializePlot(ax=ax, figSize=figSize)
        g = sns.barplot(ax=ax, data=data, x=x, y=y, hue=category, palette=self.snsPalette, edgecolor = self.colorBlack)
        self.setPlotProperties(g, ax, title=title, showGrid=False, hideLegendTitle=True)

    def drawScatterPlot(self, data, x, y, category=None, title=None, figSize=None, ax=None):
        ax = self.initializePlot(ax=ax, figSize=figSize)
        g = sns.scatterplot(ax=ax, data=data, x=x, y=y, hue=category, palette=self.snsPalette, edgecolor = self.colorWhite)
        self.setPlotProperties(g, ax, title=title, showGrid=False, hideLegendTitle=True)

    def drawMultipleScatterPlots(self, data, xs, y, category=None, title=None, figSize=None, nrows=None, ncols=None):
        self.drawMultiplePlots(plotFunction=self.drawScatterPlot, data=data, xs=xs, y=y, category=category, \
            title=title, figSize=figSize, nrows=nrows, ncols=ncols)

    def drawBoxPlot(self, data, x, category=None, title=None, figSize=None, ax=None):
        ax = self.initializePlot(ax=ax, figSize=figSize)
        colorBlackDict = {"color": self.colorBlack}
        plotProps = {"boxprops": {"edgecolor": self.colorBlack}, "medianprops": colorBlackDict, "whiskerprops": colorBlackDict, "capprops": colorBlackDict}
        g = sns.boxplot(ax=ax, data=data, x=category, y=x, palette=self.snsPalette, fliersize=3, linewidth=self.defaultLineWidth, **plotProps)
        self.setPlotProperties(g, ax, title=title, showGrid=False, hideLegendTitle=True)

    def drawMultipleBoxPlots(self, data, xs, category=None, title=None, figSize=None, nrows=None, ncols=None):
        self.drawMultiplePlots(plotFunction=self.drawBoxPlot, data=data, xs=xs, category=category, \
            title=title, figSize=figSize, nrows=nrows, ncols=ncols)