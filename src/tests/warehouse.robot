*** Settings ***
Library           RequestsLibrary
Library           Process
Library           BuiltIn
Suite Setup       Start Warehouse
Suite Teardown    Stop Warehouse

*** Variables ***
${BASE_URL}       http://127.0.0.1:5001

*** Test Cases ***
Create Storage And Show Balance
    ${created}=    POST    ${BASE_URL}/storages    data=name=Robot%20tools&capacity=12    headers=${{ {'Content-Type': 'application/x-www-form-urlencoded'} }}
    Should Be Equal As Integers    ${created.status_code}    200
    ${page}=    GET    ${BASE_URL}/
    Should Contain    ${page.text}    Robot tools
    Should Contain    ${page.text}    0.00</strong> / 12.00

Add And Take Stock
    POST    ${BASE_URL}/storages/1/stock    data=quantity=8&action=add    headers=${{ {'Content-Type': 'application/x-www-form-urlencoded'} }}
    POST    ${BASE_URL}/storages/1/stock    data=quantity=3&action=take    headers=${{ {'Content-Type': 'application/x-www-form-urlencoded'} }}
    ${page}=    GET    ${BASE_URL}/
    Should Contain    ${page.text}    5.00</strong> / 12.00

*** Keywords ***
Start Warehouse
    Start Process    uv    run    --project    ${EXECDIR}    python    ${EXECDIR}/src/web.py
    Wait Until Keyword Succeeds    10x    1s    GET    ${BASE_URL}/
    Create Session    warehouse    ${BASE_URL}

Stop Warehouse
    Terminate All Processes    kill=${TRUE}
