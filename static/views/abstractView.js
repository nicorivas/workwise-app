import ErrorMessageComponent from "../components/errorMessageComponent/errorMessage.js";

export default class AbstractView {

    constructor(element) {
        this.$element; // The jQuery element for this view
        this.data = {}; // A basic example of how you might manage data for this view
        this.events = {}; // Store event listeners
        if (new.target === AbstractView) {
            throw new TypeError("Cannot construct AbstractView instances directly");
        }
        if (typeof element === "string") {
            this.$element = jQuery(element);
        } else {
            this.$element = element;
        }
        if (this.$element.length === 0) {
            throw new Error(`Element not found: ${element}`);
        }
        this.errorMessageComponent = new ErrorMessageComponent("#error-message");
    }

    init() {
        this.bindEvents();
    }

    render() {
        // This is where you'd render your view and attach any components
        
    }

    update() {
        // Called when the view needs to update itself, possibly due to data changes
        this.render();
    }

    destroy() {
        // Cleanup tasks when the view is no longer needed
        this.unbindEvents();
    }

    bindEvents() {
        // Use jQuery or any other method to attach event listeners
        // Example: $(this.element).on('click', this.handleClick.bind(this));
    }

    unbindEvents() {
        // Use jQuery or any other method to remove event listeners
        // Example: $(this.element).off('click', this.handleClick.bind(this));
    }

    setData(newData) {
        this.data = { ...this.data, ...newData };
        this.update();
    }

    navigateTo(newView) {
        // Handle navigation tasks here, perhaps unloading the current view and loading the new one
    }

    showError(error) {
        this.errorMessageComponent.show(error);
    }

}