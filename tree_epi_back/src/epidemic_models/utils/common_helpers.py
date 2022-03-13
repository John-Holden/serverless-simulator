import math
import numpy as np
from typing import Optional, List
from tree_epi_back.src.params_and_config import DomainConfig, Compartmentalised_models


def time_print(time_seconds: int, msg: Optional[str] = 'Simulation done in: ', display: Optional[bool] = True) -> str:
    """
    Pretty formatter to display time
    """
    seconds = math.floor(time_seconds)
    hrs = math.floor(seconds / 3600)
    mns = math.floor(seconds / 60)
    secs = seconds % 60

    if seconds < 60:
        if display:
            print(f'{msg} {seconds} (s)')
    elif 60 <= seconds < 3600:
        if display:
            print(f'{msg} {mns} (mins): {secs} (s)')
    elif seconds >= 3600:
        if display:
            print(f'{msg} {hrs} (Hrs): {mns%60} (mins): {secs} (s)')

    return f'{msg} {hrs} (Hrs): {mns%60} (mins): {secs} (s)'


def get_initial_host_number(patch_size: tuple, tree_density: float) -> float:
    """
    Calculate number of susceptible hosts in a simple flat domain of size [Lx, Ly]
    """
    return patch_size[0] * patch_size[1] * tree_density


def simple_square_host_num(S: List[np.ndarray], I: List[np.ndarray], R: List[np.ndarray]) -> int:
    """
    From list of SIR fields, return the total number of hosts in the system
    """
    return len(S[0]) + len(I[0]) + len(R[0])


def get_total_host_number(S: List[np.ndarray], I: List[np.ndarray], R: List[np.ndarray],
                          domain_config: DomainConfig) -> int:
    # Find and return the total number of trees in the domain based on SIR
    if domain_config.domain_type == 'simple_square':
        return simple_square_host_num(S, I, R)

    raise NotImplementedError(f'domain type: {domain_config.domain_type}')


def get_tree_density(host_number: int, patch_size: tuple):
    # Find tree density based on host number and domain config
    return host_number / (patch_size[0] * patch_size[1])


def get_model_name(compartments: str, dispersal_model: str, sporulation_model: Optional[str] = None) -> str:
    """
    Get the model-name, based on sporulation and dispersal type
    :param compartments:
    :param dispersal_model:
    :param sporulation_model:

    :return:
    """

    if compartments not in Compartmentalised_models:
        raise NotImplementedError(f'Expected models {Compartmentalised_models}, found type {compartments}')

    name = False
    if sporulation_model is None:
        name = 'phi0'
    elif sporulation_model == 'step':
        name = 'phi1'
    elif sporulation_model == 'peaked':
        name = 'phi2'
    elif not compartments:
        raise Exception('Incorrectly defined sporulation')

    if 'power' in dispersal_model and 'law' in dispersal_model:
        return f'{compartments}-{name}-pl'
    elif dispersal_model in ['Gaussian', 'gaussian', 'ga']:
        return f'{compartments}-{name}-ga'