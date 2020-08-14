#!/bin/sh

GPT=${GPT:-~/.gnome-pomodoro-tracking}
REPO=${REPO:-josehbez/gnome-pomodoro-tracking}
REMOTE=${REMOTE:-https://github.com/${REPO}.git}
BRANCH=${BRANCH:-master}

command_exists() {
	command -v "$@" >/dev/null 2>&1
}
error(){
    echo ${RED}"Error: $@"${RESET} >&2
}
setup_gpt(){
    echo "Cloning Gnome Pomodoro Tracking ..."
    git clone -c core.eol=lf -c core.autocrlf=false \
		-c fsck.zeroPaddedFilemode=ignore \
		-c fetch.fsck.zeroPaddedFilemode=ignore \
		-c receive.fsck.zeroPaddedFilemode=ignore \
        --depth=1 --branch "$BRANCH" "$REMOTE" "$GPT" || {
		error "git clone of gnome-pomodoro-tracking repo failed"
		exit 1
	}
}
setup_gpt_conf(){
    echo "Looking for an existing ~/.gp-tracking.conf..."
    if [ ! -f ~/.gp-tracking.conf ]; then
        echo "Copy $GPT/gp-tracking.template ~/.gp-tracking.conf"
        cp $GPT/gp-tracking.template ~/.gp-tracking.conf
        echo "ln $GPT/gp-tracking.py -s ~/.local/bin/gp-tracking"
        ln $GPT/gp-tracking.py -s ~/.local/bin/gp-tracking        
    else
        echo "Found ~/.gp-tracking.conf"
        return 
    fi
}

main(){    
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
    setup_gpt
    setup_gpt_conf

    cat <<-'EOF'

		GNOME POMODORO TRACKING ....is now installed!
		
		• Follow us on Twitter: https://twitter.com/josehbez
		• Get stickers, shirts, coffee mugs and other swag: https://github.com/josehbez/gnome-pomodoro-tracking
		• Don't forget to restart your terminal!
	EOF
    echo "Run gp-tracking to try it out."
} 

main "$@"