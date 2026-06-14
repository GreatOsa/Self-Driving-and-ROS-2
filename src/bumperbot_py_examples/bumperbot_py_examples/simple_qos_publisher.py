import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile,QoSReliabilityPolicy,QoSDurabilityPolicy
from std_msgs.msg import String


class SimpleQoSPublisher(Node):
    def __init__ (self):
        super().__init__('simple_qos_publisher')

        self.qos_profile_pub=QoSProfile(depth=10)

        self.declare_parameter("reliability","system_default")
        self.declare_parameter("durability","system_default")

        reliability = self.get_parameter("reliability").get_parameter_value().string_value
        durability = self.get_parameter("durability").get_parameter_value().string_value

        if reliability =="best_effort":
            self.qos_profile_pub.reliability = QoSReliabilityPolicy.BEST_EFFORT
            self.get_logger().info("[Reliablity]: Best Effort")
        elif reliability == "reliable":
            self.qos_profile_pub.reliability=QoSReliabilityPolicy.RELIABLE
            self.get_logger().info("[Reliablity]: Reliable")
        elif reliability =="system_default":
            self.qos_profile_pub.reliability=QoSReliabilityPolicy.SYSTEM_DEFAULT
            self.get_logger().info("[Reliablity]: system_Default")
        else:
            self.get_logger().error(f"Selected Reliability QOS {reliability} doesnt exist")
            return

        

        if durability =="volatile":
            self.qos_profile_pub.durability = QoSDurabilityPolicy.VOLATILE
            self.get_logger().info("[Durability]: volatile")
        elif durability=="system_default":
            self.qos_profile_pub.durability=QoSDurabilityPolicy.SYSTEM_DEFAULT
            self.get_logger().info("[Durability]: system_default")
        elif durability=="transient_local":
            self.qos_profile_pub.durability=QoSDurabilityPolicy.TRANSIENT_LOCAL
        else:
            self.get_logger().error(f"Selected Durability QOS {durability} doesnt exist")
            return


        self.pub_=self.create_publisher(String, 'chatter',self.qos_profile_pub)

        self.counter=0
        self.frequency=1.0

        self.get_logger().info('Publishing at %d Hz' % self.frequency)
        self.timer= self.create_timer(self.frequency, self.timer_callback)

    def timer_callback(self):
        msg=String()
        msg.data=f'Osayande the Great - counter: {self.counter}'
        self.pub_.publish(msg)
        self.counter+=1


def main():
    rclpy.init()
    simple_qos_publisher=SimpleQoSPublisher()
    rclpy.spin(simple_qos_publisher)
    simple_qos_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
