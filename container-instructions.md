# t5-Small Docker Container Setup

### To Ensure the Container can be ran using docker, download Docker Desktop for your specified PC Architecture:

https://www.docker.com/products/docker-desktop/

Ensure that you add the command `docker.exe` into the system path

## After downloading the container zipfile, build the container

### First move into the container directory with the command

```bash
cd ./container
```

### To build the container run the command below (Docker Desktop must be running)

```bash
docker build -t t5-onnx-summarizer .
```

## Running the Container

### After the container is built, you can run the container and pass any text as an argument, for exmample

```bash
docker run --rm t5-onnx-summarizer "The RAVEN system is an internally developed battery management platform designed to monitor and optimize the performance of distributed on-site devices. It provides continuous measurement of cell voltage, temperature, and discharge rates across all units, using a lightweight telemetry protocol that minimizes bandwidth consumption. RAVEN also includes a predictive module that estimates remaining useful life based on historical load patterns and environmental conditions. The system is deployed on our local network to ensure full control over operational data and to comply with internal security requirements. During routine operation, RAVEN identifies abnormal conditions such as rapid temperature rise, irregular voltage drift, or significant mismatch in pack balancing. When a threshold is exceeded, the system automatically triggers a notification to the maintenance dashboard and logs diagnostic details for later inspection. The diagnostic log includes recent telemetry windows, expected operating constraints, and a ranked list of probable root causes. These automated assessments help technicians prioritize field checks and reduce downtime across the device fleet. RAVEN also supports coordinated charging schedules to prevent power spikes and extend battery longevity. The scheduler evaluates current charge levels, predicted device usage, and grid load forecasts before assigning charging windows to each unit. In addition, RAVEN periodically performs firmware consistency checks to verify that all battery controllers are running the correct version of our embedded software. Any mismatch results in an automatic quarantine of the affected device until verification is complete. This ensures reliable operation and reduces the risk of system-wide failures."
```

### Or more generically

```bash
dokcer run --rm t5-onnx-summarizer <"Your detailed text">
```
