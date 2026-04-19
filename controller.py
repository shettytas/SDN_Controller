from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ipv4


class StaticRouting(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    # Function to install flow rules
    def add_flow(self, dp, priority, match, actions):
        parser = dp.ofproto_parser
        ofp = dp.ofproto

        inst = [parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]

        mod = parser.OFPFlowMod(
            datapath=dp,
            priority=priority,
            match=match,
            instructions=inst
        )
        dp.send_msg(mod)

    # Runs when switch connects
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        dp = ev.msg.datapath
        parser = dp.ofproto_parser
        ofp = dp.ofproto

        print(f"Switch {dp.id} connected")

        # Send unknown packets to controller
        self.add_flow(dp, 0,
            parser.OFPMatch(),
            [parser.OFPActionOutput(ofp.OFPP_CONTROLLER)]
        )

        # Static forwarding rules
        if dp.id == 1:
            self.add_flow(dp, 10, parser.OFPMatch(in_port=1),
                          [parser.OFPActionOutput(2)])
            self.add_flow(dp, 10, parser.OFPMatch(in_port=2),
                          [parser.OFPActionOutput(1)])

        elif dp.id == 2:
            self.add_flow(dp, 10, parser.OFPMatch(in_port=1),
                          [parser.OFPActionOutput(2)])
            self.add_flow(dp, 10, parser.OFPMatch(in_port=2),
                          [parser.OFPActionOutput(1)])

    # Runs when packet comes to controller
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        dp = msg.datapath
        parser = dp.ofproto_parser
        ofp = dp.ofproto

        pkt = packet.Packet(msg.data)
        ip = pkt.get_protocol(ipv4.ipv4)

        if not ip:
            return

        src = ip.src
        dst = ip.dst

        print(f"{src} → {dst}")

        # Allow only h1 → h2
        if src == "10.0.0.1" and dst == "10.0.0.2":
            out_port = 2
        else:
            print("Blocked")
            return

        # Forward packet
        actions = [parser.OFPActionOutput(out_port)]

        out = parser.OFPPacketOut(
            datapath=dp,
            buffer_id=ofp.OFP_NO_BUFFER,
            in_port=msg.match['in_port'],
            actions=actions,
            data=msg.data
        )
        dp.send_msg(out)
