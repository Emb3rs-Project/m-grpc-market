if [ $# -eq 0 ]
  then
    echo "No arguments supplied, Need Path to python.file"
    exit
fi

PYTHONPATH=$PYTHONPATH:plibs python $1