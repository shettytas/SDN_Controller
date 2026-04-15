from mininet.topo import Topo

class StaticTopo(Topo):
    """
    Custom Mininet topology:
    h1 --- s1 --- s2 --- h2

    - Two hosts (h1, h2)
    - Two switches (s1, s2)
    - Linear topology for static routing
    """

    def build(self):
        # Add hosts with static IPs
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')

        # Add switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # Create links
        self.addLink(h1, s1)
        self.addLink(s1, s2)
        self.addLink(s2, h2)

# Register topology
topos = {'static': StaticTopo}