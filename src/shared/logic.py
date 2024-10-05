"""
    Business Logic for the various functionalities expected from this component
"""

from typing import Dict, Union
from src.shared.commands import SampleCommand
from src.shared.domain import BaseDomainEntity


def sample_logic(data: SampleCommand) -> Union[Dict[str, str], BaseDomainEntity]:
    """Sample logic to do some stuff"""

    name = data.name
    return {"type": "Sample response", "name": name}
