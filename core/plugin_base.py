from abc import ABC, abstractmethod
from typing import Dict, Any, List
from core.plugin_registry import register_plugin


class PluginBase(ABC):
    """
    Base class for all FRIDAY plugins.
    """

    name: str = ""
    intents: List[str] = []
    permission: str = "basic"
    requires_confirmation: bool = False

    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls is not PluginBase:
            register_plugin(cls)

    def __init__(self):
        if not self.name or not self.intents:
            raise ValueError(
                f"{self.__class__.__name__} must define 'name' and 'intents'"
            )

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        pass
