"""
Storage service factory - manage storage instances
"""
from src.services.storage import StorageAbstraction, InMemoryStorage
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Global storage instance
_storage_instance: Optional[StorageAbstraction] = None


class StorageService:
    """Factory for managing storage instances"""

    @staticmethod
    def initialize_storage(storage_type: str = "memory") -> StorageAbstraction:
        """Initialize storage (currently only in-memory supported)"""
        global _storage_instance
        
        if storage_type == "memory":
            _storage_instance = InMemoryStorage()
            logger.info("Initialized InMemoryStorage")
            return _storage_instance
        else:
            raise ValueError(f"Unknown storage type: {storage_type}")

    @staticmethod
    def get_storage() -> StorageAbstraction:
        """Get the current storage instance"""
        global _storage_instance
        if _storage_instance is None:
            _storage_instance = StorageService.initialize_storage("memory")
        return _storage_instance

    @staticmethod
    def reset_storage() -> None:
        """Reset storage (for testing)"""
        global _storage_instance
        _storage_instance = InMemoryStorage()
        logger.info("Storage reset")
