import os
from concurrent import futures

import dotenv
import grpc
import jsonpickle

from market.market_pb2 import MarketInput, MarketOutput
from market.market_pb2_grpc import MarketModuleServicer, add_MarketModuleServicer_to_server
from module.market_module.long_term.market_functions.run_longterm_market import run_longterm_market
from module.market_module.short_term.market_functions.run_shortterm_market import run_shortterm_market

dotenv.load_dotenv()


class MarketModule(MarketModuleServicer):

    def __init__(self) -> None:
        pass

    def RunLongTermMarket(self, request: MarketInput, context) -> MarketOutput:
        input_dict = jsonpickle.decode(request.input)
        return MarketOutput(
            Gn=jsonpickle.encode([], unpicklable=True)
        )
        # output = run_longterm_market(input_dict)
        # return MarketOutput(
        #     Gn=jsonpickle.encode(output['Gn'], unpicklable=True),
        #     Ln=jsonpickle.encode(output['Ln'], unpicklable=True),
        #     Pn=jsonpickle.encode(output['Pn'], unpicklable=True),
        #     QoE=jsonpickle.encode(output['QoE'], unpicklable=True),
        #     optimal=output['optimal'],
        #     plot_market_clearing=jsonpickle.encode(output['plot_market_clearing'], unpicklable=True),
        #     settlement=jsonpickle.encode(output['settlement'], unpicklable=True),
        #     social_welfare_h=jsonpickle.encode(output['social_welfare_h'], unpicklable=True),
        #     shadow_price=jsonpickle.encode(output['shadow_price'], unpicklable=True),
        #     Tnm=jsonpickle.encode(output['Tnm'], unpicklable=True),
        #     agent_operational_cost=jsonpickle.encode(output['agent_operational_cost'], unpicklable=True),
        # )

    def RunShortTermMarket(self, request: MarketInput, context) -> MarketOutput:
        input_dict = jsonpickle.decode(request.input)
        # output = run_shortterm_market(input_dict)
        # return MarketOutput(
        #     Gn=jsonpickle.encode(output['Gn'], unpicklable=True),
        #     Ln=jsonpickle.encode(output['Ln'], unpicklable=True),
        #     Pn=jsonpickle.encode(output['Pn'], unpicklable=True),
        #     QoE=jsonpickle.encode(output['QoE'], unpicklable=True),
        #     optimal=output['optimal'],
        #     plot_market_clearing=jsonpickle.encode(output['plot_market_clearing'], unpicklable=True),
        #     settlement=jsonpickle.encode(output['settlement'], unpicklable=True),
        #     social_welfare_h=jsonpickle.encode(output['social_welfare_h'], unpicklable=True),
        #     shadow_price=jsonpickle.encode(output['shadow_price'], unpicklable=True),
        #     Tnm=jsonpickle.encode(output['Tnm'], unpicklable=True),
        #     agent_operational_cost=jsonpickle.encode(output['agent_operational_cost'], unpicklable=True),
        # )
        return MarketOutput(
            Gn=jsonpickle.encode([], unpicklable=True)
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
