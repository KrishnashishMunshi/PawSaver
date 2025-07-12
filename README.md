# PawSaver
*VITB Healthhack 2025 project*

<img width="1915" height="925" alt="Image" src="https://github.com/user-attachments/assets/3237fba2-d84f-4e69-9795-774521dd81bc" />


## What it is

This is an IoT integrated animal health monitoring system for animal shelters, NGO's and wildlife conservation organizations.

<img width="1918" height="920" alt="Image" src="https://github.com/user-attachments/assets/dfa097d3-03cd-4163-be2e-7c904b50b633" />


## How it works

It uses a smart IoT device equipped with sensors to measure the **blood oxygen levels**, **pulse rate** and **GPS location** to gather data on each animal.

The data is sent as a JSON file to a flask API route and parsed for analysis and observation.

The gathered data is analyzed using preset in-built condition sets to determine the health status of the animal. In case of emergency an email alert is sent to the user notifying them about the particular animal in distress along with their current location.


## Features

1) Keep track of the health status of all your animals from a single place using the visual dashboard.
<img width="1919" height="933" alt="Image" src="https://github.com/user-attachments/assets/6fd56af6-c46a-4383-b9aa-7c0f4750e1cc" />





2) Monitor individual animal's health parameters using the easily understandable animal profile that visualizes their health parameters.

<img width="1914" height="914" alt="Image" src="https://github.com/user-attachments/assets/f37d4d7b-ab05-4d7a-b554-026cba449ff6" />




3) Receive e-mail updates in case of emergency.

<img width="1082" height="92" alt="Image" src="https://github.com/user-attachments/assets/daaf1b88-d8a4-42b4-aa31-4ff703013251" />




4) Keep track of all your animals' live location by referring to the relative map.

<img width="1506" height="821" alt="Image" src="https://github.com/user-attachments/assets/9c686327-31fd-41ce-a8f1-8b635bad70d1" />




5) Create different user accounts for different groups of animals/departments.

<img width="1916" height="930" alt="Image" src="https://github.com/user-attachments/assets/2055bc20-dde4-460d-92bb-3680f091ec76" />







## Impact

The lack of timely intervention is a huge cause of deaths in animals, and stray dogs in paticular. Dog shelters and wildlife sanctuaries could use this tool to quickly detect and be notified of any sings of distress and track the animal down accurately to give them the needed aid.

<img width="1919" height="918" alt="Image" src="https://github.com/user-attachments/assets/981d314c-66a8-462d-b17c-656e063e2e83" />

## Tech stack:

- Frotend: Javascript, TailwindCSS, HTML

- Backend: Flask (python), WebSockets.

- Email: Flask mail

- Database: SQLlite(Development), PostgreSQL(Aiven) (Production)

## Limitations:

- Lack of detailed health data (restricted to 2 sensors)

- Network delays between detection of anomaly and notification

- Uses a rule-based system for categorizing health status

- Requires wireless network connection for working properly

## Future improvements:

- Adding more sophisitciated health sensors for more accurate analysis

- Using ML models to classify animal health intelligently

- Minimize network delays by using local servers

- Create a LAN comaptible IoT connection

- Increase deployment scales 

