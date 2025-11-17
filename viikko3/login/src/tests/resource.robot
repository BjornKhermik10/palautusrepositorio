*** Settings ***
Library    SeleniumLibrary
Library    ../AppLibrary.py

*** Variables ***
${SERVER}      localhost:5001
${HOME_URL}    http://${SERVER}
${LOGIN_URL}   http://${SERVER}/login
${REGISTER_URL} http://${SERVER}/register
${BROWSER}     chrome
${HEADLESS}    false

*** Keywords ***
Open And Configure Browser
    Open Browser    ${HOME_URL}    ${BROWSER}
