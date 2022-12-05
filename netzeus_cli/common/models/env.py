from pydantic import BaseModel
from typing import List, Any


class EnvironmentVariable(BaseModel):
    """Base Environment Variable

    Args:
        name:       Name of environment variable
        var_type:   Type of variable (str, int, etc...)
    """

    name: str
    var_type: Any


class EnvironmentVariableModule(BaseModel):
    """Module Environment Variable

    Args:
        module:     Name of module
        variables:  List of EnvironmentVariable
    """

    module: str
    variables: List[EnvironmentVariable]
