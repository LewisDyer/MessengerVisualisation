# MessengerVisualisation
Building a system to visualise data from Facebook Messenger.

## Project aims

For many people, Facebook messages represent a significant portion of online communication, especially with Messenger's support for large groups. But the linear structure of chats can make it difficult to track information about a chat as a whole - for instance, the most frequent commenters, or people who frequently engage with each other within the chat. My aim is to make it easier to visualise this sort of information, share it with friends, and potentially better understand the social dynamics of large groups.

## Obtaining data

You can obtain information from any Messenger chats you're part of, directly from Facebook:

* While logged into your Facebook account, head to the top right, click the little arrow, and click 'Settings'.
* Click 'Your Facebook information' on the lest sidebar, and then 'Download your information' in the middle menu.
* You'll see a list of pieces of information you can receive. If you just want messages, click 'Deselect all', then check 'Messages'.
* In the series of dropdown boxes, make sure you change format from HTML to JSON. You may also want to change media quality if you want to save space.
* It can take a few hours or days to receive a copy of your messages, and the file is quite large (about 6GB when compressed).

## Usage

1. Obtain your Facebook Messenger data, as above. Place it in the same directory as this README file (i.e there should be a folder called `messages` in this repo). You can change the name of the individual chat folders, but make sure you don't change the name of any other folders or files.
2. Install Pyviz, which is used to output the final graphs as an HTML file. Install it using `pip install pyviz`.
3. If you're not using Anaconda, you may also need to `pip install networkx`, which actually stores the underlying graphs. (All the other libraries should come standard with Python).

## Settings

Various settings are provided in `config.yaml` to change, which are described here:

`directed` - if this is `yes`, a directed graph will be given. Otherwise an undirected graph is produced.

`pair_threshold` - an edge between two people will only appear in the graph if the number of reacts between them is *above* this value. Setting this number very low can lead to very large, messy graphs for large group chats.

`react_category` - when outputting the graph, only reaction types that are included in this category will be considered. React categories are described in `react-info.json`, and can be modified or added to accordingly (for instance, setting `react_category: love` will combined heart eyes and heart reacts, since these are now exclusive to desktop and mobile respectively).

`base_size` - this sets the default size of all nodes, which may be adjusted if `adjust_node_size` is enabled.

`adjust_node_size` - if enabled, this will adjust the size of nodes, on a logarithmic scale, such that people who've posted more messages in the chat are represented by larger nodes.


## Issues

If you're having any issues running the program, or want to suggest any new features/additions, feel free to stick in an issue. I'll mainly be working on this during the winter vacation (around mid-December to mid-January), though I may continue it on a more irregular basis if I end up enjoying it enough.

