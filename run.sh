#!/bin/bash

cd "${0%/*}" || exit 1



# set the default Docker image tag to dactyl-keyboard
IMAGE_TAG="dactyl-keyboard"

# by default, don't rebuild the image
REBUILD=false;

# leave config empty to use default values
CONFIG=""


# check for command line flags
while test $# -gt 0; do
  case "$1" in
    -r|--rebuild)
      REBUILD=true
      shift
      ;;
    -t|--tag)
      if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
        IMAGE_TAG=$2
        shift 2
      else
        echo "Error: Argument for $1 is missing" >&2
        exit 1
      fi
      ;;
    -c|--config)
      CONFIG=$2
      shift 2
      ;;
    -*|--*)
      echo "Error: Unknown flag $1" >&2
      exit 1
      ;;
    *)
      COMMAND=$1
      shift;
      ;;
  esac
done



case $COMMAND in
  help)
    echo "Dactyl-Manuform Keyboard Generator"
    echo ""
    echo "Use this tool to configure and generate files for building a keyboard. All"
    echo "commands will be run in a Docker contianer, which will be built if it does"
    echo "not already exist."
    echo ""
    echo ""
    echo "Usage:"
    echo "  run [-r] [-i <docker-image-tag>] [-c <configuration-name>] <command>"
    echo ""
    echo "Available Commands:"
    echo "  help        Show this help"
    echo "  build       Rebuild the docker image"
    echo "  release     Run model_builder.py"
    echo "  generate    Output the keyboard files to the './things' directory"
    echo "  configure   Generate a configuration file with default values. The config"
    echo "              file will be saved to configs/<configuration-name>.json. If the"
    echo "              -c flag is not set, the defailt config_name will be used."
    echo ""
    echo "Flags:"
    echo "  -c    Set the configuration file to use. This should be the name of the file"
    echo "        only, without a file extension, and it is relative to the './configs'"
    echo "        directory. For example, '-c my-custom-dm' will refer to a file located"
    echo "        at './configs/my-custom-dm.json'"
    echo "  -r    Rebuild the docker image"
    echo "  -t    The tag that should be applied to the docker image"
    exit 0
    ;;
  build)
    docker build -t ${IMAGE_TAG} -f docker/Dockerfile .
    exit 0
    ;;
  generate)
    SCRIPT=dactyl_manuform.py
    ;;
  configure)
    SCRIPT=generate_configuration.py
    ;;
  release)
    SCRIPT=model_builder.py
    ;;
  *)
    echo "Invalid command. Try 'run help'"
    exit 1
esac


# get the image ID, and save the return code so we'll know if the image exists
IMAGE_ID=$(docker inspect --type=image --format={{.Id}} ${IMAGE_TAG})
INSPECT_RETURN_CODE=$?

# if we were specifically told to rebuild, or if the image doesn't exists, then build the docker image
if $REBUILD || [ $INSPECT_RETURN_CODE -ne 0 ]; then
    docker build -t ${IMAGE_TAG} -f docker/Dockerfile .
fi


# if a config file was specified, set the command line argument for the python script
if [[ ! -z $CONFIG ]]; then
  CONFIG_OPTION="--config=${CONFIG}"
fi

# run the command in a temporary container
docker run --name dm-run -d --rm -v "`pwd`/src:/app/src" -v "`pwd`/things:/app/things" -v "`pwd`/configs:/app/configs" ${IMAGE_TAG} python3 $SCRIPT $CONFIG_OPTION > /dev/null 2>&1

# show progress indicator while until dm-run container completes
while $(docker inspect --format={{.Id}} dm-run > /dev/null 2>&1); do
    echo -n "."
    sleep 1.5
done

echo ""
echo "Dactyl-Manuform '${COMMAND}' is complete!"
echo ""