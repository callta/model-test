# stdlib
from typing import Tuple

# third party
import optuna

# adjutorium absolute
import adjutorium.logger as log
from adjutorium.utils.redis import backend

threshold = 40


class EarlyStoppingExceeded(optuna.exceptions.OptunaError):
    pass


class ParamRepeatPruner:
    """Prunes reapeated trials, which means trials with the same paramters won't waste time/resources."""

    def __init__(
        self,
        study: optuna.study.Study,
    ) -> None:
        self.study = study
        self.seen: set = set()

        self.best_score: float = -1
        self.no_improvement_for = 0

        if self.study is not None:
            self.register_existing_trials()

    def register_existing_trials(self) -> None:
        for trial_idx, trial_past in enumerate(
            self.study.get_trials(states=[optuna.trial.TrialState.COMPLETE])
        ):
            if trial_past.values[0] > self.best_score:
                self.best_score = trial_past.values[0]
                self.no_improvement_for = 0
            else:
                self.no_improvement_for += 1
            self.seen.add(hash(frozenset(trial_past.params.items())))

    def check_patience(
        self,
        trial: optuna.trial.Trial,
    ) -> None:
        if self.no_improvement_for > threshold:
            raise EarlyStoppingExceeded()

    def check_trial(
        self,
        trial: optuna.trial.Trial,
    ) -> None:
        self.check_patience(trial)

        params = frozenset(trial.params.items())

        current_val = hash(params)
        if current_val in self.seen:
            raise optuna.exceptions.TrialPruned()

        self.seen.add(current_val)

    def report_score(self, score: float) -> None:
        if score > self.best_score:
            self.best_score = score
            self.no_improvement_for = 0
        else:
            self.no_improvement_for += 1


def create_study(
    study_name: str,
    direction: str = "maximize",
    load_if_exists: bool = True,
    storage_type: str = "redis",
) -> Tuple[optuna.Study, ParamRepeatPruner]:

    storage_obj = None
    if storage_type == "redis":
        storage_obj = backend.optuna()

    try:
        study = optuna.create_study(
            direction=direction,
            study_name=study_name,
            storage=storage_obj,
            load_if_exists=load_if_exists,
        )
    except BaseException as e:
        log.debug(f"create_study failed {e}")
        study = optuna.create_study(
            direction=direction,
            study_name=study_name,
        )

    return study, ParamRepeatPruner(study)
