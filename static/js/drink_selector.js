// Initialize all event listeners when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Set up the "Other" drink selection dropdown visibility
    const otherRadio = document.getElementById('other');
    const otherSelect = document.getElementById('other-drink-select');
    const drinkRadios = document.getElementsByName('drink');
    
    if (drinkRadios && otherRadio && otherSelect) {
        drinkRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                if (otherRadio.checked) {
                    otherSelect.style.display = 'inline-block';
                } else {
                    otherSelect.style.display = 'none';
                }
            });
        });
    }
    
    // Set up alcohol percentage select change handler
    const alcoholPercentageSelect = document.getElementById('alcohol-percentage');
    if (alcoholPercentageSelect) {
        alcoholPercentageSelect.addEventListener('change', function() {
            const customAlcoholContainer = document.getElementById('custom-alcohol-container');
            if (alcoholPercentageSelect.value === 'custom' && customAlcoholContainer) {
                customAlcoholContainer.style.display = 'flex';
                document.getElementById('custom-alcohol').focus();
            } else {
                document.getElementById('custom-alcohol-container').style.display = 'none';
            }
        });
    }
    
    // Add event listener for custom amount input to handle Enter key
    const customAmountInput = document.getElementById('custom-amount');
    if (customAmountInput) {
        customAmountInput.addEventListener('keyup', function(event) {
            if (event.key === "Enter") {
                confirmCustomAmount();
            }
        });
    }
    
    // Add event listener for custom alcohol input to handle Enter key
    const customAlcoholInput = document.getElementById('custom-alcohol');
    if (customAlcoholInput) {
        customAlcoholInput.addEventListener('keyup', function(event) {
            if (event.key === "Enter") {
                confirmCustomAlcohol();
            }
        });
    }
    
    // Set up drink radio buttons to show/hide alcohol percentage selector
    const alcoholPercentageContainer = document.getElementById('alcohol-percentage-container');
    const customAlcoholContainer = document.getElementById('custom-alcohol-container');
    
    if (drinkRadios && alcoholPercentageContainer && alcoholPercentageSelect) {
        drinkRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                if (this.value === 'Wine' || this.value === 'Beer' || this.value === 'Cocktail' || this.value === 'Shot') {
                    alcoholPercentageContainer.style.display = 'flex';
                } else {
                    alcoholPercentageContainer.style.display = 'none';
                    alcoholPercentageSelect.value = '0'; // Reset to 0% if not an alcoholic drink
                    if (customAlcoholContainer) {
                        customAlcoholContainer.style.display = 'none'; // Hide custom alcohol input
                    }
                }
            });
        });
    }
});

// Global variable for selected amount
let selectedDrink = 'Water'; // Default drink selected
let selectedAmount = 100; // Default amount
let radioId = 'water'; // Default drink type

/**
 * Function to add a drink
 */
function addDrink() {
    const drinkForm = document.getElementById('drink-form');
    
    console.log("Adding drink...");
    console.log("Selected drink: " + selectedDrink);
    console.log("Selected amount: " + selectedAmount);
    console.log("Selected alcohol percentage: " + getSelectedAlcoholPercentage());
    console.log("Drink Type: " + radioId);

    if (!selectedDrink) {
        alert("Please select a drink.");
        return;
    }
    
    const amount = selectedAmount;
    
    // If "Other" is selected, get the specific drink type from the dropdown
    let drinkType = selectedDrink;
    if (selectedDrink === "Other") {
        const otherSelect = document.getElementById('other-drink-select');
        if (otherSelect && otherSelect.selectedIndex >= 0) {
            drinkType = otherSelect.options[otherSelect.selectedIndex].value;
        }
    }
    
    if (!amount || isNaN(amount) || amount <= 0) {
        alert("Please enter a valid amount.");
        return;
    }
    
    // Get alcohol percentage if applicable
    let alcoholPercentage = 0;
    if (['Wine', 'Beer', 'Cocktail', 'Shot'].includes(drinkType) || 
         selectedDrink === "Alcohol") {
        alcoholPercentage = getSelectedAlcoholPercentage();
        if (isNaN(alcoholPercentage) || alcoholPercentage < 0) {
            alcoholPercentage = 0;
        }
    }
    
    // Prepare data for API call
    const drinkData = {
        drink_name: drinkType,
        amount: parseInt(amount),
        alcohol_percentage: parseFloat(alcoholPercentage)
    };
    
    console.log("Sending data to API:", drinkData);
    
    // Make API call to save drink log
    fetch('/api/add_drink', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'same-origin',
        body: JSON.stringify(drinkData)
    })
    .then(response => {
        if (!response.ok) {
            // Try to get the error message from the response
            return response.json().then(errorData => {
                throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
            }).catch(() => {
                throw new Error(`HTTP error! status: ${response.status}`);
            });
        }
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            throw new Error('Response is not JSON');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            if (alcoholPercentage > 0) {
                console.log(`Added ${amount}ml of ${drinkType} (${alcoholPercentage}% alcohol)`);
                alert(`Added ${amount}ml of ${drinkType} (${alcoholPercentage}% alcohol)!`);
            } else {
                console.log(`Added ${amount}ml of ${drinkType}`);
                alert(`Added ${amount}ml of ${drinkType}!`);
            }
            
            // Reset form
            document.getElementById('amount').value = '';
            
            // Optionally refresh the page or update UI
            // location.reload();
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        if (error.message.includes('401')) {
            alert('Please log in to add drinks.');
        } else if (error.message.includes('500')) {
            alert('Server error: ' + error.message + '. Please check the server logs.');
        } else {
            alert('Failed to save drink: ' + error.message);
        }
    });
}

/**
 * Select a drink from the drink icon carousel
 */
function selectDrink(drinkType) {
    console.log("Selected drink: " + drinkType);
    selectedDrink = drinkType;

    // Highlight the selected icon
    const icons = document.querySelectorAll('.drink-icon');
    icons.forEach(icon => {
        icon.style.transform = 'scale(1)';
        icon.querySelector('img').style.boxShadow = 'none';
    });
    
    // Find the clicked element and highlight it
    const clickedIcon = event.currentTarget;
    clickedIcon.style.transform = 'scale(1.1)';
    clickedIcon.querySelector('img').style.boxShadow = '0 0 10px rgba(255, 255, 255, 0.8)';
    
    // Check if it's an alcoholic drink
    const isAlcoholic = ['Wine', 'Beer', 'Cocktail', 'Shot'].includes(drinkType);
    const alcoholPercentageContainer = document.getElementById('alcohol-percentage-container');
    
    // Show/hide alcohol percentage selector
    if (alcoholPercentageContainer) {
        if (isAlcoholic) {
            alcoholPercentageContainer.style.display = 'flex';
            
            // Set default alcohol percentage based on drink type
            const alcoholPercentageSelect = document.getElementById('alcohol-percentage');
            if (alcoholPercentageSelect) {
                switch(drinkType) {
                    case 'Beer':
                        alcoholPercentageSelect.value = '5';
                        break;
                    case 'Wine':
                        alcoholPercentageSelect.value = '12';
                        break;
                    case 'Cocktail':
                        alcoholPercentageSelect.value = '14';
                        break;
                    case 'Shot':
                        alcoholPercentageSelect.value = '40';
                        break;
                }
            }
        } else {
            alcoholPercentageContainer.style.display = 'none';
            // Reset to 0 for non-alcoholic drinks
            const alcoholPercentageSelect = document.getElementById('alcohol-percentage');
            if (alcoholPercentageSelect) {
                alcoholPercentageSelect.value = '0';
            }
        }
    }
    
    // Set the corresponding radio button
    // let radioId;
    switch(drinkType) {
        case 'Water':
            radioId = 'water';
            break;
        case 'Coffee':
            radioId = 'coffee';
            break;
        case 'Wine':
        case 'Beer':
        case 'Cocktail':
        case 'Shot':
            radioId = 'alcohol';
            break;
        default:
            radioId = 'other';
            
            // If it's "other", show the select dropdown
            const otherSelect = document.getElementById('other-drink-select');
            if (otherSelect) {
                otherSelect.style.display = 'inline-block';
                
                // Try to select the matching option if it exists
                for (let i = 0; i < otherSelect.options.length; i++) {
                    if (otherSelect.options[i].text === drinkType) {
                        otherSelect.selectedIndex = i;
                        break;
                    }
                }
            }
    }
    
    // Set the corresponding radio button
    const radioButton = document.getElementById(radioId);
    if (radioButton) {
        radioButton.checked = true;
        
        // Trigger the change event to ensure any listeners are notified
        const event = new Event('change');
        radioButton.dispatchEvent(event);
    }
    
    // Suggest an amount based on drink type
    const amountInput = document.getElementById('amount');
    if (amountInput) {
        switch(drinkType) {
            case 'Water':
                amountInput.value = '250';
                break;
            case 'Coffee':
                amountInput.value = '200';
                break;
            case 'Wine':
                amountInput.value = '150';
                break;
            case 'Beer':
                amountInput.value = '330';
                break;
            case 'Cocktail':
                amountInput.value = '200';
                break;
            case 'Shot':
                amountInput.value = '45';
                break;
            case 'Soda':
                amountInput.value = '330';
                break;
            case 'Milk':
                amountInput.value = '250';
                break;
            case 'Energy':
                amountInput.value = '250';
                break;
            default:
                amountInput.value = '200';
        }
    }
}

/**
 * Handle selecting a predefined amount from the amount carousel
 */
function selectAmount(amount) {
    console.log(`Selected amount: ${amount}ml`);
    selectedAmount = amount;
    document.querySelectorAll('.amount-option').forEach(option => {
        option.querySelector('div').style.background = 'rgba(13, 110, 253, 0.2)';
        option.querySelector('div').style.color = 'white';
    });
    const activeOption = document.querySelector(`.amount-option[onclick="selectAmount(${amount})"]`);
    if (activeOption) {
        activeOption.querySelector('div').style.background = 'rgba(13, 110, 253, 0.5)';
        activeOption.querySelector('div').style.color = 'white';
    }
    
    // Hide custom amount input if it's visible
    const customAmountContainer = document.getElementById('custom-amount-container');
    if (customAmountContainer) {
        customAmountContainer.style.display = 'none';
    }
    
    // Set the amount input field value
    const amountInput = document.getElementById('amount');
    if (amountInput) {
        amountInput.value = amount;
    }
}

/**
 * Show the custom amount input field when "Other" is clicked
 */
function selectCustomAmount() {
    console.log("Selected custom amount");
    
    // Highlight the "Other" option
    const amountOptions = document.querySelectorAll('.amount-option');
    amountOptions.forEach(option => {
        option.style.transform = 'scale(1)';
        option.querySelector('div').style.boxShadow = 'none';
    });
    
    // Find the clicked element and highlight it
    const clickedOption = event.currentTarget;
    clickedOption.style.transform = 'scale(1.1)';
    clickedOption.querySelector('div').style.boxShadow = '0 0 10px rgba(255, 255, 255, 0.8)';
    
    // Show custom amount container
    const customAmountContainer = document.getElementById('custom-amount-container');
    if (customAmountContainer) {
        customAmountContainer.style.display = 'flex';
        
        // Focus the input field
        const customAmountInput = document.getElementById('custom-amount');
        if (customAmountInput) {
            customAmountInput.focus();
            customAmountInput.select();
        }
    }
}

/**
 * Confirm and set the custom amount when the OK button is clicked
 */
function confirmCustomAmount() {
    const customAmountInput = document.getElementById('custom-amount');
    const amount = customAmountInput.value;
    if (!amount || isNaN(amount) || amount <= 0) {
        alert("Please enter a valid amount.");
        return;
    }
    selectedAmount = amount;
    alert(`Custom amount set to ${amount}ml`);
    document.getElementById('amount').value = amount;
    document.getElementById('custom-amount-container').style.display = 'none';
}

/**
 * Confirm and set a custom alcohol percentage
 */
function confirmCustomAlcohol() {
    const customAlcoholInput = document.getElementById('custom-alcohol');
    if (!customAlcoholInput || !customAlcoholInput.value) {
        alert("Please enter an alcohol percentage.");
        return;
    }
    
    const alcoholPercentage = parseFloat(customAlcoholInput.value);
    if (isNaN(alcoholPercentage) || alcoholPercentage < 0 || alcoholPercentage > 100) {
        alert("Please enter a valid alcohol percentage between 0 and 100.");
        return;
    }
    
    console.log(`Custom alcohol percentage set to ${alcoholPercentage}%`);
    
    // Hide the custom input container
    document.getElementById('custom-alcohol-container').style.display = 'none';
    
    // Store the custom value for retrieval when adding the drink
    document.getElementById('alcohol-percentage').setAttribute('data-custom-value', alcoholPercentage);
}

/**
 * Get the current alcohol percentage (either from dropdown or custom input)
 */
function getSelectedAlcoholPercentage() {
    const alcoholPercentageSelect = document.getElementById('alcohol-percentage');
    if (!alcoholPercentageSelect) return 0;
    
    if (alcoholPercentageSelect.value === 'custom') {
        return parseFloat(alcoholPercentageSelect.getAttribute('data-custom-value') || 0);
    } else {
        return parseFloat(alcoholPercentageSelect.value);
    }
}

