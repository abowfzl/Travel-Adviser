from abc import ABC, abstractmethod
from typing import Any, List


def raise_(ex):
    raise ex


class BaseLLM(ABC):
    """LLM wrapper should take in a prompt and return a string."""

    @abstractmethod
    async def generate_streaming(
        self,
            question,
            session_id,
            similars,
            prompt
    ) -> List[Any]:
        """Comment"""

    def reconstruct_streaming_response(self, fragments: list) -> str:
        combined_response = ''.join(fragments).strip()

        return combined_response
