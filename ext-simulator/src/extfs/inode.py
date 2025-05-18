# src/extfs/inode.py
class Inode:
    """Representa un inodo del sistema de archivos Ext con gestión de bloques."""
    
    def __init__(self, inode_id: int, size: int = 0, blocks: list = None):
        self.inode_id = inode_id
        self.size = size  # Tamaño en bytes
        self.blocks = blocks if blocks else []
        self.permissions = 0o755

    def free_blocks(self) -> list:
        """Libera todos los bloques asignados al inodo."""
        freed = self.blocks.copy()
        self.blocks.clear()
        self.size = 0
        return freed