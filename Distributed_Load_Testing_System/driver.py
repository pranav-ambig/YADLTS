import requests
from multiprocessing import Process

url = 'http://localhost:5052'

def bombard():
    while True:
        try:
            response = requests.get('http://localhost:5052') 
        except requests.exceptions.ConnectionError:
            print("Server crashed")
            return


num_drivers = 10
driver_procs = []

if __name__ == "__main__":
    for _ in range(num_drivers):
        driver_proc = Process(target=bombard)

        driver_procs.append(driver_proc)
        driver_proc.start()

    for driver_proc in driver_procs:
        driver_proc.join()
