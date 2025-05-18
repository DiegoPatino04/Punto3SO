# tests/stress_test.py
import random
from src.simulation.core import SimulationCore
from src.visualization import Plotter, Reporter

def test_stress():
    sim = SimulationCore(1000, 'first_fit')
    for _ in range(1000):
        if random.random() > 0.3 or not sim.inodes:
            sim.create_file(random.randint(512, 10240))
        else:
            sim.delete_file(random.choice(list(sim.inodes.keys())))
    
    Plotter.plot_usage(sim.logger.disk_states)
    frag = [Reporter.calculate_fragmentation(state) for state in sim.logger.disk_states]
    Plotter.plot_fragmentation(frag)

if __name__ == "__main__":
    test_stress()