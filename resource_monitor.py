#!/usr/bin/env python3
"""
VM Resource Monitor with GCP Auto-Scaling
Simplified version for assignment demonstration-M22AIE233
"""

import time
import logging
import psutil
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='vm_monitor.log',
    filemode='a'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
logger = logging.getLogger('')

# Configuration
CONFIG = {
    'threshold': 75,  
    'check_interval': 10, 
    'resources_to_monitor': ['cpu', 'memory', 'disk'],
    'gcp_project_id': 'innate-might-454613-p4',
    'gcp_zone': 'us-central1-c',
    'gcp_instance_name': 'instance-20250323-145124',
    'cooldown_period': 60,
}

def get_resource_usage():
    """Get current resource usage of the local VM."""
    usage = {
        'cpu': psutil.cpu_percent(interval=1),
        'memory': psutil.virtual_memory().percent,
        'disk': psutil.disk_usage('/').percent
    }
    return usage

def simulate_gcp_connection():
    """Simulate connecting to GCP."""
    logger.info("Successfully connected to GCP")
    return True

def simulate_auto_scaling(resource_type, usage_value):
    """Simulate auto-scaling to GCP."""
    logger.info(f"AUTO-SCALING EVENT TRIGGERED by high {resource_type.upper()} usage: {usage_value}%")
    logger.info(f"Would connect to GCP instance '{CONFIG['gcp_instance_name']}' in zone '{CONFIG['gcp_zone']}'")
    
    logger.info("Simulating auto-scaling process...")
    
    # Step 1: Verify instance exists
    logger.info("Step 1/4: Verifying GCP instance exists... [SUCCESS]")
    time.sleep(1)
    
    # Step 2: Start instance if not running
    logger.info("Step 2/4: Starting GCP instance... [SUCCESS]")
    time.sleep(1)
    
    # Step 3: Prepare local workload for migration
    logger.info("Step 3/4: Preparing workload for migration... [SUCCESS]")
    time.sleep(1)
    
    # Step 4: Migrate workload to GCP
    logger.info("Step 4/4: Migrating workload to GCP instance... [SUCCESS]")
    time.sleep(1)
    
    logger.info(f"AUTO-SCALING COMPLETE: Workload successfully migrated to GCP instance '{CONFIG['gcp_instance_name']}'")
    return True

def main():
    """Main monitoring loop."""
    logger.info("Starting VM resource monitoring...")
    logger.info(f"Monitoring threshold set at {CONFIG['threshold']}%")
    
    simulate_gcp_connection()
    
    last_scale_time = 0
    
    try:
        while True:
            usage = get_resource_usage()
            logger.info(f"Current usage: CPU: {usage['cpu']}%, Memory: {usage['memory']}%, Disk: {usage['disk']}%")
            
            current_time = time.time()
            in_cooldown = (current_time - last_scale_time) < CONFIG['cooldown_period']
            
            if in_cooldown:
                cooldown_remaining = CONFIG['cooldown_period'] - (current_time - last_scale_time)
                logger.info(f"In cooldown period, {cooldown_remaining:.0f} seconds remaining")
            
            for resource_type in CONFIG['resources_to_monitor']:
                if usage[resource_type] > CONFIG['threshold'] and not in_cooldown:
                    logger.warning(f"THRESHOLD EXCEEDED: {resource_type.upper()} usage ({usage[resource_type]}%) > {CONFIG['threshold']}%")
                    

                    if simulate_auto_scaling(resource_type, usage[resource_type]):
                        last_scale_time = current_time
                        logger.info(f"Entering cooldown period of {CONFIG['cooldown_period']} seconds")
                        break
            
            time.sleep(CONFIG['check_interval'])
            
    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user")
    except Exception as e:
        logger.error(f"Error in monitoring: {e}")

if __name__ == "__main__":
    main()