# src/extfs/disk_manager.py
BLOCK_SIZE = 4096  # 4KB por bloque

class DiskManager:
    def __init__(self, total_blocks: int):
        self.total_blocks = total_blocks
        self.bitmap = [False] * total_blocks

    def find_contiguous_free_blocks(self, num: int, start: int = 0) -> int:
        current_start = -1
        count = 0
        
        for i in range(start, self.total_blocks):
            if not self.bitmap[i]:
                if current_start == -1:
                    current_start = i
                count += 1
                if count == num:
                    return current_start
            else:
                current_start = -1
                count = 0
        
        for i in range(0, start):
            if not self.bitmap[i]:
                if current_start == -1:
                    current_start = i
                count += 1
                if count == num:
                    return current_start
            else:
                current_start = -1
                count = 0
        
        return -1

    def mark_blocks_used(self, start: int, num: int):
        for i in range(start, start + num):
            if i < self.total_blocks:
                self.bitmap[i] = True

    def mark_blocks_free(self, blocks: list):
        for b in blocks:
            if b < self.total_blocks:
                self.bitmap[b] = False