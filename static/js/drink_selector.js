// Add this function to your existing falken.js file
function selectDrink(drinkType) {
    console.log("Selected drink: " + drinkType);
    
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
    let radioId;
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
    console.log("Selected amount: " + amount + "ml");
    
    // Highlight the selected amount option
    const amountOptions = document.querySelectorAll('.amount-option');
    amountOptions.forEach(option => {
        option.style.transform = 'scale(1)';
        option.querySelector('div').style.boxShadow = 'none';
    });
    
    // Find the clicked element and highlight it
    const clickedOption = event.currentTarget;
    clickedOption.style.transform = 'scale(1.1)';
    clickedOption.querySelector('div').style.boxShadow = '0 0 10px rgba(255, 255, 255, 0.8)';
    
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
