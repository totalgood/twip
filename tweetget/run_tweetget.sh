#!/bin/bash
# var for session name (to avoid repeated occurences)
sn=tweetgetter

# Start the session and window 0 in /etc
#   This will also be the default cwd for new windows created
#   via a binding unless overridden with default-path.
cd ~/src/twip
tmux new-session -s "$sn" -n etc -d

names=("python" "#sarcasm" "#happy" "#sad" "#joy" "#angry" "#lucky" "#sadness" "#namaste" "#frustrated")
# Create a bunch of windows
for i in "${names[@]}"; do
    if [ -f "data/oldest_id.txt${i}" ]; then
        cp -f data/oldest_id.txt"$i" data/"$i"--oldest_id.txt
    fi
done

for i in "${names[@]}"; do
    tmux new-window -t "$sn:$i" -n "$i" 'bash -i -c "python -m tweetget.cron ${i}"'
done

# Set the default cwd for new windows (optional, otherwise defaults to session cwd)
#tmux set-option default-path /

# Select window #1 and attach to the session
tmux select-window -t "$sn:1"
tmux -2 attach-session -t "$sn"