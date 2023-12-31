# stdlib
from typing import Any, List

# third party
import pandas as pd
from sklearn.impute import SimpleImputer

# adjutorium absolute
import adjutorium.plugins.core.params as params
import adjutorium.plugins.imputers.base as base
import adjutorium.utils.serialization as serialization


class MeanPlugin(base.ImputerPlugin):
    """Imputation plugin for completing missing values using the Mean Imputation strategy.

    Method:
        The Mean Imputation strategy replaces the missing values using the mean along each column.

    Example:
        >>> import numpy as np
        >>> from adjutorium.plugins.imputers import Imputers
        >>> plugin = Imputers().get("mean")
        >>> plugin.fit_transform([[1, 1, 1, 1], [np.nan, np.nan, np.nan, np.nan], [1, 2, 2, 1], [2, 2, 2, 2]])
                  0         1         2         3
        0  1.000000  1.000000  1.000000  1.000000
        1  1.333333  1.666667  1.666667  1.333333
        2  1.000000  2.000000  2.000000  1.000000
        3  2.000000  2.000000  2.000000  2.000000
    """

    def __init__(self, model: Any = None, **kwargs: Any) -> None:
        super().__init__()

        if model:
            self._model = model
            return

        self._model = SimpleImputer(strategy="mean", **kwargs)

    @staticmethod
    def name() -> str:
        return "mean"

    @staticmethod
    def hyperparameter_space(*args: Any, **kwargs: Any) -> List[params.Params]:
        return []

    def _fit(self, X: pd.DataFrame, *args: Any, **kwargs: Any) -> "MeanPlugin":
        self._model.fit(X, *args, **kwargs)

        return self

    def _transform(self, X: pd.DataFrame) -> pd.DataFrame:
        return self._model.transform(X)

    def save(self) -> bytes:
        return serialization.save_model(self._model)

    @classmethod
    def load(cls, buff: bytes) -> "MeanPlugin":
        model = serialization.load_model(buff)
        return cls(model=model)


plugin = MeanPlugin
