# src/extfs/allocator.py
class Allocator:
    """Implementa diferentes estrategias de asignación de bloques."""
    
    def __init__(self, disk_manager):
        self.disk = disk_manager
        self.last_pos = 0  # Para next-fit

    def first_fit(self, num: int) -> int:
        """Primer ajuste: primera zona contigua que encuentre."""
        return self.disk.find_contiguous_free_blocks(num, 0)

    def next_fit(self, num: int) -> int:
        """Próximo ajuste: busca desde la última posición asignada."""
        pos = self.disk.find_contiguous_free_blocks(num, self.last_pos)
        if pos != -1:
            self.last_pos = (pos + num) % self.disk.total_blocks
        return pos

    def best_fit(self, num: int) -> int:
        """Mejor ajuste: zona contigua más pequeña que pueda albergar los bloques."""
        best_start = -1
        best_size = float('inf')
        current_start = -1
        current_size = 0
        
        for i in range(self.disk.total_blocks):
            if not self.disk.bitmap[i]:
                if current_start == -1:
                    current_start = i
                current_size += 1
                if current_size >= num and current_size < best_size:
                    best_start = current_start
                    best_size = current_size
            else:
                current_start = -1
                current_size = 0
        
        return best_start