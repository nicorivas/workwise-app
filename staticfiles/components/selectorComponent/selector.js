import AbstractComponent from "../abstractComponent.js";

export default class SelectorComponent extends AbstractComponent {

    constructor(element) {
        super(element);
        // Elements
        this.$selected = this.$element.find(".selector__selected-item");
        this.$itemsContainer = this.$element.find(".selector__items-container");
        this.$items = this.$element.find(".selector__item");
        this.$text = this.$element.find(".selector__selected-item-text");
        // Define state
        this.state = {
            "open": false,
            "selected": "",
            "highlight": this.$element.find(".selector--highlight").length > 0,
            "active": this.$element.find(".selector--active").length > 0,
            "small": this.$element.find(".selector--small").length > 0,
        }
        // Others
        this.functions = [];
        this.init();
    }

    init() {
        this.bindEvents();

        // Set initial state. Initial selected item is the first item.
        // This is just state: it doesn't trigger the first item click event.
        this.setState({
            "open": false,
            "selected": this.$items.first(),
        });
    }

    bindEvents() {
        this.bindEvent("click", this.selectedItemClick, ".selector__selected-item");
        this.bindEvent("click", this.itemClick, ".selector__item");

        // Hide the dropdown when clicked outside
        jQuery(document).click((e) => {
            if (!jQuery(e.target).closest('.selector-wrapper').length) {
                this.setState({"open": false,})
            }
        });
    }

    selectedItemClick(e) {
        e.stopPropagation();
        if (this.$items.length > 0) {
            // Open dropdown if closed, close if open
            if (this.state.open) {
                this.setState({"open": false,})
            } else {
                this.setState({"open": true,})
            }
        }
        
    }

    itemClick(e) {
        e.stopPropagation();

        // Get item clicked
        let $item = jQuery(e.currentTarget);

        // Iterate over functions and call them
        this.functions.forEach((funcObject) => {
            const {func, args} = funcObject;
            args.push($item);
            console.log("Button.buttonClick(): call function", func, args);
            // Execute the function, when it finished executing, set state back to idle
            Promise.resolve(func(...args)).then((e) => {
                console.log("Button.buttonClick(): return function", func, args);
            });
        });

        // Change of state after selection
        this.selectionAfter($item);
    }

    select(id) {
        let $item = this.$element.find(`.selector-item[data-id="${id}"]`);
        this.selectionAfter($item);
    }

    selectionAfter($item) {
        this.setState({
            "open": false,
            "selected_text":jQuery.trim($item.text())
        })
    }

    setSelectedText(text) {
        this.$text.text(text);
    }

    clearText() {
        this.$text.text("");
    }

    addFunction(func, args = []) {
        this.functions.push({func, args});        
    }

    render() {
        // Show or hide selector items
        if (this.state.open) {
            this.$selected.addClass("selector__selected-item--open");
            this.$itemsContainer.show();
        } else {
            this.$selected.removeClass("selector__selected-item--open");
            this.$itemsContainer.hide();
        }

        if (this.state.highlight) {
            this.$selected.addClass("selector__selected-item--highlight");
            this.$itemsContainer.addClass("selector__items-container--highlight");
        } else {
            this.$selected.removeClass("selector__selected-item--highlight");
            this.$itemsContainer.removeClass("selector__items-container--highlight");
        }

        if (this.state.active) {
            this.$selected.addClass("selector--active");
        } else {
            this.$selected.removeClass("selector--active");
        }

        if (this.state.small) {
            this.$selected.addClass("selector--small");
        } else {
            this.$selected.removeClass("selector--small");
        }

        this.$text.text(this.state.selected.text());
    }
}