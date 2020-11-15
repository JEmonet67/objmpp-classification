import matplotlib.pyplot as plt
plt.style.use("seaborn-whitegrid")

def initialize_glob_graph():
    fig_all = plt.figure()
    ax_all = plt.axes()
    plt.title(label="Intensité moyenne en fonction de la distance de toutes les ellipses")
    ax_all = ax_all.set(xlabel = "Distance au centre (%)",
                ylabel = "Intensité moyenne des pixels")
    
    return fig_all, ax_all

def new_unitary_graph(i_obj, obj, x, path_output):
    #Bloc if permettant de pallier au fait que parfois une valeur très proche de 100 en trop
    #au lieu d'égal à 100 à cause de l'imprécision est ajoutée à  x.
    if len(x) > len(obj.list_mean):
        x = x[:-1]
    fig_ell = plt.figure()
    ax_ell = plt.axes()
    plt.title(f"""Intensité moyenne en fonction de la
                distance dans l'ellipse {i_obj}""")
    ax_ell = ax_ell.set(xlabel = "Distance au centre (%)",
                ylabel = "Intensité moyenne des pixels")
    plt.plot(x, obj.list_mean)
    plt.vlines(obj.threshold,0,200,
                colors="r",linestyles="dashed")
    
    fig_ell.savefig(f"{path_output}/{obj.type}_{obj.subtype}_{i_obj}_graphic.png")
    plt.close()
