import logging
import datetime as dt

from tree_epi_back.src.epidemic_models.compartments import SIR
from tree_epi_back.src.params_and_config import GenericSimulationConfig, RuntimeSettings, SaveOptions, \
    PATH_TO_CPP_EXECUTABLE

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def pre_sim_checks(sim_context: GenericSimulationConfig, save_options: SaveOptions):
    logger.info(' generic_SIR - perfoming pre-sim checks')
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


def generic_SIR(sim_context: GenericSimulationConfig, save_options: SaveOptions, runtime_settings: RuntimeSettings):
    """
    Run a single SIR/SEIR model simulation
    :param save_options:
    :param runtime_settings:
    :param sim_context:
    """

    try:
        pre_sim_checks(sim_context, save_options)
    except Exception as e:
        logger.info(f'generic_SIR - Failed pre-sim checks')
        raise e

    start = dt.datetime.now()
    sim_result = SIR.run_SIR(sim_context, save_options, runtime_settings)
    elapsed = dt.datetime.now() - start
    logger.info(f"Termination condition: {sim_result['termination']} "
                f"Sim steps elapsed: {sim_result['end']}, "
                f"sim time elapsed: {elapsed} (s)")
    # todo
    #   end_of_sim_plots(sim_context, sim_result, runtime_settings)


def generic_SIR_animation(sim_context: GenericSimulationConfig, save_options: SaveOptions, runtime_settings: RuntimeSettings):
    try:
        pre_sim_checks(sim_context, save_options)
    except Exception as e:
        logger.info(f'generic_SIR - Failed pre-sim checks')
        raise e

    start = dt.datetime.now()
    SIR.SIR_function_animate(sim_context, save_options, runtime_settings)
    elapsed = dt.datetime.now() - start
    print(f"Simulation finished in {elapsed} (s)")
    logger.info(f"Simulation finished in {elapsed} (s)")


def execute_cpp_SIR(sim_context: GenericSimulationConfig, save_options: SaveOptions, runtime_settings: RuntimeSettings):
    from ctypes import cdll

    lib = cdll.LoadLibrary(f'{PATH_TO_CPP_EXECUTABLE}/libSIR.so')

    class SimulationExecutor:
        def __init__(self):
            self.obj = lib.newSimOjb()

        def ExecuteRun(self, a: int):
            return lib.execute(self.obj, a)

    s = SimulationExecutor()
    out = s.ExecuteRun(123456789)
    print(f'out from c++ == {out}')
    print(sim_context)
    print(save_options)
    print(runtime_settings)
