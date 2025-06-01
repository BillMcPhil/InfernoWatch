# InfernoWatch

InfernoWatch is a full stack web app that was made for the GDSC Mac-a-thon at McMaster University. It consists of a Convolutional Neural Network that judges whether or not an area has been affected by wildfires based on satellite imagery. Users input location information on the front end and then satellite images are pulled from Google Maps and fed into the CNN to determine a percentage of area that has been burned.

# Inspiration
Inspired by recent wildfire disasters, including Jasper National Park and LA, we decided to build an app that could help with wildfire risk assessment as well as allowing anyone to find areas impacted by wildfire easily.

# What it does
InfernoWatch is a classification neural network that will take a satellite image of an area and determine if it has previously been affected by a wildfire. Users can enter their addresses in order determine whether or not a specific area near them was affected

# How we built it
We found a model and dataset online to use, and trained the model ourselves. We then created a web app using react for the frontend and flask for the backend, and utilized the google maps API in order to pull satellite images, run them through the AI and send the results to the frontend

For more info see the devpost here: https://devpost.com/software/infernowatch
![image](https://github.com/user-attachments/assets/179acb58-290d-4f5e-a9d0-398365faee08)

