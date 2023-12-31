# stdlib
from typing import Any, List

# third party
from geomloss import SamplesLoss
import numpy as np
import pandas as pd
from sklearn.base import TransformerMixin
import torch

# adjutorium absolute
import adjutorium.plugins.core.params as params
import adjutorium.plugins.imputers.base as base
import adjutorium.plugins.utils.decorators as decorators


class SinkhornImputation(TransformerMixin):
    """Sinkhorn imputation can be used to impute quantitative data and it relies on the idea that two batches extracted randomly from the same dataset should share the same distribution and consists in minimizing optimal transport distances between batches.

    Original paper: "Missing Data Imputation using Optimal Transport", Boris Muzellec, Julie Josse, Claire Boyer, Marco Cuturi


    Args:
        eps: float, default=0.01
            Sinkhorn regularization parameter.

        lr : float, default = 0.01
            Learning rate.

        opt: torch.nn.optim.Optimizer, default=torch.optim.Adam
            Optimizer class to use for fitting.

        niter : int, default=15
            Number of gradient updates for each model within a cycle.

        batchsize : int, defatul=128
            Size of the batches on which the sinkhorn divergence is evaluated.

        n_pairs : int, default=10
            Number of batch pairs used per gradient update.

        noise : float, default = 0.1
            Noise used for the missing values initialization.

        scaling: float, default=0.9
            Scaling parameter in Sinkhorn iterations
    """

    def __init__(
        self,
        eps: float = 0.01,
        lr: float = 1e-2,
        opt: Any = torch.optim.Adam,
        niter: int = 500,
        batchsize: int = 128,
        n_pairs: int = 1,
        noise: float = 1e-2,
        scaling: float = 0.9,
    ):
        self.eps = eps
        self.lr = lr
        self.opt = opt
        self.niter = niter
        self.batchsize = batchsize
        self.n_pairs = n_pairs
        self.noise = noise
        self.sk = SamplesLoss(
            "sinkhorn", p=2, blur=eps, scaling=scaling, backend="tensorized"
        )

    def fit_transform(self, X: pd.DataFrame, *args: Any, **kwargs: Any) -> pd.DataFrame:
        X = torch.tensor(X.values)
        X = X.clone()
        n, d = X.shape

        if self.batchsize > n // 2:
            e = int(np.log2(n // 2))
            self.batchsize = 2 ** e

        mask = torch.isnan(X).double()
        imps = (self.noise * torch.randn(mask.shape).double() + np.nanmean(X, 0))[
            mask.bool()
        ]
        imps.requires_grad = True

        optimizer = self.opt([imps], lr=self.lr)

        for i in range(self.niter):
            X_filled = X.detach().clone()
            X_filled[mask.bool()] = imps
            loss: SamplesLoss = 0

            for _ in range(self.n_pairs):

                idx1 = np.random.choice(n, self.batchsize, replace=False)
                idx2 = np.random.choice(n, self.batchsize, replace=False)

                X1 = X_filled[idx1]
                X2 = X_filled[idx2]

                loss = loss + self.sk(X1, X2)

            if torch.isnan(loss).any() or torch.isinf(loss).any():
                # Catch numerical errors/overflows (should not happen)
                break

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        X_filled = X.detach().clone()
        X_filled[mask.bool()] = imps

        return X_filled.detach().numpy()


class SinkhornPlugin(base.ImputerPlugin):
    """Imputation plugin for completing missing values using the Sinkhorn strategy.

    Method:
        Details in the SinkhornImputation class implementation.

    Example:
        >>> import numpy as np
        >>> from adjutorium.plugins.imputers import Imputers
        >>> plugin = Imputers().get("sinkhorn")
        >>> plugin.fit_transform([[1, 1, 1, 1], [np.nan, np.nan, np.nan, np.nan], [1, 2, 2, 1], [2, 2, 2, 2]])
                  0         1         2         3
        0  1.000000  1.000000  1.000000  1.000000
        1  1.404637  1.651113  1.651093  1.404638
        2  1.000000  2.000000  2.000000  1.000000
        3  2.000000  2.000000  2.000000  2.000000
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__()

        self._model = SinkhornImputation(**kwargs)

    @staticmethod
    def name() -> str:
        return "sinkhorn"

    @staticmethod
    def hyperparameter_space(*args: Any, **kwargs: Any) -> List[params.Params]:
        return []

    @decorators.benchmark
    def _fit(self, X: pd.DataFrame, *args: Any, **kwargs: Any) -> "SinkhornPlugin":
        return self

    @decorators.benchmark
    def _transform(self, X: pd.DataFrame) -> pd.DataFrame:
        return self._model.fit_transform(X)

    def save(self) -> bytes:
        return b""

    @classmethod
    def load(cls, buff: bytes) -> "SinkhornPlugin":
        return cls()


plugin = SinkhornPlugin
