import json
import os
from concurrent import futures
from pathlib import Path

import dotenv
import grpc
import jsonpickle
from base.wrappers import SimulationWrapper
from market.market_pb2 import LongTermMarketResponse, MarketInput, MarketInputRequest, ShortTermMarketResponse
from market.market_pb2_grpc import MarketModuleServicer, add_MarketModuleServicer_to_server
from module.market_module.long_term.market_functions.run_longterm_market import run_longterm_market
from module.market_module.long_term.market_functions.convert_user_and_module_inputs import (
    convert_user_and_module_inputs as long_convert
)
from module.market_module.long_term.report.report_long_term import report_long_term
from module.market_module.short_term.market_functions.run_shortterm_market import run_shortterm_market
from module.market_module.short_term.market_functions.convert_user_and_module_inputs import (
    convert_user_and_module_inputs as short_convert
)

from helpers import NumpyJsonEncode

dotenv.load_dotenv()
PROJECT_PATH = str(Path.cwd().parent)


class MarketModule(MarketModuleServicer):
    def RunLongTermMarket(self, request: MarketInputRequest, context) -> LongTermMarketResponse:
        in_var = {
            "user": jsonpickle.decode(request.platform),
            "gis-module": jsonpickle.decode(request.gis_module),
            "cf-module": jsonpickle.decode(request.cf_module),
            "teo-module": jsonpickle.decode(request.teo_module)
        }
        with SimulationWrapper(project_path=PROJECT_PATH):
            input_dict = long_convert(in_var)
            output = run_longterm_market(input_dict=input_dict)
            report = report_long_term(
                longterm_results=output,
                data_profile=in_var["user"]["data_profile"],
                fbp_time=input_dict["fbp_time"],
                fbp_agent=input_dict["fbp_agent"],
                md=input_dict['md'],
            )
        return LongTermMarketResponse(
            Gn=json.dumps(output['Gn']),
            Ln=json.dumps(output['Ln']),
            Pn=json.dumps(output['Pn']),
            QoE=json.dumps(output['QoE']),
            optimal=str(output['optimal']),
            settlement=json.dumps(output['settlement']),
            social_welfare_h=json.dumps(output['social_welfare_h']),
            shadow_price=json.dumps(output['shadow_price']),
            Tnm=json.dumps(output['Tnm']),
            agent_operational_cost=json.dumps(output['agent_operational_cost']),
            SPM=json.dumps(output['SPM']),
            ADG=json.dumps(output['ADG']),
            report=report,
        )

    def RunLongTermMarketDirect(self, request: MarketInput, context) -> LongTermMarketResponse:
        input_dict = jsonpickle.decode(request.input)
        with SimulationWrapper(project_path=PROJECT_PATH):
            output = run_longterm_market(input_dict=input_dict)
        return LongTermMarketResponse(
            Gn=json.dumps(output['Gn']),
            Ln=json.dumps(output['Ln']),
            Pn=json.dumps(output['Pn']),
            QoE=json.dumps(output['QoE']),
            optimal=str(output['optimal']),
            settlement=json.dumps(output['settlement']),
            social_welfare_h=json.dumps(output['social_welfare_h']),
            shadow_price=json.dumps(output['shadow_price']),
            Tnm=json.dumps(output['Tnm']),
            agent_operational_cost=json.dumps(output['agent_operational_cost']),
            SPM=json.dumps(output['SPM']),
            ADG=json.dumps(output['ADG']),
        )

    def RunShortTermMarket(self, request: MarketInputRequest, context) -> ShortTermMarketResponse:
        in_var = {
            "platform": jsonpickle.decode(request.platform),
            "gis-module": jsonpickle.decode(request.gis_module),
            "cf-module": jsonpickle.decode(request.cf_module),
            "teo-module": jsonpickle.decode(request.teo_module)
        }
        with SimulationWrapper(project_path=PROJECT_PATH):
            input_dict = short_convert(in_var)
            output = run_shortterm_market(input_dict)
        return ShortTermMarketResponse(
            Gn=json.dumps(output['Gn']),
            Ln=json.dumps(output['Ln']),
            Pn=json.dumps(output['Pn']),
            QoE=json.dumps(output['QoE']),
            optimal=str(output['optimal']),
            settlement=json.dumps(output['settlement']),
            social_welfare_h=json.dumps(output['social_welfare_h']),
            shadow_price=json.dumps(output['shadow_price']),
            Tnm=json.dumps(output['Tnm']),
            # agent_operational_cost=json.dumps(output['agent_operational_cost']),
        )

    def RunShortTermMarketDirect(self, request: MarketInput, context) -> ShortTermMarketResponse:
        input_dict = jsonpickle.decode(request.input)
        with SimulationWrapper(project_path=PROJECT_PATH):
            output = run_shortterm_market(input_dict)
        return ShortTermMarketResponse(
            Gn=json.dumps(output['Gn']),
            Ln=json.dumps(output['Ln']),
            Pn=json.dumps(output['Pn']),
            QoE=json.dumps(output['QoE']),
            optimal=str(output['optimal']),
            settlement=json.dumps(output['settlement']),
            social_welfare_h=json.dumps(output['social_welfare_h']),
            shadow_price=json.dumps(output['shadow_price'], cls=NumpyJsonEncode),
            Tnm=json.dumps(output['Tnm']),
            # agent_operational_cost=json.dumps(output['agent_operational_cost']),
        )


def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[('grpc.max_send_message_length', -1), ('grpc.max_receive_message_length', -1)],
    )
    add_MarketModuleServicer_to_server(MarketModule(), server)

    server.add_insecure_port(f"{os.getenv('GRPC_HOST')}:{os.getenv('GRPC_PORT')}")
    print(f"Market module Listening at {os.getenv('GRPC_HOST')}:{os.getenv('GRPC_PORT')}")

    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
