#!/usr/bin/env python3
"""
Load Generator Script
Generates system load to test auto-scaling functionality-M22aie233
"""

import time
import argparse
import threading
import multiprocessing

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Generate system load for testing')
    parser.add_argument('--type', choices=['cpu', 'memory', 'all'], default='cpu',
                      help='Type of load to generate (cpu, memory, or all)')
    parser.add_argument('--duration', type=int, default=60,
                      help='Duration in seconds to generate load')
    parser.add_argument('--intensity', type=int, default=90,
                      help='Load intensity percentage (1-100)')
    
    return parser.parse_args()

def generate_cpu_load(intensity, duration):
    """Generate CPU load."""
    print(f"Generating CPU load at {intensity}% intensity for {duration} seconds...")
    
    num_cores = multiprocessing.cpu_count()
    cores_to_use = max(1, int(num_cores * intensity / 100))
    
  
    def cpu_load():
        end_time = time.time() + duration
        while time.time() < end_time:
            for i in range(10000000):
                _ = i * i
    
    threads = []
    for _ in range(cores_to_use):
        thread = threading.Thread(target=cpu_load)
        thread.daemon = True
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print("CPU load generation completed")

def generate_memory_load(intensity, duration):
    """Generate memory load."""
    print(f"Generating memory load at {intensity}% intensity for {duration} seconds...")
    

    total_mem = psutil.virtual_memory().total
    
    mem_to_allocate = int(total_mem * intensity / 100)
    
    chunk_size = 10 * 1024 * 1024  
    allocated_memory = []
    
    try:
        end_time = time.time() + duration
        total_allocated = 0
        
        while time.time() < end_time and total_allocated < mem_to_allocate:
            #Allocate memory chunk
            current_chunk = bytearray(min(chunk_size, mem_to_allocate - total_allocated))
            allocated_memory.append(current_chunk)
            total_allocated += len(current_chunk)
            
            for i in range(0, len(current_chunk), 4096):
                current_chunk[i] = 1
            
            print(f"Allocated {total_allocated / (1024*1024):.2f} MB of {mem_to_allocate / (1024*1024):.2f} MB")
            time.sleep(0.5)
        
        print(f"Memory allocated. Holding for remainder of duration...")
        remaining_time = end_time - time.time()
        if remaining_time > 0:
            time.sleep(remaining_time)
    
    finally:
        #Free memory by removing references to the allocated memory
        print("Releasing allocated memory...")
        allocated_memory.clear()
    
    print("Memory load generation completed")

def main():
    """Main function to generate system load."""
    args = parse_arguments()
    
    print(f"Starting load generator with {args.type} load at {args.intensity}% intensity for {args.duration} seconds")
    
    try:
        global psutil
        import psutil
        
        if args.type == 'cpu' or args.type == 'all':
            generate_cpu_load(args.intensity, args.duration)
        
        if args.type == 'memory' or args.type == 'all':
            generate_memory_load(args.intensity, args.duration)
        
        print("Load generation completed")
        
    except KeyboardInterrupt:
        print("Load generation stopped by user")
    except Exception as e:
        print(f"Error generating load: {e}")

if __name__ == "__main__":
    main()