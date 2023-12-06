import AbstractComponent from "../abstractComponent.js";

export default class ErrorMessage extends AbstractComponent {
    constructor(element) {
        super(element);
        this.state = {
            "init": true,
            "visible": false,
        }
        this.init();
    }

    init() {
        this.bindEvents();
        this.setState(this.state);
        setTimeout(() => {this.setState({"init":false});}, 3000);
    }

    bindEvents() {
        this.$element.find(".error-message__close").on("click", this.close, this);
    }

    close() {
        this.setState({"visible":false});
    }

    show(error) {
        this.$element.find(".error-message__text").text(error);
        this.setState({"visible":true});
        setTimeout(() => {this.close();}, 3000);
    }

    render() {
        if (!this.state["init"]) {
            this.$element.toggleClass("error-message--fade-in", this.state["visible"])
            this.$element.toggleClass("error-message--fade-out", !this.state["visible"])
        }
    }
    
}