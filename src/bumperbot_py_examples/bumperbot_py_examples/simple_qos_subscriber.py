import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile,QoSReliabilityPolicy,QoSDurabilityPolicy
from std_msgs.msg import String

class SimpleQoSSubscriber(Node):
    def __init__(self):
        super().__init__('simpleQoSSubscriber')

        self.qos_profile_sub=QoSProfile(depth=10)

        self.declare_parameter("reliability","system_default")
        self.declare_parameter("durability","system_default")

        reliability = self.get_parameter("reliability").get_parameter_value().string_value
        durability = self.get_parameter("durability").get_parameter_value().string_value

        if reliability =="best_effort":
            self.qos_profile_sub.reliability = QoSReliabilityPolicy.BEST_EFFORT
            self.get_logger().info("[Reliablity]: Best Effort")
        elif reliability == "reliable":
            self.qos_profile_sub.reliability=QoSReliabilityPolicy.RELIABLE
            self.get_logger().info("[Reliablity]: Reliable")
        elif reliability =="system_default":
            self.qos_profile_sub.reliability=QoSReliabilityPolicy.SYSTEM_DEFAULT
            self.get_logger().info("[Reliablity]: system_Default")
        else:
            self.get_logger().error(f"Selected Reliability QOS {reliability} doesnt exist")
            return

        

        if durability =="volatile":
            self.qos_profile_sub.durability = QoSDurabilityPolicy.VOLATILE
            self.get_logger().info("[Durability]: volatile")
        elif durability=="system_default":
            self.qos_profile_sub.durability=QoSDurabilityPolicy.SYSTEM_DEFAULT
            self.get_logger().info("[Durability]: system_default")
        elif durability=="transient_local":
            self.qos_profile_sub.durability=QoSDurabilityPolicy.TRANSIENT_LOCAL
        else:
            self.get_logger().error(f"Selected Durability QOS {durability} doesnt exist")
            return

        self.sub_=self.create_subscription(String, 'chatter',self.msg_callback,self.qos_profile_sub)

    def msg_callback(self,msg):
        self.get_logger().info('I heard: %s' % msg.data)


def main():
    rclpy.init()
    simpleQoSSubscriber=SimpleQoSSubscriber()
    rclpy.spin(simpleQoSSubscriber)
    simpleQoSSubscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()