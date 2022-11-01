import asyncio

import rclpy
from rclpy.node import Node

from tutorial_interfaces.msg import Num

from ws_manager import ConnectionManager


class MinimalSubscriber(Node):

    def __init__(self, manager: ConnectionManager):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            Num,
            'topic',
            self.listener_callback,
            10)
        self.ws_manager = manager
        # self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        asyncio.create_task(self.ws_manager.broadcast(f"Message from ros: {msg}"))


async def ros_listen(manager: ConnectionManager):
    rclpy.init()

    minimal_subscriber = MinimalSubscriber(manager)

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()
