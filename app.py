import os
import boto3
from flask_cors import CORS
from flask import Flask, jsonify, make_response, request
from tree_epi_back.src.epidemic_models.executor import generic_SIR
from tree_epi_back.src.epidemic_models.utils.common_helpers import get_tree_density, get_model_name
from tree_epi_back.src.params_and_config import (set_dispersal, set_domain_config, set_infectious_lt,
                                                 set_infection_dynamics, set_runtime, set_initial_conditions,
                                                 set_R0_trace, GenericSimulationConfig, SaveOptions, RuntimeSettings)


app = Flask(__name__)
CORS(app)


@app.route("/", methods=['POST'])
def simulation_client():
    sim_parameters = request.get_json(force=True)
    print(f'sim params : {sim_parameters}')
    try:
        print('simulating: ')
        simulate(sim_parameters)
        print('dome')
        return make_response(jsonify(message=f''), 200)
    except Exception as e:
        print('error: ', e)
        return make_response(jsonify(error=f'{e}'), 500)


def simulate(sim_params: dict):
    sim_config = get_simulation_config(sim_params)

    rt_settings = RuntimeSettings()
    rt_settings.verbosity = 0
    rt_settings.frame_plot = True
    rt_settings.frame_show = True
    rt_settings.frame_freq = 2
    save_options = SaveOptions()
    save_options.frame_save = True

    generic_SIR(sim_config, save_options, rt_settings)


def get_simulation_config(sim_params: dict):
    dispersal_model = sim_params['dispersal_type']
    dispersal_param = sim_params['dispersal_param']
    dispersal = set_dispersal(dispersal_model, dispersal_param)

    domain_size = sim_params['domain_size']
    host_number = sim_params['host_number']

    domain = set_domain_config(domain_type='simple_square',
                               scale_constant=1,
                               patch_size=domain_size,
                               tree_density=get_tree_density(host_number, domain_size))

    secondary_R0 = sim_params['secondary_R0']
    # todo convert R0 into infectious param...
    infection_dynamics = set_infection_dynamics('SIR', 10)
    runtime = set_runtime(sim_params['simulation_runtime'])
    infectious_lt = set_infectious_lt('exp', sim_params['infectious_lifetime'])
    initial_conditions = set_initial_conditions(sim_params['initially_infected_dist'],
                                                sim_params['initially_infected_hosts'])

    return GenericSimulationConfig({'runtime': runtime,
                                    'dispersal': dispersal,
                                    'infection_dynamics': infection_dynamics,
                                    'infectious_lt': infectious_lt,
                                    'initial_conditions': initial_conditions,
                                    'domain_config': domain,
                                    'R0_trace': set_R0_trace(active=True, first_gen_only=False),
                                    'sim_name': get_model_name(infection_dynamics.compartments, dispersal.model_type)})


@app.route("/s3_upload")
def upload_to_s3():
    try:
        temp_file = open(file='/tmp/temp.upload', mode='w')
        temp_file.write('test string from local dev')
        temp_file.close()
        s3_client = boto3.client('s3')
        s3_client.upload_file('/tmp/temp.upload', 'tree-epi-site-bucket', 'temp.upload')
        os.remove('/tmp/temp.upload')
        return jsonify(message=f'Uploaded to s3!')
    except Exception as e:
        return make_response(jsonify(error=f'{e}'), 404)


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found - homie!'), 404)
