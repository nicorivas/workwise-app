import AbstractComponent from "../abstractComponent.js";

export default class IconButtonComponent extends AbstractComponent {

    constructor(element, async = true, selectable = false) {
        super(element);
        // Default state
        this.state = {
            "status": "idle",
            "disabled": false,
            "selected": false,
        }
        // Others
        this.async = async;
        this.selectable = selectable;
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
        console.log("IconButtonComponent.buttonClick()", e, this, this.state, this.async, this.selectable);
        // If button is disabled, don't do anything.
        if (this.state["disabled"]) return;
        
        // If button is running don't do anything on click.
        if (this.state["status"] == "running") return;

        let state = {"status": "running"};
        if (this.selectable) {
            state["selected"] = !this.state["selected"];
        }
        this.setState(state);
        console.log(this.state);

        this.callFunctions(e);
        if (!this.async) this.setState({"status":"idle"});
    }

    render() {
        console.log("IconButtonComponent.render()", this.state);
        if (this.state["status"] == "running") {
            this.$element.addClass("icon-button--running");
        } else if (this.state["status"] == "idle") {            
            this.$element.removeClass("icon-button--running");
        }

        this.$element.toggleClass("icon-button--selected", this.state["selected"] === true);
        this.$element.toggleClass("icon-button--disabled", this.state["disabled"] === true);
    }
    
}