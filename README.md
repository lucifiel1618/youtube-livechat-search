# Youtube LiveChat Query

## Description
A simple special-purpose command line tool for searching and data visualizing keywords appearing in youtube live chat.

## Requirements
* python >= 3.7
* pytchat
* coloredlogs
* data visualization: numpy, matplotlib (optional)

## Usage
```sh
usage: youtube-live-chat-query [-h] [--ignore-case] [--occurance OCCURANCE] [--hide-url] [--show-graph]
                            [--debug-level {DEBUG,INFO,ERROR,CRITICAL}]
                            id pattern [pattern ...]

Youtube Live Chat Search

positional arguments:
  id                    Video ID
  pattern               Search pattern

options:
  -h, --help            show this help message and exit
  --ignore-case, -I     Perform case-insensitive matching. (default: False)
  --occurance OCCURANCE, -O OCCURANCE
                        String occurance. (default: 0)
  --hide-url, -U        Hide url (default: False)
  --show-graph, -G      Show statistical graph (default: False)
  --debug-level {DEBUG,INFO,ERROR,CRITICAL}, -L {DEBUG,INFO,ERROR,CRITICAL}
                        debug level (default: DEBUG)
```