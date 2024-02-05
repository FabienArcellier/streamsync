import dataclasses
import io
import math
import typing
from datetime import date, datetime
from typing import Callable, Optional, Any, Type, Union, List

from streamsync.core import state_serialiser, FileWrapper, StateProxy, BytesWrapper

if typing.TYPE_CHECKING:
    import numpy

@dataclasses.dataclass
class Serdes:
    targetting_type: Union[str, Type[Any]]
    serializer: Callable[[Any], Any]
    deserializer: Callable[[Any], Any]
    mro: List[str] = dataclasses.field(default_factory=list)


def register_serdes(targetting_type: Union[str, Type[Any], Callable[[Type[Any]], bool]],
                    serializer: Optional[Callable[[Any], Any]] = None,
                    deserializer: Optional[Callable[[Any], Any]] = None):
    """
    Registers a new serializer for a given object type.

    This serializer replaces other serializers that apply to the same type.

    >>> streamsync.serdes_register("str", serializer=lambda x: x.upper(), deserializer=lambda x: x.lower())
    >>> streamsync.serdes_register(str, serializer=lambda x: x.upper(), deserializer=lambda x: x.lower())
    """
    if isinstance(targetting_type, type):
        targetting_type = f'{targetting_type.__module__}.{targetting_type.__name__}'

    if serializer is None:
        serializer = lambda x: x

    if deserializer is None:
        deserializer = lambda x: x

    serdes = Serdes(targetting_type, serializer=serializer, deserializer=deserializer)
    state_serialiser.serdes_register(serdes)


def reset_serdes():
    """
    Resets all registered serializers to the default ones.
    """
    state_serialiser.reset_serdes()


def serialise(value: Any) -> Any:
    """
    Serialises a value using the registered serializers.
    """
    return state_serialiser.serialise(value)


def register_serdes_core():
    """
    Registers default serializers for base types.
    """
    register_serdes(StateProxy, serializer=lambda v: _serialise_recursive_dict(v.to_dict()))
    register_serdes(FileWrapper, serializer=_serialise_ss_wrapper)
    register_serdes(BytesWrapper, serializer=_serialise_ss_wrapper)
    register_serdes(datetime, serializer=lambda v: str(v))
    register_serdes(date, serializer=lambda v: str(v))
    register_serdes(int, serializer=_serialise_int)
    register_serdes(float, serializer=_serialise_float)
    register_serdes(bytes, serializer=lambda v: _serialise_ss_wrapper(BytesWrapper(v)))
    register_serdes(dict, serializer=lambda v: _serialise_ss_wrapper(BytesWrapper(v)))
    register_serdes("numpy.float64", serializer=_serialise_numpy_float)
    register_serdes("matplotlib.figure.Figure", serializer=_serialise_matplotlib_fig)
    register_serdes("plotly.graph_objs._figure.Figure", serializer=lambda v: v.to_json())
    register_serdes("numpy.ndarray", serializer=lambda v: _serialise_list_recursively(v.tolist()))


def _serialise_recursive_dict(d: dict) -> dict:
    return {str(k): serialise(v) for k, v in d.items()}


def _serialise_int(v: int) -> Optional[int]:
    if math.isnan(v):
        return None

    return v


def _serialise_float(v: float) -> Optional[float]:
    if hasattr(v, "mro"):
        if "numpy.float64" in v.mro():
            return float(v)

        if math.isnan(v):
            return None

    return v

def _serialise_ss_wrapper(v: Union[FileWrapper, BytesWrapper]) -> str:
    return v.get_as_dataurl()


def _serialise_numpy_float(v: 'numpy.float64') -> Optional[float]:
    return float(v)


def _serialise_matplotlib_fig(fig) -> str:
    # It's safe to import matplotlib here without listing it as a dependency.
    # If this method is called, it's because a matplotlib figure existed.
    # Note: matplotlib type needs to be ignored since it doesn't provide types
    import matplotlib.pyplot as plt  # type: ignore

    iobytes = io.BytesIO()
    fig.savefig(iobytes, format="png")
    iobytes.seek(0)
    plt.close(fig)
    return FileWrapper(iobytes, "image/png").get_as_dataurl()


def _serialise_list_recursively(l: List) -> List:
    return [serialise(v) for v in l]