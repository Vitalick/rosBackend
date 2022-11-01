import asyncio

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from ws_manager import ConnectionManager


class MinimalSubscriber(Node):

    def __init__(self, manager: ConnectionManager):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.ws_manager = manager
        # self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        asyncio.create_task(self.ws_manager.broadcast(f"Message from ros: {msg.data}"))


async def ros_listen(manager: ConnectionManager):
    rclpy.init()

    while True:
        minimal_subscriber = MinimalSubscriber(manager)
        try:
            while rclpy.ok():
                rclpy.spin_once(minimal_subscriber, timeout_sec=0.01)
                await asyncio.sleep(0.01)
        except Exception as e:
            print(e)
            minimal_subscriber.destroy_node()
        await asyncio.sleep(1)
    # Get response

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    rclpy.shutdown()
