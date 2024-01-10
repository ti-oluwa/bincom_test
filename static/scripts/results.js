const resultForm = document.getElementById('result-form');
const resultFormSubmitButton = resultForm.querySelector('button[type="submit"]');
const resultTable = document.getElementById('result-table');
const resultTableBody = resultTable.querySelector('tbody');
const resultFormSelectFields = resultForm.querySelectorAll('select');


// DIVISION FETCHING 

/**
 * Updates the options of a select field with the response data
 * @param {HTMLSelectElement} nextField 
 * @param {Array} data  The response data
 */
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
    if (!nextField) return;

    const siblings = nextField.parentElement.parentElement.querySelectorAll('select');
    siblings.forEach((select, index) => {
        if (select != nextField && index > Array.from(siblings).indexOf(nextField)){
            select.disabled = true;
        };
    });

    const data = {
        'csrfmiddlewaretoken': resultForm.querySelector('input[name="csrfmiddlewaretoken"]').value,
    }
    data['previous'] = {
        'name': field.name,
        'value': field.value,
    }
    data['next'] = {
        'name': nextField.name,
    }

    const options = {
        method: resultForm.method,
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


resultFormSelectFields.forEach((field) => {
    field.addEventListener('change', () => {
        fetchAndUpdateNextSelectFieldOptions(field);
    });
});


// RESULTING FETCHING

resultForm.onSubmit = () => {
    resultFormSubmitButton.disabled = true;
    resultFormSubmitButton.innerHTML = 'Fetching Results...';
}


resultForm.onResponse = () => {
    resultFormSubmitButton.disabled = false;
    resultFormSubmitButton.innerHTML = 'Fetch Results';
}


/**
 * Add response data to the result table
 * @param {object} data
 * @returns {void}
 */
function updateResultTableWithResponseData(data) {
    resultTableBody.querySelectorAll('tr').forEach(row => {
        if (row.id !== "no-results"){
            resultTableBody.removeChild(row);
        }
    });

    data.forEach((result) => {
        const row = document.createElement('tr');
        const party = document.createElement('td');
        const score = document.createElement('td');

        party.innerHTML = result.party_abbreviation;
        score.innerHTML = result.party_score;

        row.appendChild(party);
        row.appendChild(score);

        resultTableBody.appendChild(row);
    });

    const countDisplayer = resultTable.parentElement.querySelector('#results-count');
    countDisplayer.innerHTML = data.length;
}



resultForm.addEventListener('submit', (event) => {
    event.stopImmediatePropagation();
    event.preventDefault();

    const formData = new FormData(resultForm);
    const data = {};
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    };

    const url = resultForm.action;
    const options = {
        method: resultForm.method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': data.csrfmiddlewaretoken,
        },
        body: JSON.stringify(data),
    };

    resultForm.onSubmit();
    fetch(url, options).then((response) => {
        resultForm.onResponse();
        if (response.ok) {
            response.json().then((data) => {
                updateResultTableWithResponseData(data.data.results);
            });
        } else {
            response.json().then((data) => {
                alert(data.detail);
            });
            throw new Error('Something went wrong');
        }
    });
});
