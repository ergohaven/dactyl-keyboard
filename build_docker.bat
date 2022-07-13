docker build -t dactyl-keyboard -f docker/Dockerfile .
docker run --name DM-run -d -v "%cd%/:/app"  dactyl-keyboard python3 -i dactyl_manuform.py
docker run --name DM-config -d -v "%cd%/:/app"  dactyl-keyboard python3 -i generate_configuration.py
docker run --name DM-release-build -d -v "%cd%/:/app"  dactyl-keyboard python3 -i model_builder.py
docker run --name DM-shell -d -ti -v "%cd%/:/app"  dactyl-keyboard
