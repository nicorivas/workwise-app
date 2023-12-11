export default class AbstractComponent {
    constructor(element) {
        if (new.target === AbstractComponent) {
            throw new TypeError("Cannot construct AbstractComponent instances directly");
        }
        if (typeof element === "string") {
            this.$element = jQuery(element);
        } else {
            this.$element = element;
        }
        if (this.$element.length === 0) {
            throw new Error(`Element not found: ${element}`);
        }
        this.state = {}; // Initial empty state
        this.functions = []; // Function call on event
    }

    setState(newState) {
        this.state = {...this.state, ...newState}; // Merge current state with new state
        this.render(); // Re-render the component after a state change
    }

    getState() {
        return this.state;
    }

    init() {
        throw new Error("Method 'init()' must be implemented.");
    }

    render() {
        throw new Error("Method 'render()' must be implemented.");
    }

    destroy() {
        // Default behavior is no-op
    }

    bindEventToElement(event, handler, element, ...args) {
        element.on(event, handler.bind(this, ...args));
    }

    bindEvent(event, handler, selector=null, ...args) {
        if (selector === null) {
            this.$element.on(event, handler.bind(this, ...args));
        } else {
            if (jQuery(selector).length === 0) {
                throw new Error(`Element not found: ${selector}`);
            }    
            this.$element.on(event, selector, handler.bind(this, ...args));
        }
    }

    unbindEvent(event, selector) {
        this.$element.off(event, selector);
    }

    callFunctions(e) {
        // Call registered functions.
        this.functions.forEach((funcObject) => {
            const {func, args} = funcObject;
            // We add the event to the arguments of the function, always at the end.
            args.push(e);
            // Execute the function, when it finished executing, set state back to idle
            Promise.resolve(func(...args)).then((e) => {
                /**/
            });
        });
    }

    addFunction(func, args = []) {
        this.functions.push({func, args});        
    }

    clearFunctions() {
        this.functions = [];
    }
}