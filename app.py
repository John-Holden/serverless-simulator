import logging
from flask_cors import CORS
from flask import Flask, jsonify, make_response, request
from tree_epi_back.src.epidemic_models.executor import execute_cpp_SIR
from tree_epi_back.src.epidemic_models.utils.common_helpers import get_tree_density, get_model_name
from tree_epi_back.src.params_and_config import (mkdir_tmp_store, set_dispersal, set_domain_config, set_infectious_lt,
                                                 set_infection_dynamics, set_runtime, set_initial_conditions,
                                                 set_R0_trace, GenericSimulationConfig, SaveOptions, RuntimeSettings)


app = Flask(__name__)
CORS(app)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


@app.route("/", methods=['POST'])
def simulation_request_handler():
    logger.info(' simulation_request_handler', extra={'sim': 'begging'})
    sim_parameters = request.get_json(force=True)
    try:
        simulate(sim_parameters)
        logger.info(' simulation_request_handler', extra={'sim': 'Success'})
        # TODO placeholder resp for neow
        return make_response(jsonify(message=f'this is what you gave me mofo {sim_parameters} '), 200)
    except Exception as e:
        logger.info(' simulation_request_handler', extra={'sim': 'Failed', 'Error': e})
        return make_response(jsonify(error=f'{e}'), 500)


def simulate(sim_params: dict):
    logger.info(' simulate - parsing input request imput parameters')
    sim_config = get_simulation_config(sim_params)
    rt_settings = RuntimeSettings()
    rt_settings.verbosity = 0
    rt_settings.frame_plot = True
    rt_settings.frame_show = False
    rt_settings.frame_freq = 10
    save_options = SaveOptions()
    save_options.frame_save = True
    mkdir_tmp_store()
    try:
        execute_cpp_SIR(sim_config, save_options, rt_settings)
    except Exception as e:
        msg = f'Error when executing SIR model - {e}'
        print(msg)
        raise e


def get_simulation_config(sim_params: dict):
    dispersal_model = sim_params['dispersal_type']
    dispersal_param = sim_params['dispersal_param']
    dispersal = set_dispersal(dispersal_model, dispersal_param)

    domain_size = tuple(map(int, sim_params['domain_size']))
    host_number = int(sim_params['host_number'])
    domain = set_domain_config(domain_type='simple_square',
                               scale_constant=1,
                               patch_size=domain_size,
                               tree_density=get_tree_density(host_number, domain_size))

    runtime = set_runtime(int(sim_params['simulation_runtime']))
    infectious_lt = set_infectious_lt('exp', int(sim_params['infectious_lifetime']))

    infection_dynamics = set_infection_dynamics('SIR',
                                                int(sim_params['secondary_R0']),
                                                pr_approx=False)

    initial_conditions = set_initial_conditions(sim_params['initially_infected_dist'],
                                                int(sim_params['initially_infected_hosts']))

    return GenericSimulationConfig({'runtime': runtime,
                                    'dispersal': dispersal,
                                    'infection_dynamics': infection_dynamics,
                                    'infectious_lt': infectious_lt,
                                    'initial_conditions': initial_conditions,
                                    'domain_config': domain,
                                    'R0_trace': set_R0_trace(active=False),
                                    'sim_name': get_model_name(infection_dynamics.compartments, dispersal.model_type)})


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found - homie!'), 404)
