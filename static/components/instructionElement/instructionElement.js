import AbstractComponent from "../abstractComponent.js";

export default class InstructionElement extends AbstractComponent {

    constructor(element, instruction = null, view = null) {
        super(element);
        this.id = this.$element.data("id");
        this.type = this.$element.data("type");
        // Parent
        this.instruction = instruction;
        this.$header = jQuery(".instruction-element__header");
        this.$title = jQuery(".instruction-element__header__title");
        this.$body = jQuery(".instruction-element__body");
        this.$footer = jQuery(".instruction-element__footer");
        this.state = {
            "header_hidden": false,
            "body_hidden": false,
            "footer_hidden": false,
        }
    }

    init() {
        this.createComponents();
        this.bindEvents();
    }

    createComponents() {
        /* */
    }

    bindEvents() {
        /* */
    }

    render() {
        // Propagate change of state to button
        this.$header.toggleClass("hidden", this.state.header_hidden);
        this.$body.toggleClass("hidden", this.state.body_hidden);
        this.$footer.toggleClass("hidden", this.state.footer_hidden);
    }
    
    destroy() {
        /* */
    }

    /* -- */

    value() {
        if (this.type == "TXT") {
            return this.textField.val();
        }
    }
}