@echo off
echo Activating Python virtual environment...
call .\venv\Scripts\activate

echo Starting BeamNG...
cd .\beamng_gym
python -m envs.env
