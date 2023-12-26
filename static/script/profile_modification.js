
let userAttributes = document.getElementsByClassName("account-attribute");

function getIdValues(element) {
    let elementId = element.id;
    let parts = elementId.split("-");
    let newValueRaw = element.innerText;
    let newValueData = newValueRaw.split(":");
    let newValue = null;
    if(newValueData.length > 1) {
        newValue = newValueData.at(1).trim();
    }
    else {
        newValue = newValueData.at(0).trim();
    }
    return {attribute: parts.at(1), accountId: parseInt(parts.at(2)), newValue: newValue}
}

