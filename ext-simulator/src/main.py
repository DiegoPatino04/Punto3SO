import sys
import os
import random
import matplotlib.pyplot as plt
from pathlib import Path

# Configurar rutas de importación
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))  # src/
sys.path.insert(0, str(current_dir.joinpath("extfs")))
sys.path.insert(0, str(current_dir.joinpath("simulation")))
sys.path.insert(0, str(current_dir.joinpath("visualization")))

from simulation.core import SimulationCore
from visualization.plotter import Plotter

def main():
    strategies = ['first_fit', 'best_fit', 'next_fit']
    metrics = {}
    
    for strategy in strategies:
        sim = SimulationCore(disk_size=2000, alloc_strategy=strategy)
        
        # Ejecutar prueba de estrés
        for _ in range(500):
            if random.random() < 0.7:
                sim.create_file(random.randint(1024, 10240))
            else:
                if sim.inodes:
                    sim.delete_file(random.choice(list(sim.inodes.keys())))
        
        # Almacenar todas las métricas
        metrics[strategy] = {
            'fragmentation': sim.metrics['fragmentation'],
            'free_space': sim.metrics['free_space'],  # ¡Clave añadida!
            'allocation_times': sim.metrics['allocation_times']
        }
    
    # Generar gráficos con datos completos
    Plotter.plot_combined_analysis({
        'free_space': metrics['best_fit']['free_space'],
        'fragmentation': metrics['best_fit']['fragmentation'],
        'allocation_times': metrics['best_fit']['allocation_times'],
        'strategies_comparison': {
            s: {'fragmentation': m['fragmentation']} for s, m in metrics.items()
        }
    })
    plt.show()

if __name__ == "__main__":
    main()