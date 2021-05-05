import math

import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.gridspec as grid_spec
import seaborn as sns
from pywaffle import Waffle

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

    def computeGridSize(self, feats, nrows=None, ncols=None):
        if (nrows is None) & (ncols is None):
            ncols = math.ceil(math.sqrt(len(feats)))
            nrows = math.ceil(len(feats) / ncols)
        elif (nrows is None):
            nrows = math.ceil(len(feats) / ncols)
        else:
            ncols = math.ceil(len(feats) / nrows)
        return (nrows, ncols)

    def drawMultiplePlots(self, plotFunction, data, feats=None, title=None, figSize=None, nrows=None, ncols=None, **kwargs):
        if feats is None:
            feats = list(data.columns[data.dtypes != object])
        nrows, ncols = self.computeGridSize(feats=feats, nrows=nrows, ncols=ncols)
        if figSize is None:
            figSize = tuple([self.defaultFigSize[0] * ncols, self.defaultFigSize[1] * nrows])
        fig = plt.figure(figsize=figSize, facecolor=self.figFaceColor, tight_layout=True)
        fig.suptitle(title, fontsize=self.fontSize+4, fontweight=self.fontWeight, fontfamily=self.fontFamily)
        for i, feat in enumerate(feats):
            locals()["ax" + str(i)] = fig.add_subplot(nrows, ncols, i + 1)
            plotFunction(data=data, feat=feat, title=feat, ax=locals()["ax" + str(i)], **kwargs)

    def drawKDEPlot(self, data, feat, title=None, figSize=None, showGrid=True, ax=None):       
        ax = self.initializePlot(ax=ax, figSize=figSize)
        g = sns.kdeplot(ax=ax, data=data, x=feat, fill=True, linewidth=self.defaultLineWidth, \
            ec=self.colorBlack, alpha=self.defaultAlpha, zorder=3, legend=False)
        self.setPlotProperties(g, ax, title=title, xlabel=feat, showGrid=showGrid, hideYAxis=True)        

    def drawMultipleKDEPlots(self, data, figSize, title=None, feats=None, showGrid=True, nrows=None, ncols=None):
        self.drawMultiplePlots(plotFunction=self.drawKDEPlot, data=data, figSize=figSize, title=title, \
            nrows=nrows, ncols=ncols, feats=feats, showGrid=showGrid)

    def drawKDEPlotsByCategory(self, data, feat, category, title=None, figSize=None, showGrid=True, ax=None):       
        ax = self.initializePlot(ax=ax, figSize=figSize)
        g = sns.kdeplot(ax=ax, data=data, x=feat, hue=category, palette=self.snsPalette, fill=True, \
            alpha=self.defaultAlpha, linewidth=self.defaultLineWidth, multiple="stack", zorder=3)
        self.setPlotProperties(g, ax, title=title, showGrid=showGrid, hideYAxis=True, hideLegendTitle=True)

    def drawMultipleKDEPlotsByCategory(self, data, category, feats=None, title=None, figSize=None, showGrid=True, nrows=None, ncols=None):
        self.drawMultiplePlots(plotFunction=self.drawKDEPlotsByCategory, data=data, figSize=figSize, title=title, \
            nrows=nrows, ncols=ncols, feats=feats, category=category, showGrid=showGrid)

    def drawRegressionPlot(self, data, feat, feat2, title=None, figSize=None, ax=None):
        ax = self.initializePlot(ax=ax, figSize=figSize)
        g = sns.regplot(ax=ax, data=data, x=feat, y=feat2, line_kws={"color":self.colorBlack}, \
            scatter_kws={"edgecolors":[self.colorWhite], "alpha":self.defaultAlpha, "linewidth": 0.5})
        self.setPlotProperties(g, ax, title=title, showGrid=False, hideLegendTitle=True)

    def drawBarPlot(self, data, feat, feat2, category=None, title=None, figSize=None, ax=None):
        ax = self.initializePlot(ax=ax, figSize=figSize)
        g = sns.barplot(ax=ax, data=data, x=feat, y=feat2, hue=category, palette=self.snsPalette, edgecolor=self.colorBlack)
        self.setPlotProperties(g, ax, title=title, showGrid=False, hideLegendTitle=True)

    def drawScatterPlot(self, data, feat, feat2, category=None, title=None, figSize=None, ax=None):
        ax = self.initializePlot(ax=ax, figSize=figSize)
        g = sns.scatterplot(ax=ax, data=data, x=feat, y=feat2, hue=category, palette=self.snsPalette, edgecolor=self.colorWhite)
        self.setPlotProperties(g, ax, title=title, showGrid=False, hideLegendTitle=True)

    def drawMultipleScatterPlots(self, data, feats, feat2, category=None, title=None, figSize=None, nrows=None, ncols=None):
        self.drawMultiplePlots(plotFunction=self.drawScatterPlot, data=data, feats=feats, feat2=feat2, category=category, \
            title=title, figSize=figSize, nrows=nrows, ncols=ncols)

    def drawBoxPlot(self, data, feat, feat2=None, title=None, figSize=None, ax=None):
        ax = self.initializePlot(ax=ax, figSize=figSize)
        colorBlackDict = {"color": self.colorBlack}
        plotProps = {"boxprops": {"edgecolor": self.colorBlack}, "medianprops": colorBlackDict, "whiskerprops": colorBlackDict, "capprops": colorBlackDict}
        g = sns.boxplot(ax=ax, data=data, y=feat, x=feat2, palette=self.snsPalette, fliersize=3, linewidth=self.defaultLineWidth, **plotProps)
        self.setPlotProperties(g, ax, title=title, showGrid=False, hideLegendTitle=True)

    def drawMultipleBoxPlots(self, data, feats, feat2=None, title=None, figSize=None, nrows=None, ncols=None):
        self.drawMultiplePlots(plotFunction=self.drawBoxPlot, data=data, feats=feats, feat2=feat2, \
            title=title, figSize=figSize, nrows=nrows, ncols=ncols)

    def drawViolinPlot(self, data, feat, feat2, category=None, title=None, figSize=None, ax=None):
        ax = self.initializePlot(ax=ax, figSize=figSize)
        g = sns.violinplot(ax=ax, data=data, y=feat, x=feat2, hue=category, palette=self.snsPalette, linewidth=self.defaultLineWidth)
        self.setPlotProperties(g, ax, title=title, showGrid=False, hideLegendTitle=True)

    def drawMultipleViolinPlots(self, data, feats, feat2, category=None, title=None, figSize=None, nrows=None, ncols=None):
        self.drawMultiplePlots(plotFunction=self.drawViolinPlot, data=data, feats=feats, feat2=feat2, category=category, \
            title=title, figSize=figSize, nrows=nrows, ncols=ncols)

    def drawMissingValuesHeatmap(self, data, title=None, figSize=None, sorted=True):
        if figSize is None:
            figSize = (5, math.ceil(data.shape[1] / 3))
        missingCounts = data.isna().sum().to_frame()
        if sorted:
            missingCounts.sort_values(by=0, inplace=True)
        ax = self.initializePlot(ax=None, figSize=figSize)
        reverseCMap = cm.get_cmap(self.snsPalette).reversed()
        g = sns.heatmap(ax=ax, data=missingCounts, vmin=0, vmax=data.shape[0], cmap=reverseCMap, \
            xticklabels=False, annot=True, fmt="d")
        self.setPlotProperties(g, ax, title=title, showGrid=False)
        
    def drawWafflePlot(self, data, feat, feat2=None, title=None, figSize=None, iconName=None, iconSize=None, waffleRows=10, waffleColumns=10):

        def getCountsData(data, feat):
            countsData = data.groupby(feat).size().reset_index(name="counts").sort_values("counts", ascending=False)
            countsData["counts"] = countsData["counts"] / sum(countsData["counts"])
            return (countsData)

        plotLabels = [feat] if (feat2 is None) else data[feat2].unique()
        countsData = getCountsData(data=data, feat=feat)
        wafflePlots = {}
        for p in range(len(plotLabels)):
            if feat2 is not None:
                countsData = getCountsData(data=data[data[feat2] == plotLabels[p]], feat=feat)
            waffleColors = [plt.get_cmap(self.snsPalette)(i / float(countsData.shape[0])) for i in range(countsData.shape[0])]
            waffleLabels = ["%s (%.1f%%)" % (row[feat], 100 * row["counts"]) for _, row in countsData.iterrows()]
            propsDict = {
                "values":countsData["counts"], 
                "rows": waffleRows, 
                "columns": waffleColumns, 
                "colors": waffleColors, 
                "icons": iconName, 
                "icon_size": iconSize, 
                "icon_legend": False,
                "title": {"label": plotLabels[p], "loc":"center","fontsize":(self.fontSize + 2)},
                "legend": {"labels": waffleLabels, "loc": "upper center", "bbox_to_anchor": (0.5, -0.05), "ncol":2}, 
            }
            wafflePlots["1" + str(len(plotLabels)) + str(p + 1)] = propsDict
        
        fig = plt.figure(FigureClass=Waffle, plots=wafflePlots, figsize=figSize, rounding_rule="floor")
        plt.show()
