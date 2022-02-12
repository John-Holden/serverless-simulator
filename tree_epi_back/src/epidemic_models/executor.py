import datetime as dt
import warnings

from epidemic_models.compartments import SIR
from epidemic_models.utils import common_helpers
from params_and_config import GenericSimulationConfig, RuntimeSettings, SaveOptions


def generic_SIR(sim_context: GenericSimulationConfig, save_options: SaveOptions, runtime_settings: RuntimeSettings):
    """
    Run a single SIR/SEIR model simulation
    :param save_options:
    :param runtime_settings:
    :param sim_context:
    """
    if sim_context.dispersal.model_type == 'power_law' and save_options.save_max_d:
        raise Exception('Percolation-like boundary conditions is not valid for power-law based dispersal')

    if sim_context.sporulation:
        raise NotImplementedError('Sporulation for generic sim not implemented')

    if not sim_context.runtime.steps:
        raise Exception('Expected non-zero runtime')

    if sim_context.R0_trace.active and not sim_context.infection_dynamics.pr_approx:
        raise Exception('We cannot cannot contact-trace secondary infections when using the full poisson construct')

    if sim_context.other_boundary_conditions.percolation and save_options.save_max_d:
        raise Exception('Enable max distance metric to use the percolation BCD')

    if runtime_settings.frame_plot and not runtime_settings.frame_show:
        warnings.warn("\n Runtime redundant setting, expected 'frame_show = True'. "
                      f"Found 'frame_show = {runtime_settings.frame_show}'")

    print(f'Running model: {sim_context.sim_name}')
    start = dt.datetime.now()
    sim_result = SIR.run_SIR(sim_context, save_options, runtime_settings)
    elapsed = dt.datetime.now() - start
    common_helpers.time_print(elapsed.seconds, msg='@ singleSim Done')
    print(f"Termination condition: {sim_result['termination']}")
    print(f"Steps elapsed {sim_result['end']}")

    # end_of_sim_plots(sim_context, sim_result, runtime_settings)