import AbstractComponent from "../abstractComponent.js";

/**
 * Button component.
 * @class
 */
export default class ButtonComponent extends AbstractComponent {

    /**
     * 
     * @param {string|jQuery} element 
     */
    constructor(element, async = true) {
        super(element);
        // Elements
        this.$button = this.$element.find(".button");
        this.$loader = this.$element.find(".button__loader");
        this.selectable = true;
        this.async = async;
        // Default state
        this.state = {
            "status": "idle",
            "selected": false
        }
        // Others
        this.init();
    }

    /**
     * @override
     */
    init() {
        this.bindEvents();
    }

    /**
     * @override
     */
    bindEvents() {
        this.bindEvent("click", this.buttonClick);
    }


    buttonClick(e) {
        // If button is selectable change state
        if (this.selectable) this.setState({"selected": !this.state["selected"]});

        // If button is running don't do anything on click.
        if (this.state["status"] == "running") return;

        this.setState({"status":"running"});
        this.callFunctions(e);
        if (!this.async) {
            this.setState({"status":"idle"});
        }
    }

    setId(id) {
        this.$element.attr("id", id);
    }

    setLabel(label) {
        this.$element.find(".button__text").text(label);
    }

    

    /**
     * @override
     */
    render() {
        if (this.state["status"] == "running") {
            this.$button.addClass("button--running");
            this.$loader.show();
        } else if (this.state["status"] == "disabled") {
            this.$button.addClass("button--disabled");
            this.$loader.show();
        } else if (this.state["status"] == "idle") {
            this.$button.removeClass("button--disabled");
            this.$button.removeClass("button--running");
            this.$loader.hide();
        }

        this.$button.toggleClass("button--selected", this.state["selected"]);
    }
    
}