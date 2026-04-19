from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3

class StaticRouting(app_manager.RyuApp):
    """
    Ryu Controller for Static Routing using OpenFlow 1.3

    - Installs static flow rules on switch connection
    - Ensures predefined path is always used
    - Logs packet-in events for debugging
    """

    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def add_flow(self, dp, priority, match, actions):
        """
        Function to install flow rules in switches
        """
        ofp = dp.ofproto
        parser = dp.ofproto_parser

        # Define instruction (apply actions)
        inst = [parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]

        # Create flow mod message
        mod = parser.OFPFlowMod(
            datapath=dp,
            priority=priority,
            match=match,
            instructions=inst
        )

        # Send flow rule to switch
        dp.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        """
        Triggered when switch connects to controller
        Installs static routing rules
        """
        dp = ev.msg.datapath
        parser = dp.ofproto_parser
        dpid = dp.id

        print(f"[INFO] Switch connected: {dpid}")

        # STATIC ROUTING RULES
        # Switch 1: Forward between ports 1 and 2
        if dpid == 1:
            # Firewall rule: Drop packets arriving on port 1 (blocks h1 → h2 traffic)
            self.add_flow(dp, 20,
                  parser.OFPMatch(in_port=1),[]) 
            self.add_flow(dp, 10,
                          parser.OFPMatch(in_port=1),
                          [parser.OFPActionOutput(2)])

            self.add_flow(dp, 10,
                          parser.OFPMatch(in_port=2),
                          [parser.OFPActionOutput(1)])

        # Switch 2: Same forwarding logic
        elif dpid == 2:
            self.add_flow(dp, 10,
                          parser.OFPMatch(in_port=1),
                          [parser.OFPActionOutput(2)])

            self.add_flow(dp, 10,
                          parser.OFPMatch(in_port=2),
                          [parser.OFPActionOutput(1)])

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        """
        Handles packet-in events (for grading requirement)
        """
        msg = ev.msg
        dp = msg.datapath
        in_port = msg.match['in_port']

        print(f"[PACKET_IN] Switch {dp.id} received packet on port {in_port}")
