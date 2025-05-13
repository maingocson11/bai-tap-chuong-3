*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}             https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
${BROWSER}         chrome
${VALID_USER}      Admin
${VALID_PASSWORD}  admin123
${INVALID_USER}    wronguser
${INVALID_PASSWORD} wrongpass

*** Test Cases ***
Login With Valid Credentials
    Open Browser    ${URL}    ${BROWSER}
    Input Text    xpath://input[@name="username"]    ${VALID_USER}
    Input Text    xpath://input[@name="password"]    ${VALID_PASSWORD}
    Click Button    xpath://button[@type="submit"]
    Wait Until Page Contains Element    xpath://h6[text()="Dashboard"]    timeout=10
    [Teardown]    Close Browser

Login With Invalid Credentials
    Open Browser    ${URL}    ${BROWSER}
    Input Text    xpath://input[@name="username"]    ${INVALID_USER}
    Input Text    xpath://input[@name="password"]    ${INVALID_PASSWORD}
    Click Button    xpath://button[@type="submit"]
    Wait Until Page Contains    Invalid credentials    timeout=5
    [Teardown]    Close Browser
