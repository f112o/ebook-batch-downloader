KEY_WORDS=${1:-"数学"}
NUMBERS=${2:1}
SAVE_DIR=${3:-"./data"}

python pars.py --key_words "$KEY_WORDS" --numbers "$NUMBERS" --save_dir "$SAVE_DIR"