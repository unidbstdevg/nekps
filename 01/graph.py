import networkx as nx
import matplotlib.pyplot as plt

NODE_ETALON_COLOR = "#c69c8c"
NODE_COLOR = "#3b2319"


def make_edges(data, headers):
    N = len(data)

    for i in range(N):
        for j in range(N):
            if data[i][j]:
                yield (headers[i], headers[j])


def draw(data, headers, out_filename, directed=False):
    edges = make_edges(data, headers)

    G = nx.DiGraph() if directed else nx.Graph()
    G.add_nodes_from(headers)
    G.add_edges_from(edges)

    pos = nx.shell_layout(G)
    # pos = nx.planar_layout(G)

    # colorize first node - etalon
    # yapf: disable
    node_colors = [NODE_ETALON_COLOR,
                   *[NODE_COLOR for _ in range(len(headers) - 1)]]

    plt.figure(1, figsize=(15, 10), dpi=140)
    plt.margins(0.1)

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=8000,
        arrowsize=40,
        font_size=20,
        width=2,
        font_color="white",
        node_color=node_colors,
    )

    plt.savefig(out_filename)
    plt.close()
