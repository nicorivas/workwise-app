import AbstractComponent from "../abstractComponent.js";
import IconButtonComponent from "../iconButtonComponent/iconButton.js";

export default class HelpSidearComponent extends AbstractComponent {
    constructor(element) {
        super(element);
        console.log("HelpSidear.constructor()")
        this.state = {
            "open": false
        }
        this.init();
    }

    init() {
        console.log("HelpSidear.init()")
        this.setState(this.state);
        this.loadComponents();
    }

    loadComponents() {
        // Load components
        this.closeButton = new IconButtonComponent("#help-sidebar__close");
        this.bindEvents();
    }

    bindEvents() {
        this.closeButton.bindEvent("click", this.closeButtonHandler, null, this);
    }

    closeButtonHandler(view) {
        console.log("HelpSidear.closeButtonHandler()", view);
        view.setState({"open": false});
    }

    render() {
        console.log("HelpSidear.render()", this.state);
        if (this.state.open) {
            this.$element.addClass("help-sidebar--open");
        } else {
            this.$element.removeClass("help-sidebar--open");
        }
    }
}