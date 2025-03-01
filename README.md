# BeamNG Gym

## Overview  

This project provides a custom reinforcement learning (RL) environment built on **BeamNG.tech**, a high-fidelity vehicle simulation platform. By leveraging **BeamNGpy**, the official Python API, it enables interaction with simulated vehicles, allowing the collection of sensor data such as **cameras, LiDAR, and vehicle states** while applying control actions.  

This environment adheres to the **Gymnasium API** standard, making it compatible with various RL frameworks. Researchers and developers can utilize it for **training autonomous driving models, evaluating reinforcement learning algorithms, and simulating real-world driving scenarios**.

## Usage
### 1. Setup BeamNG.tech  
BeamNG has two main versions:  

- **BeamNG.drive**: A consumer driving simulator for free driving and vehicle physics.  
- **BeamNG.tech**: A research and development version.  

To access sensor data (**e.g., cameras, LiDAR, vehicle states**) and interact with the simulation programmatically, **BeamNG.tech is required**.  

A valid license is required to use BeamNG.tech.  

For licensing details, please visit the official [BeamNG.tech website](https://www.beamng.tech) and scroll down to the **Licensing Inquiry** section at the bottom of the page.

### 2. Install beamng_gym  

Clone this repository and install it using pip:  

```sh
git clone https://github.com/peregrine-884/beamng-gym.git
cd beamng_gym
pip install -e .
```  

This will install `beamng_gym` in **editable mode**, allowing you to modify the code and see changes without reinstalling.  

### 3. Launch BeamNG.tech  

Before running the reinforcement learning environment, start BeamNG.tech with the following command:  

```sh
cd <path-to-beamng.tech-directory>  
Bin64\BeamNG.tech.x64.exe -console -nosteam -tcom-listen-ip "127.0.0.1" -lua "extensions.load('tech/techCore');tech_techCore.openServer(64256)"  
```  

This command launches BeamNG.tech and enables communication with the Python API.  

### 4. Start the Reinforcement Learning Environment  

Once BeamNG.tech is running, you can start the custom reinforcement learning environment:  

```python
import gymnasium as gym
import beamng_gym

env = gym.make('BeamNG-v0')
```  

Now the environment is ready for interaction, and you can use it for reinforcement learning experiments.
