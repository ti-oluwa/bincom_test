const addForm = document.getElementById('result-form');
const addFormNumberField = addForm.querySelector('input[type="number"]');
const addFormSubmitButton = addForm.querySelector('button[type="submit"]');
const addFormSelectFields = addForm.querySelectorAll('select');


// DIVISION FETCHING 

function updateSelectFieldOptionsWithResponseData(nextField, data){
    nextField.querySelectorAll('option').forEach(option => {
        if (option.value){
            nextField.removeChild(option);
        }
    })

    data.forEach((result) => {
        const option = document.createElement('option');

        option.innerHTML = result[`${nextField.name.replace('-', '_')}_name`]
        option.value = result.pk;

        nextField.appendChild(option);
        nextField.disabled = false
    });
}

/**
 * Fetch the options for the next select field after the current field
 * @param {HTMLSelectElement} field Th current select field
 * @returns {object} The options for the next select field
 */
function fetchAndUpdateNextSelectFieldOptions(field) {
    const nextField = field.parentElement.nextElementSibling.querySelector('select');
    if (!nextField) {
        return;
    }

    const siblings = nextField.parentElement.parentElement.querySelectorAll('select');
    siblings.forEach((select, index) => {
        if (select != nextField && index > Array.from(siblings).indexOf(nextField)){
            select.disabled = true;
        };
    });

    const data = {
        'csrfmiddlewaretoken': addForm.querySelector('input[name="csrfmiddlewaretoken"]').value,
    }
    data['previous'] = {
        'name': field.name,
        'value': field.value,
    }
    data['next'] = {
        'name': nextField.name,
    }

    const options = {
        method: addForm.method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': data.csrfmiddlewaretoken,
        },
        body: JSON.stringify(data),
    }

    const baseURL = window.location.origin
    fetch(baseURL + '/results/fetch-next-division/', options).then((response) => {
        if (response.ok){
            response.json().then((data) => {
                updateSelectFieldOptionsWithResponseData(nextField, data.data.results);
            });
        }else{
            throw new Error('Something went wrong');
        };
    });
}


addFormSelectFields.forEach((field) => {
    field.addEventListener('change', () => {
        if(field.name == 'party') return;
        fetchAndUpdateNextSelectFieldOptions(field);
    });
});



addForm.addEventListener('change', () => {

    let allFilled = true;
    addFormSelectFields.forEach((field) => {
        allFilled = allFilled && field.value;
    });

    if (allFilled){
        addFormNumberField.disabled = false;
    };
})


// SUBMITTING RESULTS

addForm.onSubmit = () => {
    addFormSubmitButton.disabled = true;
    addFormSubmitButton.innerHTML = 'Adding Result...';
}


addForm.onResponse = () => {
    addFormSubmitButton.disabled = false;
    addFormSubmitButton.innerHTML = 'Add Result';
}


addForm.addEventListener('submit', (event) => {
    event.stopImmediatePropagation();
    event.preventDefault();

    const formData = new FormData(addForm);
    const data = {};
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    };

    const url = addForm.action;
    const options = {
        method: addForm.method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': data.csrfmiddlewaretoken,
        },
        body: JSON.stringify(data),
    };

    addForm.onSubmit();
    fetch(url, options).then((response) => {
        addForm.onResponse();
        if (response.ok) {
            response.json().then((data) => {
                alert(data.detail)
            });
        } else {
            response.json().then((data) => {
                alert(data.detail)
            });
        }
    });
});
