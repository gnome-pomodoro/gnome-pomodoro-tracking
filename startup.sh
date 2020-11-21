#!/bin/sh

GPT_DIR=${GPT_DIR:-$HOME/.gp-tracking}
REMOTE=${REMOTE:-https://github.com/josehbez/gp-tracking.git}
GPT_CONF="$HOME/.gp-tracking.conf"
GPT_BIN="$HOME/.local/bin/gp-tracking"

command_exists() {
	command -v "$@" >/dev/null 2>&1
}

error(){
    echo ${RED}"Error: $@"${RESET} >&2
}


gpt_install(){
    echo "Start process instalation ... $GPT_DIR"
    echo "Cloning gp-tracking branch:$1"
    if [ ! -d $GPT_DIR ]; then
        mkdir $GPT_DIR
    fi 
    git clone -c core.eol=lf -c core.autocrlf=false \
		-c fsck.zeroPaddedFilemode=ignore \
		-c fetch.fsck.zeroPaddedFilemode=ignore \
		-c receive.fsck.zeroPaddedFilemode=ignore \
        --depth=1 --branch "$1" "$REMOTE" "$GPT_DIR" || {
		error "git clone of gp-tracking repo failed"
		exit 1
	}
    echo "Looking for an existing ... $GPT_CONF"
    if [ ! -f $GPT_CONF ]; then
        echo "Copy $GPT_DIR/gp-tracking.template $GPT_CONF"
        cp $GPT_DIR/gp-tracking.template $GPT_CONF
        echo "ln $GPT_DIR/gp-tracking.py -s $GPT_BIN"
        ln $GPT_DIR/gp-tracking.py -s $GPT_BIN
    else
        echo "Found $GPT_CONF"
        return 
    fi

    echo ""
    echo "• Follow us on Twitter: https://twitter.com/josehbez"
    echo "• Now is installed, try gp-tracking -h"
    echo "• Don't forget to restart your terminal!''"
}

gpt_upgrade(){
    echo "Start process upgrading ... $GPT_DIR"
    currentdir=$(pwd)
    cd $GPT_DIR
    #printf "Updating Gnome Pomodoro Tracking"
    if git pull --rebase --stat origin $1; then
        echo  ""
        printf "• Has been upgrade at the current version."
    else
        printf 'There was an error updating. Try again later'
    fi
    cd $currentdir
}
gpt_uninstall(){
    echo "Start process uninstall  ... $GPT_DIR"
    read -r -p "Are you sure you want to remove Oh GNOME POMODORO TRACKING? [y/N] " confirmation
    if [ "$confirmation" != y ] && [ "$confirmation" != Y ]; then
        echo "Uninstall cancelled"
        exit
    fi
    if [ -e $GPT_CONF ]; then    
        echo "Removing config: $GPT_CONF ..."
        rm $GPT_CONF
    fi
    if [ -f $GPT_BIN ]; then
        echo "Removing bin: $GPT_BIN ..."
        rm -rf $GPT_BIN
    fi
    if [ -d $GPT_DIR ]; then
        echo "Removing dir: $GPT_DIR ..."
        rm -rf $GPT_DIR
    fi
    echo ""
    echo "• Thanks for trying out gp-tracking. It's been uninstalled."
    echo "• Don't forget to restart your terminal!"

}

main(){      

    echo "Wizard startup gp-tracking\n"

    if ! command_exists git; then
        error "git is not installed. Please install git."
        exit 
    fi
    if ! command_exists python3; then
        error "python3 is not installed. Please install python3."
        exit 
    fi
    if ! command_exists gnome-pomodoro; then
        error "gnome-pomodoro is not installed. Please install gnome-pomodoro."
        exit 
    fi
    action=$1
    
    if [ -z "$2" ]; then 
        branch=master
    else
        branch=$2
    fi 
    
    if [ $action = "--install"  ]; then 
        gpt_install $branch
    elif [ $action = "--upgrade" ]; then 
        gpt_upgrade $branch
    elif [ $action = "--uninstall" ]; then
        gpt_uninstall
    fi
} 

main "$@"