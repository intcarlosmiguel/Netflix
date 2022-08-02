import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def scatterGraph(x,y):
    plt.figure(figsize=(18,9))
    plt.scatter(x,y)
    plt.show()

def boxGraph(x,titulo):
    filled_marker_style = dict(marker='D', markersize=5,
                           color='k',
                           markerfacecolor='teal',
                           markerfacecoloralt='lightsteelblue',
                           markeredgecolor=None)
    plt.figure(figsize=(10, 8))
    plt.title(titulo, size=18)
    plt.grid(linewidth=1, alpha=0.8,axis = 'y')
    boxprops = dict(linestyle='-', linewidth=2, color='k')
    ax = plt.boxplot(x,
        flierprops=filled_marker_style,
        patch_artist=True,
        boxprops=boxprops)

    colors = ['coral']

    for patch, color in zip(ax['boxes'], colors):
        patch.set_facecolor(color)
    for median in ax['medians']:
        median.set_color('k')
    plt.show()

def temporalplot(ax,x,y,labels = '',color = 'darkslategray'):
    ax.grid(linewidth=1, alpha=0.8,axis = 'y')
    ax.plot(x,y,color = color, linewidth=3, markersize=12,label = labels)
    return ax

def reduce(test):
    test0 = test[test>0.1]
    test1 = test[test<0.1]
    test = np.concatenate((test0,[np.sum(test1)]))
    return test

def pieGraph(ax,label,value):
    value2 = value/np.sum(value)
    value2 = np.sort(value2)[::-1]
    if(len(value2[value2<0.1])!=0):
        value = reduce(value2)
        label = np.concatenate((label[:len(value)-1],['Resto']))
    exp = np.zeros(len(value))
    exp[0] = 0.2
    color = ['tab:blue','mediumorchid']
    #plt.figure(figsize = (10,8))
    ax.pie(value,
            labels = label,
            explode = exp,
            shadow = True,
            colors = color,
            autopct='%.1f%%')
    return ax

def barGraph(ax,x,y):
    my_cmap = plt.get_cmap("tab20b_r")
    y = y.astype(float)
    rescale = lambda y: (y - np.min(y)) / (np.max(y) - np.min(y))
    ax.bar(x[:7],y[:7],color = my_cmap(rescale(y[:7])))
    ax.grid(linewidth=1, alpha=0.8,axis = 'y')
    return ax

def generateGraphs(x,y,titulo,Graphs,col = 'row'):
    n_graphs = 0

    if(type(Graphs)==list):
        n_graphs = len(Graphs)
    else:
        n_graphs = 1
    if(n_graphs==2 and col == 'row'):
        fig, axis = plt.subplots(1,2,figsize=(18, 9))
        fig.suptitle(titulo[0], size=20)

        axis[0] = Graphs[0](axis[0],x[0],y[0])
        plt.setp([axis[0]], title=titulo[1])

        axis[1] = Graphs[1](axis[1],x[1],y[1])
        plt.setp([axis[1]], title=titulo[2])
        return 0
    if(n_graphs==2 and col == 'up'):

        fig, axis = plt.subplots(2,1,figsize=(18, 9))
        fig.tight_layout()
        fig.suptitle(titulo[0], size=20)

        axis[0] = Graphs[0](axis[0],x[0],y[0])
        plt.setp([axis[0]], title=titulo[1])

        axis[1] = Graphs[1](axis[1],x[1],y[1])
        plt.setp([axis[1]], title=titulo[2])
    
    elif(n_graphs==3):
        fig = plt.figure(figsize=(18, 15))
        fig.suptitle(titulo, size=20)
        gs = gridspec.GridSpec(2, 2,figure = fig)

        ax1 = plt.subplot(gs[0, 0])
        ax1 = Graphs[0](ax1,x[0],y[0])
        plt.setp([ax1], title='IMDB')

        ax2 = plt.subplot(gs[0, 1])
        ax2 = Graphs[1](ax2,x[1],y[1])
        plt.setp([ax2], title='TMDB')

        ax3 = plt.subplot(gs[1, :])
        ax3 = Graphs[2](ax3,x[2],y[2])
        plt.setp([ax3], title='Netflix')

    else:
        fig, ax = plt.subplots(1,1,figsize=(18, 9))
        plt.title(titulo, size=18)
        ax = Graphs(ax,x,y)