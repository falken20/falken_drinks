/**
 * Unit tests for the embedded JavaScript in templates/drinks_management.html
 *
 * Functions tested:
 *   setupPercentageSliders, resetForm, populateForm,
 *   displayDrinks, saveDrink (validation), deleteDrink (validation),
 *   showLoading, hideLoading
 */

const fs = require('fs');
const path = require('path');

// ─── Extract the main <script> block from the Jinja2 template ───────────────

function extractMainScript(templatePath) {
    const html = fs.readFileSync(templatePath, 'utf-8');
    const blocks = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
    // The largest block is the main component script
    return blocks.sort((a, b) => b[1].length - a[1].length)[0][1];
}

const templatePath = path.resolve(
    __dirname, '../../templates/drinks_management.html'
);
const mainScript = extractMainScript(templatePath);

// Load the script ONCE into the global (jsdom) context so function
// declarations become globally accessible in tests. 'let' module-scope
// variables (isEditing, editingDrinkId) are in the eval closure so they
// cannot be read/written directly from tests; all functions work normally.
(0, eval)(mainScript);

// ─── Minimal DOM structure required by the component ────────────────────────

function buildDOM() {
    document.body.innerHTML = `
        <div id="loadingModal" aria-hidden="true" style="display: none;">
            <div class="modal-dialog">
                <div class="modal-content"><div class="modal-body"></div></div>
            </div>
        </div>

        <form id="drink-form">
            <input type="hidden" id="drink-id" value="">
            <input type="text"   id="drink-name"  value="">
            <input type="range"  id="water-percentage"   min="0" max="100" value="100">
            <input type="range"  id="alcohol-percentage" min="0" max="100" value="0">
            <input type="range"  id="other-percentage"   min="0" max="100" value="0">
            <input type="text"   id="drink-image" value="">
            <input type="checkbox" id="counts-as-water" checked>
            <button type="submit" id="save-btn">Save Drink</button>
        </form>

        <span id="water-value">100%</span>
        <span id="alcohol-value">0%</span>
        <span id="other-value">0%</span>
        <h3 id="form-title">Add New Drink</h3>
        <div id="drinks-list"></div>
    `;
}

// ─── Mocks ────────────────────────────────────────────────────────────────────

const bootstrapModalMock = {
    show: jest.fn(),
    hide: jest.fn()
};
const bootstrapMock = {
    Modal: Object.assign(
        jest.fn(() => bootstrapModalMock),
        { getInstance: jest.fn(() => bootstrapModalMock) }
    )
};

beforeEach(() => {
    buildDOM();
    // jsdom does not implement scrollIntoView — mock it globally
    window.HTMLElement.prototype.scrollIntoView = jest.fn();
    global.alert   = jest.fn();
    global.confirm = jest.fn(() => true);
    global.fetch   = jest.fn();
    global.bootstrap = bootstrapMock;
    jest.clearAllMocks();
    // Reset isEditing / editingDrinkId to defaults so tests are isolated
    resetForm();
});

// ─── resetForm ────────────────────────────────────────────────────────────────

describe('resetForm', () => {
    test('clears form fields and resets title to "Add New Drink"', () => {
        document.getElementById('drink-name').value = 'Old Name';
        document.getElementById('form-title').textContent = 'Edit Drink';
        resetForm();
        expect(document.getElementById('drink-name').value).toBe('');
        expect(document.getElementById('form-title').textContent).toBe('Add New Drink');
    });

    test('resets water slider to 100 and other displays', () => {
        document.getElementById('water-percentage').value = '50';
        resetForm();
        expect(document.getElementById('water-percentage').value).toBe('100');
        expect(document.getElementById('water-value').textContent).toBe('100%');
    });

    test('resets alcohol slider to 0', () => {
        document.getElementById('alcohol-percentage').value = '10';
        resetForm();
        expect(document.getElementById('alcohol-percentage').value).toBe('0');
        expect(document.getElementById('alcohol-value').textContent).toBe('0%');
    });

    test('resets other-percentage slider to 0', () => {
        document.getElementById('other-percentage').value = '50';
        resetForm();
        expect(document.getElementById('other-percentage').value).toBe('0');
        expect(document.getElementById('other-value').textContent).toBe('0%');
    });

    test('checks counts-as-water checkbox', () => {
        document.getElementById('counts-as-water').checked = false;
        resetForm();
        expect(document.getElementById('counts-as-water').checked).toBe(true);
    });
});

// ─── populateForm ─────────────────────────────────────────────────────────────

describe('populateForm', () => {
    const sampleDrink = {
        drink_id: 7,
        drink_name: 'Lemonade',
        drink_water_percentage: 80,
        drink_alcohol_percentage: 0,
        drink_image: '',
        counts_as_water: true
    };

    test('sets form-title to "Edit Drink"', () => {
        populateForm(sampleDrink);
        expect(document.getElementById('form-title').textContent).toBe('Edit Drink');
    });

    test('populates drink name field', () => {
        populateForm(sampleDrink);
        expect(document.getElementById('drink-name').value).toBe('Lemonade');
    });

    test('sets water percentage slider and display', () => {
        populateForm(sampleDrink);
        expect(document.getElementById('water-percentage').value).toBe('80');
        expect(document.getElementById('water-value').textContent).toBe('80%');
    });

    test('sets other-percentage display and slider', () => {
        populateForm(sampleDrink);
        const expected = 100 - 80 - 0;
        expect(document.getElementById('other-value').textContent).toBe(`${expected}%`);
        expect(document.getElementById('other-percentage').value).toBe(String(expected));
    });

    test('sets counts-as-water checkbox', () => {
        const alcoholicDrink = { ...sampleDrink, counts_as_water: false };
        populateForm(alcoholicDrink);
        expect(document.getElementById('counts-as-water').checked).toBe(false);
    });

    test('defaults counts-as-water to true when undefined', () => {
        const drinkWithoutFlag = { ...sampleDrink };
        delete drinkWithoutFlag.counts_as_water;
        populateForm(drinkWithoutFlag);
        expect(document.getElementById('counts-as-water').checked).toBe(true);
    });
});

// ─── setupPercentageSliders ────────────────────────────────────────────────────

describe('setupPercentageSliders', () => {
    test('auto-calculates other percentage from water + alcohol', () => {
        setupPercentageSliders();
        const waterSlider   = document.getElementById('water-percentage');
        const alcoholSlider = document.getElementById('alcohol-percentage');

        waterSlider.value   = '60';
        alcoholSlider.value = '20';
        waterSlider.dispatchEvent(new Event('input'));

        expect(document.getElementById('other-value').textContent).toBe('20%');
        expect(document.getElementById('other-percentage').value).toBe('20');
    });

    test('auto-unchecks counts-as-water when alcohol > 0', () => {
        setupPercentageSliders();
        document.getElementById('counts-as-water').checked = true;
        const alcoholSlider = document.getElementById('alcohol-percentage');
        alcoholSlider.value = '5';
        alcoholSlider.dispatchEvent(new Event('input'));
        expect(document.getElementById('counts-as-water').checked).toBe(false);
    });

    test('re-checks counts-as-water when alcohol returns to 0', () => {
        setupPercentageSliders();
        document.getElementById('counts-as-water').checked = false;
        const alcoholSlider = document.getElementById('alcohol-percentage');
        alcoholSlider.value = '0';
        alcoholSlider.dispatchEvent(new Event('input'));
        expect(document.getElementById('counts-as-water').checked).toBe(true);
    });

    test('shows error color when water + alcohol > 100', () => {
        setupPercentageSliders();
        document.getElementById('water-percentage').value   = '80';
        document.getElementById('alcohol-percentage').value = '30';
        document.getElementById('water-percentage').dispatchEvent(new Event('input'));
        expect(document.getElementById('other-value').style.color).toBe('rgb(220, 53, 69)');
    });

    test('resets other value color when total <= 100', () => {
        setupPercentageSliders();
        document.getElementById('water-percentage').value   = '50';
        document.getElementById('alcohol-percentage').value = '10';
        document.getElementById('water-percentage').dispatchEvent(new Event('input'));
        expect(document.getElementById('other-value').style.color).toBe('white');
    });
});

// ─── displayDrinks ────────────────────────────────────────────────────────────

describe('displayDrinks', () => {
    test('renders "No drinks found" when list is empty', () => {
        displayDrinks([]);
        expect(document.getElementById('drinks-list').innerHTML).toContain('No drinks found');
    });

    test('renders a card for each drink', () => {
        const drinks = [
            { drink_id: 1, drink_name: 'Water',  drink_water_percentage: 100, drink_alcohol_percentage: 0, drink_image: '' },
            { drink_id: 2, drink_name: 'Wine',   drink_water_percentage: 87,  drink_alcohol_percentage: 13, drink_image: '' }
        ];
        displayDrinks(drinks);
        const cards = document.querySelectorAll('.drink-card');
        expect(cards.length).toBe(2);
    });

    test('shows drink name in each card', () => {
        const drinks = [
            { drink_id: 1, drink_name: 'Coffee', drink_water_percentage: 98, drink_alcohol_percentage: 0, drink_image: '' }
        ];
        displayDrinks(drinks);
        expect(document.getElementById('drinks-list').innerHTML).toContain('Coffee');
    });

    test('renders image tag when drink_image is provided', () => {
        const drinks = [
            { drink_id: 1, drink_name: 'Water', drink_water_percentage: 100,
              drink_alcohol_percentage: 0, drink_image: 'icons8-water-96.png' }
        ];
        displayDrinks(drinks);
        expect(document.getElementById('drinks-list').innerHTML).toContain('<img');
    });

    test('renders initial letter avatar when drink_image is empty', () => {
        const drinks = [
            { drink_id: 1, drink_name: 'Juice', drink_water_percentage: 90,
              drink_alcohol_percentage: 0, drink_image: '' }
        ];
        displayDrinks(drinks);
        // First letter of "Juice" = J
        expect(document.getElementById('drinks-list').innerHTML).toContain('>J<');
    });

    test('shows alcohol emoji only when alcohol > 0', () => {
        const drinks = [
            { drink_id: 1, drink_name: 'Wine', drink_water_percentage: 87,
              drink_alcohol_percentage: 13, drink_image: '' }
        ];
        displayDrinks(drinks);
        expect(document.getElementById('drinks-list').innerHTML).toContain('🍷');
    });

    test('does not show alcohol emoji for non-alcoholic drink', () => {
        const drinks = [
            { drink_id: 1, drink_name: 'Water', drink_water_percentage: 100,
              drink_alcohol_percentage: 0, drink_image: '' }
        ];
        displayDrinks(drinks);
        expect(document.getElementById('drinks-list').innerHTML).not.toContain('🍷');
    });
});

// ─── saveDrink – validation ───────────────────────────────────────────────────

describe('saveDrink – validation', () => {
    test('alerts when drink name is empty', () => {
        document.getElementById('drink-name').value = '';
        saveDrink();
        expect(global.alert).toHaveBeenCalledWith('Please enter a drink name');
    });

    test('alerts when water + alcohol percentages exceed 100', () => {
        document.getElementById('drink-name').value = 'Test';
        document.getElementById('water-percentage').value   = '80';
        document.getElementById('alcohol-percentage').value = '30';
        saveDrink();
        expect(global.alert).toHaveBeenCalledWith(
            'Water and alcohol percentages cannot exceed 100% total'
        );
    });

    test('calls fetch with POST when not editing', () => {
        global.fetch = jest.fn(() => Promise.resolve({
            ok: true,
            json: () => Promise.resolve({ success: true, message: 'created' })
        }));

        document.getElementById('drink-name').value = 'Juice';
        document.getElementById('water-percentage').value   = '90';
        document.getElementById('alcohol-percentage').value = '0';
        saveDrink();

        expect(global.fetch).toHaveBeenCalledWith(
            '/api/drinks',
            expect.objectContaining({ method: 'POST' })
        );
    });
});

// ─── deleteDrink ──────────────────────────────────────────────────────────────

describe('deleteDrink', () => {
    test('does not call fetch when user cancels confirm dialog', () => {
        global.confirm = jest.fn(() => false);
        deleteDrink(1, 'Water');
        expect(global.fetch).not.toHaveBeenCalled();
    });

    test('calls DELETE when user confirms', () => {
        global.confirm = jest.fn(() => true);
        global.fetch = jest.fn(() => Promise.resolve({
            ok: true,
            json: () => Promise.resolve({ success: true, message: 'deleted' })
        }));

        deleteDrink(5, 'Beer');

        expect(global.fetch).toHaveBeenCalledWith(
            '/api/drinks/5',
            expect.objectContaining({ method: 'DELETE' })
        );
    });
});

// ─── hideLoading ──────────────────────────────────────────────────────────────

describe('hideLoading', () => {
    test('sets modal display to none', () => {
        const modal = document.getElementById('loadingModal');
        modal.style.display = 'block';
        hideLoading();
        expect(modal.getAttribute('style')).toContain('display: none');
    });

    test('removes modal-open class from body', () => {
        document.body.classList.add('modal-open');
        hideLoading();
        expect(document.body.classList.contains('modal-open')).toBe(false);
    });

    test('does not throw when modal element is absent', () => {
        document.getElementById('loadingModal').remove();
        expect(() => hideLoading()).not.toThrow();
    });
});
