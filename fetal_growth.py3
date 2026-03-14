import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_fetal_shape(size):
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 30)
    x = size * np.outer(np.cos(u), np.sin(v))
    y = size * np.outer(np.sin(u), np.sin(v))
    z = size * np.outer(np.ones(np.size(u)), np.cos(v))
    return x, y, z

def gene_to_growth_factor(gene_sequence):
    mapping = {
        'A': 1.0, 'T': 0.9, 'C': 1.1, 'G': 1.2
    }
    return sum(mapping[nuc] for nuc in gene_sequence) / len(gene_sequence)

def simulate_fetal_growth_3d(weeks, genes):
    base_size = np.linspace(1, 2, weeks)
    growth_factors = [gene_to_growth_factor(gene) for gene in genes]

    sizes = [base_size * factor for factor in growth_factors]
    return sizes

weeks = 40

# Input gene sequences
gene_sequences = [
    "ATCG", "GCTA", "TGCA", "CGAT", "TAGC"
]

sizes = simulate_fetal_growth_3d(weeks, gene_sequences)

fig = make_subplots(rows=1, cols=len(gene_sequences),
                    specs=[[{'type': 'surface'}] * len(gene_sequences)],
                    subplot_titles=[f"Gene: {gene}{' (Folic Acid & Iron)' if gene == 'ATCG' else ''}" for gene in gene_sequences])

frames = []

for idx, size_curve in enumerate(sizes):
    x, y, z = create_fetal_shape(size_curve[0])

    fig.add_trace(go.Surface(
        x=x, y=y, z=z,
        opacity=0.7 if gene_sequences[idx] == "ATCG" else 0.5,
        colorscale='Blues' if gene_sequences[idx] == "ATCG" else 'Greys',
        showscale=False
    ), row=1, col=idx + 1)

    for i in range(weeks):
        x, y, z = create_fetal_shape(size_curve[i])
        frames.append(go.Frame(
            data=[go.Surface(
                x=x, y=y, z=z,
                opacity=0.7 if gene_sequences[idx] == "ATCG" else 0.5,
                colorscale='Blues' if gene_sequences[idx] == "ATCG" else 'Greys',
                showscale=False
            )],
            name=f"Gene_{idx}_Week_{i}",
            traces=[idx]
        ))

fig.update(frames=frames)

fig.update_layout(
    title='3D Visualization of Fetal Growth Based on Gene Sequences',
    scene=dict(
        xaxis=dict(range=[-3, 3]),
        yaxis=dict(range=[-3, 3]),
        zaxis=dict(range=[-3, 3])
    ),
    updatemenus=[{
        'buttons': [
            {'args': [None, {'frame': {'duration': 100, 'redraw': True}, 'fromcurrent': True}], 'label': 'Play', 'method': 'animate'},
            {'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate', 'transition': {'duration': 0}}], 'label': 'Pause', 'method': 'animate'}
        ],
        'direction': 'left',
        'pad': {'r': 10, 't': 87},
        'showactive': False,
        'type': 'buttons',
        'x': 0.1,
        'xanchor': 'right',
        'y': 0,
        'yanchor': 'top'
    }]
)

fig.show()
