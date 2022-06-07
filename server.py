import os
from concurrent import futures

import dotenv
import grpc
import jsonpickle
import json

from market.market_pb2 import LongTermMarketResponse, MarketInput, MarketInputRequest, ShortTermMarketResponse
from market.market_pb2_grpc import MarketModuleServicer, add_MarketModuleServicer_to_server

from module.market_module.long_term.market_functions.run_longterm_market import run_longterm_market
from module.market_module.long_term.market_functions.convert_user_and_module_inputs import convert_user_and_module_inputs as long_convert

from module.market_module.short_term.market_functions.run_shortterm_market import run_shortterm_market
from module.market_module.short_term.market_functions.convert_user_and_module_inputs import convert_user_and_module_inputs as short_convert
dotenv.load_dotenv()


class MarketModule(MarketModuleServicer):

    def __init__(self) -> None:
        pass

    def RunLongTermMarket(self, request: MarketInputRequest, context) -> LongTermMarketResponse:
        in_var = {
            "platform": jsonpickle.decode(request.platform),
            "gis-module": jsonpickle.decode(request.gis_module),
            "cf-module" : jsonpickle.decode(request.cf_module),
            "teo-module" : jsonpickle.decode(request.teo_module)
        }
        
        input_dict = long_convert(in_var)
        output = run_longterm_market(input_dict=input_dict)

        return LongTermMarketResponse(
            Gn=json.dumps(output['Gn']),
            Ln=json.dumps(output['Ln']),
            Pn=json.dumps(output['Pn']),
            QoE=json.dumps(output['QoE']),
            optimal=str(output['optimal']),
            plot_market_clearing=json.dumps(output['plot_market_clearing']),
            settlement=json.dumps(output['settlement']),
            social_welfare_h=json.dumps(output['social_welfare_h']),
            shadow_price=json.dumps(output['shadow_price']),
            Tnm=json.dumps(output['Tnm']),
            agent_operational_cost=json.dumps(output['agent_operational_cost']),
            SPM=json.dumps(output['SPM']),
            ADG=json.dumps(output['ADG']),
        )
    
    def RunLongTermMarketDirect(self, request: MarketInput, context) -> LongTermMarketResponse:
        
        input_dict = jsonpickle.decode(request.input)
        output = run_longterm_market(input_dict=input_dict)

        return LongTermMarketResponse(
            Gn=json.dumps(output['Gn']),
            Ln=json.dumps(output['Ln']),
            Pn=json.dumps(output['Pn']),
            QoE=json.dumps(output['QoE']),
            optimal=str(output['optimal']),
            plot_market_clearing=json.dumps(output['plot_market_clearing']),
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
            "cf-module" : jsonpickle.decode(request.cf_module),
            "teo-module" : jsonpickle.decode(request.teo_module)
        }
        
        input_dict = short_convert(in_var)
        output = run_shortterm_market(input_dict)
        
        return ShortTermMarketResponse(
            Gn=json.dumps(output['Gn']),
            Ln=json.dumps(output['Ln']),
            Pn=json.dumps(output['Pn']),
            QoE=json.dumps(output['QoE']),
            optimal=str(output['optimal']),
            plot_market_clearing=json.dumps(output['plot_market_clearing']),
            settlement=json.dumps(output['settlement']),
            social_welfare_h=json.dumps(output['social_welfare_h']),
            shadow_price=json.dumps(output['shadow_price']),
            Tnm=json.dumps(output['Tnm']),
            agent_operational_cost=json.dumps(output['agent_operational_cost']),
        )

    def RunShortTermMarketDirect(self, request: MarketInput, context) -> ShortTermMarketResponse:
        
        input_dict = jsonpickle.decode(request.input)
        output = run_shortterm_market(input_dict)
        
        return ShortTermMarketResponse(
            Gn=json.dumps(output['Gn']),
            Ln=json.dumps(output['Ln']),
            Pn=json.dumps(output['Pn']),
            QoE=json.dumps(output['QoE']),
            optimal=str(output['optimal']),
            plot_market_clearing=json.dumps(output['plot_market_clearing']),
            settlement=json.dumps(output['settlement']),
            social_welfare_h=json.dumps(output['social_welfare_h']),
            shadow_price=json.dumps(output['shadow_price']),
            Tnm=json.dumps(output['Tnm']),
            agent_operational_cost=json.dumps(output['agent_operational_cost']),
        )

    


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_MarketModuleServicer_to_server(MarketModule(), server)

    server.add_insecure_port(f"{os.getenv('GRPC_HOST')}:{os.getenv('GRPC_PORT')}")

    print(f"Market module Listening at {os.getenv('GRPC_HOST')}:{os.getenv('GRPC_PORT')}")

    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
