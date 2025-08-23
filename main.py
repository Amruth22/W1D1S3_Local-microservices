import multiprocessing
import uvicorn
import time
import sys

def run_service1():
    """Run Service 1 (Student Personal Information Service) on port 8080"""
    from service1 import app as app1
    uvicorn.run(app1, host="0.0.0.0", port=8080)

def run_service2():
    """Run Service 2 (Student Academic Information Service) on port 8081"""
    from service2 import app as app2
    uvicorn.run(app2, host="0.0.0.0", port=8081)

if __name__ == "__main__":
    print("Starting both microservices...")
    print("Service 1 (Personal Info): http://localhost:8080")
    print("Service 2 (Academic Info): http://localhost:8081")
    print("Press Ctrl+C to stop all services")
    
    # Create processes for each service
    service1_process = multiprocessing.Process(target=run_service1)
    service2_process = multiprocessing.Process(target=run_service2)
    
    try:
        # Start both services
        service1_process.start()
        time.sleep(1)  # Small delay to ensure service1 starts first
        service2_process.start()
        
        # Wait for both processes to complete
        service1_process.join()
        service2_process.join()
        
    except KeyboardInterrupt:
        print("\nShutting down services...")
        service1_process.terminate()
        service2_process.terminate()
        service1_process.join()
        service2_process.join()
        print("All services stopped.")
        sys.exit(0)