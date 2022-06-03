*** Settings ***
Documentation           Sale of new machine in subsidiary without trade-in machine
...                     Includes creating devices with hierarchy, maintaining production and financial dimension to those,
...                     SO creation from device, PO creation from SO, product receipt to sales unit, deliver machine and creating sales invoice
Library                 QWeb
Library                 String
Resource                ${CURDIR}${/}..${/}resources${/}keywords.resource
Suite Setup             Setup_Browser
Test Teardown           Test_Teardown
Suite Teardown          Close All Browsers
Force Tags              MachineSalesBasic
# Variables    myvariables.py

*** Variables ***
${DEVICE_NAME}          Active Frame
${SERIAL_NO}            39MACAA134567
${CHASSIS_NO}           A134567
${MODEL_CODE_PARENT}    Ergo
${MODEL_CONFIG_PARENT}  AF_A22

${MODEL_CODE_BASE}      BaseErgo
${MODEL_CONFIG_BASE}    B_AF_A22
${ITEM_NUMBER_BASE}     B_AF_A22

${MODEL_CODE_CABIN}     FixedCabin
${MODEL_CONFIG_CABIN}   FixedCabin_B02
${ITEM_NUMBER_CABIN}    ${MODEL_CONFIG_CABIN}

*** Keywords ***
Create Device with child devices
    [Documentation]    Creating devices with hierarchy, base, cabin, crane and harvester head devices as childs
    ...    System generated device numbers are used but renamed to have -TA (main device) or -TAS (child devices) in place of -
    ...    Notes down device numbers and project number which is sub-part of the main device number

    Login_D365    TEST_AUT_ERP_CLOUD

    Log    Create and rename the parent device to have -TA part in middle
    ${device_parent}=    Device_Create    New device    Brand    Harvester    ${MODEL_CODE_PARENT}    ${MODEL_CONFIG_PARENT}
    ${device_prefix}=    Fetch From Left    ${device_parent}    -
    ${device_suffix}=    Fetch From Right    ${device_parent}    -
    ${project_number}=    Set Variable    TA${device_suffix}
    ${device_number_new}=    Set Variable    ${device_prefix}-TA${device_suffix}
    ${device_parent}=    Device_Rename    device_new=${device_number_new}    navigate=False

    Log    Create child devices and rename them to have -TAS part in middle
    ${device_base111111235123412785789}=    Device_Create    New device    Brand111111111111111111    BaseMachine    ${MODEL_CODE_BASE}    ${MODEL_CONFIG_BASE}
    ${device_number_new}=    Replace String    ${device_base}    -    -TAS
    ${device_base}=    Device_Rename    device_new=${device_number_new}    navigate=False

    ${device_cabin}=    Device_Create    New device    Brand    Cabin    ${MODEL_CODE_CABIN}    ${MODEL_CONFIG_CABIN}
    ${device_number_new}=    Replace String    ${device_cabin}    -    -TAS
    ${device_cabin}=    Device_Rename    device_new=${device_number_new}    navigate=False

    ${device_crane}=    Device_Create    New device    Brand    Crane    ${MODEL_CODE_CRANE}    ${MODEL_CONFIG_CRANE}
    ${device_number_new}=    Replace String    ${device_crane}    -    -TAS
    ${device_crane}=    Device_Rename    device_new=${device_number_new}    navigate=False

    ${device_head}=    Device_Create    New device    Brand    HarvesterHead    ${MODEL_CODE_HEAD}    ${MODEL_CONFIG_HEAD}
    ${device_number_new}=    Replace String    ${device_head}    -    -TAS
    ${device_head}=    Device_Rename    device_new=${device_number_new}    navigate=False

    Log    Connect child devices to the parent
    Log    Search and open the parent device
    Navigate_Modules    Device management>Devices>All devices
    Filter_And_Open    ${device_parent}

    ClickText    Device
    ClickText    Child devices

    ClickText    New
    TypeText    Item number    ${ITEM_NUMBER_BASE}
    TypeText    Device number    ${device_base}

    ClickText    New
    TypeText    Item number    ${ITEM_NUMBER_CABIN}
    TypeText    Device number    ${device_cabin}

    ClickText    New
    TypeText    Item number    ${ITEM_NUMBER_CRANE}
    TypeText    Device number    ${device_crane}

    ClickText    New
    TypeText    Item number    ${MODEL_CONFIG_HEAD}
    TypeText    Device number    ${device_head}

    ClickText    Save
    ClickItem    Select or unselect all rows
    ClickText    Install
    ClickText    OK    anchor=Cancel
    Message_Verify    Install child device Specification list successfully updated
    LogScreenshot

    Set Suite Variable    ${DEVICE_PARENT}
    Set Suite Variable    ${PROJECT_NUMBER}
    Set Suite Variable    ${DEVICE_BASE}
    Set Suite Variable    ${DEVICE_CABIN}
    Set Suite Variable    ${DEVICE_CRANE}
    Set Suite Variable    ${DEVICE_HEAD}

Add production information and financial dimension to the devices
    [Documentation]    Creates GL financial dimension for the device and maintains that to the all devices in the hierarcical device
    ...    At the same time adding Production information and chassis/serial numbers to the devices

    Log    Create GL financial dimension value for Device
    ${dimension_device}=    Set Variable    ${PROJECT_NUMBER}
    FinaDimension_CreateValue    Device    ${dimension_device}    group_description=${DEVICE_NAME} ${CHASSIS_NO}

    Log    Add Production information and Maintain created financial dimension to the devices
    ${current_date}=    Get Current Date    result_format=%d.%m.%Y
    ${current_year}=    Get Time    year
    Log To Console    ${current_year}
    ${inputs_string}=   Catenate                  SEPARATOR=  # robotidy: off
    ...    {
    ...    "Production information":
    ...    {
    ...        "Production date":   {"type": "text",  "value": "${current_date}"},
    ...        "Model year":        {"type": "text",  "value": "${current_year}"}
    ...    },
    ...    "Identification and security":
    ...    {
    ...        "Chassis number":    {"type": "text",  "value": "${CHASSIS_NO}"},
    ...        "Serial number":     {"type": "text",  "value": "${SERIAL_NO}"}
    ...    },
    ...    "Financial dimensions":
    ...    {
    ...        "Device":            {"type": "text",  "value": "${dimension_device}",  "anchor": "GroupAccount"}
    ...    }
    ...    }
    Device_Edit    ${device_parent}    ${inputs_string}
    Device_Edit    ${device_base}    ${inputs_string}
    Device_Edit    ${device_cabin}    ${inputs_string}
    Device_Edit    ${device_crane}    ${inputs_string}
    Device_Edit    ${device_head}    ${inputs_string}

Create sales order from parent device
    [Documentation]    Creates sales order from parent device and maintains some requested ship and receipt dates plus maintain unit price for the first line
    ...    Notes down the SO number

    ${requested_ship_date}=    Get Current Date    result_format=%d.%m.%Y
    ${requested_receipt_date}=    Get Current Date    result_format=%d.%m.%Y

    Log    Create sales order from device
    ${datas_string}=    Catenate                  SEPARATOR=  # robotidy: off
    ...    {
    ...    "Customer":
    ...    {
    ...        "Customer account":   {"type": "text",  "value": "${CUSTOMER}"}
    ...    },
    ...    "General":
    ...    {
    ...        "Site":               {"type": "text",  "value": "${SITE}"},
    ...        "Warehouse":          {"type": "text",  "value": "${WAREHOUSE}"},
    ...        "Customer requisition":  {"type": "text",  "value": "Test Automation requ"},
    ...        "Customer reference": {"type": "text",  "value": "Test Automation reference"}
    ...    },
    ...    "Administration":
    ...    {
    ...        "Pool":               {"type": "verify",  "value": "${POOL}",  "anchor": "GroupAccount"}
    ...    }
    ...    }
    ${sales_order}=    SalesOrder_CreateFromDevice    ${DEVICE_PARENT}    ${datas_string}

    Log    Maintain requested ship and receipt dates plus maintain unit price for the first line
    SalesOrder_Modify    navigate=False
    ...    header_data={ "Delivery": { "Requested ship date": "${requested_ship_date}", "Requested receipt date": "${requested_receipt_date}" } }
    ...    lines_table_data={ "1": { "Unit price": "${UNIT_PRICE_SALES}" } }

    Set Suite Variable    ${SALES_ORDER}

Create purchase order from sales order
    [Documentation]    Creates purchase order from sales order with Include all option enabled. Notes down the PO.

    ${purchase_order}=    PurchaseOrder_CreateFromSO    ${SALES_ORDER}

    Set Suite Variable    ${PURCHASE_ORDER}

Maintain transfer price to PO line and confirm the PO
    [Documentation]    Maintains transfer price to PO line and confirms the PO

    PurchaseOrder_Modify    ${PURCHASE_ORDER}    lines_table_data= { "1": {"Unit price": "800000"} }
    PurchaseOrder_Confirm    navigate=False

Post product receipt
    [Documentation]    Posts product receipt in PO from factory

    Log    Maintain financial dimensions (TODO: this should be unnecessary after some CR is completed)
    PurchaseOrder_Modify    ${PURCHASE_ORDER}
    ...    header_data={ "Financial dimensions": { "Device": {"type": "text", "value": "${PROJECT_NUMBER}", "anchor": "GroupAccount"} } }
    PurchaseOrder_Confirm    navigate=False

    Log    Post product receipt
    PurchaseOrder_Receive    navigate=False    product_receipt=${PURCHASE_ORDER}

Verify device major status is In stock
    Navigate_Modules    Device management>Devices>All devices
    Filter_And_Open    ${DEVICE_PARENT}

    VerifyItem    Major status: In stock
    LogScreenshot

Post packing slip to deliver sales order to customer
    [Documentation]    Posts packing slip to deliver sales order to customer

    Log    Maintain financial dimensions to SO header (TODO: this should be unnecessary after some CR is completed)
    SalesOrder_Modify    ${SALES_ORDER}
    ...    header_data={ "Financial dimensions": { "Device": {"type": "text", "value": "${PROJECT_NUMBER}", "anchor": "GroupAccount"} } }

    SalesOrder_PostPackingSlip    navigate=False    #${SALES_ORDER}

Verify device major status is Delivered
    Navigate_Modules    Device management>Devices>All devices
    Filter_And_Open    ${DEVICE_PARENT}

    VerifyItem    Major status: Delivered
    LogScreenshot

Create sales invoice to customer
    [Documentation]    Creates sales invoice to the customer and checks the printout, notes down invoice number

    ${sales_invoice}=    SalesOrder_InvoiceCreate    ${SALES_ORDER}

    Set Suite Variable    ${SALES_INVOICE}

Verify device major status is Sold
    Navigate_Modules    Device management>Devices>All devices
    Filter_And_Open    ${DEVICE_PARENT}

    VerifyItem    Major status: Sold
    LogScreenshot
