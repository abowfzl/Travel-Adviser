from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseComponent(ABC):

    @abstractmethod
    def run(
        self,
        question: str,
        session_id: str,
        similars: List[Dict[str, Any]]
    ) -> str:
        """Comment"""

    @abstractmethod
    async def run_async(
        self,
        question: str,
        session_id: str,
        similars: List[Dict[str, Any]]
    ) -> [str]:
        """Comment"""
