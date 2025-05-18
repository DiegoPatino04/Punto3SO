import time
import random
from extfs.disk_manager import BLOCK_SIZE, DiskManager
from extfs.allocator import Allocator
from extfs.inode import Inode
from simulation.logger import Logger
from visualization.reporter import Reporter

class SimulationCore:
    def __init__(self, disk_size: int, alloc_strategy: str):
        self.disk = DiskManager(disk_size)
        self.allocator = Allocator(self.disk)
        self.strategy = alloc_strategy
        self.inodes = {}
        self.next_inode = 1
        self.logger = Logger()
        self.metrics = {
            'fragmentation': [],
            'free_space': [],
            'allocation_times': []
        }

    def create_file(self, size: int) -> bool:
        """Crea un archivo con seguimiento de tiempo y fragmentación"""
        start_time = time.perf_counter()
        blocks_needed = (size + BLOCK_SIZE - 1) // BLOCK_SIZE
        success = False
        
        try:
            start_block = self._execute_allocation_strategy(blocks_needed)
            if start_block != -1:
                self._allocate_blocks(start_block, blocks_needed)
                self._register_new_inode(size, start_block, blocks_needed)
                success = True
        finally:
            if success:
                self.metrics['allocation_times'].append(
                    (time.perf_counter() - start_time) * 1000
                )
                self._update_metrics()
            return success

    def delete_file(self, inode_id: int) -> bool:
        """Elimina un archivo y actualiza métricas"""
        success = False
        if inode_id in self.inodes:
            inode = self.inodes[inode_id]
            self.disk.mark_blocks_free(inode.blocks)
            del self.inodes[inode_id]
            success = True
            self._update_metrics()
        return success

    def _execute_allocation_strategy(self, blocks: int) -> int:
        """Ejecuta la estrategia de asignación configurada"""
        return {
            'first_fit': self.allocator.first_fit,
            'best_fit': self.allocator.best_fit,
            'next_fit': self.allocator.next_fit
        }[self.strategy](blocks)

    def _allocate_blocks(self, start: int, num_blocks: int):
        """Marca bloques como ocupados en el bitmap"""
        self.disk.mark_blocks_used(start, num_blocks)

    def _register_new_inode(self, size: int, start: int, blocks: int):
        """Registra un nuevo inodo en el sistema"""
        new_inode = Inode(
            inode_id=self.next_inode,
            size=size,
            blocks=list(range(start, start + blocks))
        )
        self.inodes[self.next_inode] = new_inode
        self.next_inode += 1

    def _update_metrics(self):
        """Actualiza todas las métricas de rendimiento"""
        self.metrics['fragmentation'].append(
            Reporter.calculate_fragmentation(self.disk.bitmap)
        )
        self.metrics['free_space'].append(
            Reporter.calculate_free_space(self.disk.bitmap)
        )