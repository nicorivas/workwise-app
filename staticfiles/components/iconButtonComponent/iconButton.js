import AbstractComponent from "../abstractComponent.js";

export default class IconButtonComponent extends AbstractComponent {

    constructor(element, async = true) {
        super(element);
        // Default state
        this.state = {
            "status": "idle",
            "disabled": false,
            "selected": false,
        }
        // Others
        this.async = async;
        
        this.init();
    }

    init() {
        this.bindEvents();
    }

    bindEvents() {
        this.bindEvent("click", this.buttonClick);
    }

    click() {
        this.$element.click();
    }


    buttonClick(e) {
        // If button is disabled, don't do anything.
        if (this.state["disabled"]) return;
        
        // If button is running don't do anything on click.
        if (this.state["status"] == "running") return;

        this.setState({"status":"running"});
        this.callFunctions(e);
        if (!this.async) this.setState({"status":"idle"});
    }

    render() {
        if (this.state["status"] == "running") {
            this.$element.addClass("icon-button--running");
        } else if (this.state["status"] == "idle") {            
            this.$element.removeClass("icon-button--running");
        }

        this.$element.toggleClass("icon-button--selected", this.state["selected"] === true);
        this.$element.toggleClass("icon-button--disabled", this.state["disabled"] === true);
    }
    
}