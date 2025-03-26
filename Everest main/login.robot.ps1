*** Settings ***
Library    SeleniumLibrary
Suite Setup    Open Browser    https://qa.dashboard.everest.7span.in/#/login    chrome
Suite Teardown    Close Browser

*** Variables ***
${WAIT_TIME}    10
${EMAIL_FIELD}    id=email
${PASSWORD_FIELD}    id=password
${LOGIN_BUTTON}    xpath=//button[@type='submit']
${ERROR_MESSAGE_XPATH}    xpath=//p[normalize-space(text())]

*** Keywords ***
Login With Credentials
    [Arguments]    ${email}    ${password}
    Input Text    ${EMAIL_FIELD}    ${email}
    Input Text    ${PASSWORD_FIELD}    ${password}
    Click Button    ${LOGIN_BUTTON}
    Wait For Page To Load

Check For Error Message
    [Arguments]    ${expected_error}
    Wait For Element    ${ERROR_MESSAGE_XPATH}[normalize-space(text())='${expected_error}']
    ${error_text}=    Get Text    ${ERROR_MESSAGE_XPATH}[normalize-space(text())='${expected_error}']
    Should Be Equal As Strings    ${error_text}    ${expected_error}

Wait For Page To Load
    Wait Until Element Is Visible    ${LOGIN_BUTTON}

Scroll Down And Up
    Execute JavaScript    window.scrollTo(0, document.body.scrollHeight);
    Sleep    2
    Execute JavaScript    window.scrollTo(0, 0);
    Log    Scrolling test passed!

*** Test Cases ***
Test Login With Wrong Email And Password
    Login With Credentials    wrong.email@7span.com    wrongpassword
    Check For Error Message    Invalid email or password.

Test Login With Valid Email And Wrong Password
    Login With Credentials    krunal.b@7span.com    wrongpassword
    Check For Error Message    Invalid email or password.

Test Login With Empty Email And Filled Password
    Login With Credentials    ""    1
    Check For Error Message    Email is required.

Test Login With Filled Email And Empty Password
    Login With Credentials    krunal.b@7span.com    ""
    Check For Error Message    Password is required.

Test Login With Both Fields Empty
    Login With Credentials    ""    ""
    Check For Error Message    Email is required.

Test Login With Non 7span Email
    Login With Credentials    test@gmail.com    1
    Check For Error Message    Only 7span.com email is allowed.

Test Login With Valid Credentials
    Login With Credentials    krunal.b@7span.com    1

Test Scroll Down And Up On Login Page
    Scroll Down And Up
