import numpy as np

class Reporter:
    @staticmethod
    def calculate_fragmentation(bitmap: list) -> float:
        free_blocks = []
        current = 0
        for block in bitmap:
            if not block:
                current += 1
            else:
                if current > 0:
                    free_blocks.append(current)
                    current = 0
        if current > 0:
            free_blocks.append(current)
        
        if not free_blocks:
            return 0.0
        
        total_free = sum(free_blocks)
        max_contiguous = max(free_blocks)
        return 1 - (max_contiguous / total_free) if total_free > 0 else 0

    @staticmethod
    def calculate_free_space(bitmap: list) -> float:
        return (sum(1 for b in bitmap if not b) / len(bitmap)) * 100