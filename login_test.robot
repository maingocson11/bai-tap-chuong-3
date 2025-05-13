*** Settings ***
Library    SeleniumLibrary
Suite Setup    Open Browser    https://opensource-demo.orangehrmlive.com/web/index.php/auth/login    chrome
Suite Teardown    Close Browser

*** Variables ***
${USERNAME}    Admin
${PASSWORD}    admin123
${INVALID_PASSWORD}    wrongpassword

*** Test Cases ***
Valid Login Test
    [Documentation]    Kiểm tra đăng nhập hợp lệ
    Input Text    id=username    ${USERNAME}
    Input Text    id=password    ${PASSWORD}
    Click Button    xpath=//button[@type='submit']
    Page Should Contain    Welcome

Invalid Login Test
    [Documentation]    Kiểm tra đăng nhập không hợp lệ
    Input Text    id=username    ${USERNAME}
    Input Text    id=password    ${INVALID_PASSWORD}
    Click Button    xpath=//button[@type='submit']
    Page Should Contain    Invalid credentials
