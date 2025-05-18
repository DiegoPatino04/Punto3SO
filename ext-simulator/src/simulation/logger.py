# src/simulation/logger.py
from datetime import datetime

class Logger:
    """Registra eventos y estados del disco durante la simulación."""
    
    def __init__(self):
        self.logs = []
        self.disk_states = []

    def log(self, message: str, bitmap: list):
        """Guarda un mensaje con el estado actual del disco."""
        self.logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        self.disk_states.append(bitmap.copy())