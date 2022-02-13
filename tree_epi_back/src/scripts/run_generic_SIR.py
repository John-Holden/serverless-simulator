from params_and_config import (set_runtime, set_dispersal, set_infection_dynamics, set_infectious_lt,
                               set_initial_conditions, set_domain_config, set_R0_trace, get_model_name,
                               GenericSimulationConfig, SaveOptions, RuntimeSettings)

from epidemic_models import executor


def run_SIR():
    runtime = set_runtime(steps=1000)
    dispersal = set_dispersal(model='ga', dispersal_param=50)
    infection_dynamics = set_infection_dynamics(compartments='SIR', beta_factor=10, pr_approx=False)
    infectious_lt = set_infectious_lt(distribution='step', life_time_parameter=100)
    initial_conditions = set_initial_conditions(distribution='centralised', number_infected=10)
    domain_config = set_domain_config('simple_square', scale_constant=1, tree_density=0.01, patch_size=(500, 500))
    R0_trace = set_R0_trace(active=False, transition_times=True, get_network=True)
    generic_sim = GenericSimulationConfig({'runtime': runtime,
                                           'dispersal': dispersal,
                                           'infection_dynamics': infection_dynamics,
                                           'infectious_lt': infectious_lt,
                                           'initial_conditions': initial_conditions,
                                           'domain_config': domain_config,
                                           'R0_trace': R0_trace,
                                           'sim_name': get_model_name(infection_dynamics.compartments,
                                                                      dispersal.model_type)})
    rt_settings = RuntimeSettings()
    rt_settings.verbosity = 3
    rt_settings.frame_plot = True
    rt_settings.frame_show = True
    rt_settings.frame_freq = 25
    save_options = SaveOptions()
    executor.generic_SIR(generic_sim, save_options, rt_settings)


if __name__ == '__main__':
    run_SIR()
