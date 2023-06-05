# yt_arknights_poll
A hopefully low latency arknights poll for youtube chat. I can't guarantee it will work since you need a running stream to test all functions. Poll logic
was tested with a basic udp socket setup so I can at least be confident in that.

# Running the Script
Running the script with no arguments (except for the video ID which is required) will give a poll with every operator available as an option. 
Use '-c' or '--choices' to provide a custom list of options for the poll. Responses in chat are filtered using '!vote' as a prefix. Responses
are also fuzzy matched to the poll options so typos shouldn't be much of an issue. A requirements file is provided to use with pip to make
sure all packages are available.
