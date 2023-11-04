import AbstractComponent from "../abstractComponent.js";

export default class ErrorMessage extends AbstractComponent {
    constructor(element) {
        super(element);
        this.init();
        this.state = {
            "visible": false,
        }
    }

    init() {
        console.log("ErrorMessage.init()");
        this.bindEvents();
        this.setState(this.state);
    }

    bindEvents() {
        this.$element.find(".error-message__close").on("click", this.close, this);
    }

    close() {
        this.setState({"visible":false});
    }

    show(error) {
        console.log("ErrorMessage.show()", error);
        this.$element.find(".error-message__text").text(error);
        this.setState({"visible":true});
        setTimeout(() => {this.close();}, 3000);
    }

    render() {
        /*
        if (this.state["visible"]) {
            this.$element.show();
        } else {
            this.$element.hide();
        }
        */
        this.$element.toggleClass("error-message--fade-in", this.state["visible"])
        this.$element.toggleClass("error-message--fade-out", !this.state["visible"])
    }
    
}