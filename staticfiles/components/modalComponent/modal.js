import AbstractComponent from "../abstractComponent.js";

/**
 * Table component. Uses DataTables to handle table.
 * 
 * @extends AbstractComponent
 * @class
 */
export default class ModalComponent extends AbstractComponent {

    /**
     * 
     * @param {string|jQuery} element 
     */
    constructor(element) {
        super(element);
        console.log("#"+this.$element.attr("id"))
        this.bootstrapModal = new bootstrap.Modal("#"+this.$element.attr("id"), {keyboard: false})
        this.init();
    }

    /**
     * @override
     */
    init() {
    }

    show() {
        console.log("ModalComponent.show", this.bootstrapModal);
        this.bootstrapModal.show();
    }

    /**
     * @override
     */
    bindEvents() {
        /*
        this.bindEvent("click", this.buttonClicked, this.$button);
        this.bindEvent("click", this.itemClicked, this.$items);
        
        // Hide the dropdown when clicked outside
        // Only bind if it's not already bound
        if (!jQuery._data(document, ".kebabClickOutside")) {
            jQuery(document).on("click.kebabClickOutside", this.handleClickOutside.bind(this));
        }
        */
    }

    /**
     * @override
     */
    render() {
        //this.$menu.toggle(this.state["open"]);
    }
    
}