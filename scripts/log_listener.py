import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import Log
import chromadb
import os

class CopilotListener(Node):
    def __init__(self):
        super().__init__('copilot_listener')
        
        # 1. Connect to your existing ChromaDB using a relative path
        # Finds the folder where this script lives, then goes up one level to 'data'
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, "..", "data", "chroma_db")
        
        self.client = chromadb.PersistentClient(path=db_path)

        self.collection = self.client.get_collection(name="robot_failures")
        
        # 2. Subscribe to the system-wide log topic (/rosout)
        self.subscription = self.create_subscription(
            Log,
            '/rosout',
            self.listener_callback,
            10)
        
        self.get_logger().info('🚀 Copilot Listener is active and watching ROS 2 logs...')

    def listener_callback(self, msg):
        # Ignore logs coming from this node to prevent infinite loops
        if msg.name == 'copilot_listener':
            return
        # We only care about Warnings (3) and Errors (4)
        if msg.level >= 3:
            error_msg = msg.msg
            node_name = msg.name
            
            self.get_logger().warn(f"Detected Issue in {node_name}: {error_msg}")
            
            # 3. Search the Database automatically
            results = self.collection.query(
                query_texts=[error_msg],
                n_results=1
            )
            
            best_fix = results['metadatas'][0][0]['fix']
            
            print("\n" + "="*40)
            print(f"COPILOT AUTO-DIAGNOSIS FOR: {node_name}")
            print(f"Proposed Fix: {best_fix}")
            print("="*40 + "\n")

def main(args=None):
    rclpy.init(args=args)
    node = CopilotListener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
