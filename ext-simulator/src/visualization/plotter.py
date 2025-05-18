import matplotlib.pyplot as plt
import numpy as np

class Plotter:
    @staticmethod
    def plot_combined_analysis(sim_data: dict):
        """Genera 4 gráficos profesionales en un dashboard"""
        plt.figure(figsize=(20, 12))
        
        # Gráfico 1: Evolución del espacio libre
        plt.subplot(2, 2, 1)
        plt.plot(sim_data['free_space'], 'g-', linewidth=2)
        plt.title('Evolución del Espacio Libre en Disco')
        plt.xlabel('Operación')
        plt.ylabel('% Espacio Libre')
        plt.grid(True)
        
        # Gráfico 2: Fragmentación del sistema
        plt.subplot(2, 2, 2)
        plt.plot(sim_data['fragmentation'], 'r--', marker='o', markersize=4)
        plt.title('Fragmentación del Sistema de Archivos')
        plt.xlabel('Operación')
        plt.ylabel('Índice de Fragmentación')
        plt.ylim(0, 1)
        plt.grid(True)
        
        # Gráfico 3: Tiempos de asignación
        plt.subplot(2, 2, 3)
        plt.hist(sim_data['allocation_times'], bins=20, color='blue', alpha=0.7)
        plt.title('Distribución de Tiempos de Asignación')
        plt.xlabel('Tiempo (ms)')
        plt.ylabel('Frecuencia')
        plt.grid(True)
        
        # Gráfico 4: Comparación de estrategias
        plt.subplot(2, 2, 4)
        for strategy, data in sim_data['strategies_comparison'].items():
            plt.plot(data['fragmentation'], label=strategy.replace('_', ' ').title())
        plt.title('Comparación de Estrategias de Asignación')
        plt.xlabel('Operación')
        plt.ylabel('Fragmentación')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()