import AbstractComponent from "../abstractComponent.js";
import ButtonComponent from "../buttonComponent/button.js";
import IconButtonComponent from "../iconButtonComponent/iconButton.js";
import LLM from "../../js/llm.js";

/*
    Element that contains the feedback given to a specific instruction element,
    usually used for displaying streaming text next to Text Inputs in Forms (Flows).
*/
export default class InstructionElementFeedback extends AbstractComponent {

    constructor(element, instructionElement = null) {
        super(element);
        // Elements
        this.loadElements();
        this.openButton = null;
        this.closeButton = null;
        this.readMoreButton = null;
        this.llm = new LLM();
        // Parent
        this.instructionElement = instructionElement;
        // Define state
        this.state = {
            "id": this.$element.data("id"),
            "status": "idle",
            "visible": this.$feedback.hasClass("instruction-element-feedback--visible"),
            "open": true,
            "large": false,
            "title": this.$title.text(),
        };
        this.init();
    }

    init() {
        console.log("InstructionElementFeedback.init()", this.$element);
        this.load();
    }

    loadElements() {
        // We use loadElements, as we need to reload them when updating the html.
        this.$feedback = this.$element.find(".instruction-element-feedback");
        this.$header = this.$element.find(".instruction-element-feedback__header");
        this.$title = this.$element.find(".instruction-element-feedback__header__title");
        this.$body = this.$element.find(".instruction-element-feedback__body");
        this.$text = this.$element.find(".instruction-element-feedback__body__text");
        this.$footer = this.$element.find(".instruction-element-feedback__footer");
        this.$openButton = this.$element.find("#instruction-element-feedback__open");
        this.$closeButton = this.$element.find(".instruction-element-feedback__header__close");
        this.$overlay = this.$element.find(".instruction-element-feedback-overlay");
        this.$readMoreButton = this.$element.find("#read-more-button");
        this.$indicator = this.$element.find(".instruction-element-feedback__body__text--indicator");        
    }

    createComponents() {
        console.log("InstructionElementFeedback.createComponents()");
        this.openButton = new IconButtonComponent(this.$openButton, false, true);
        this.closeButton = new ButtonComponent(this.$closeButton, false, false);
        this.readMoreButton = new ButtonComponent(this.$readMoreButton, false, false);
    }

    bindEvents() {
        console.log("InstructionElementFeedback.bindEvents()");
        this.openButton.bindEvent("click", this.openButtonHandler, null, this);
        this.closeButton.bindEvent("click", this.closeButtonHandler, null, this);
        this.readMoreButton.bindEvent("click", this.readMoreHandler, null, this);
    }

    render() {
        if (this.state["status"] == "loading") {
            this.$indicator.show();
            this.$text.hide();
        } else {
            this.$indicator.hide();
            this.$text.show();
        }

        // Open or closed
        if (this.state["open"]) {
            this.$body.show();
        } else {
            this.$body.hide();
        }

        // Visible
        this.$feedback.toggleClass("instruction-element-feedback--visible", this.state["visible"]);

        // Loading
        this.$openButton.toggleClass("instruction-element-feedback--loading", this.state["status"] == "loading");

        // Selected
        this.$feedback.toggleClass("instruction-element-feedback--selected", this.state["selected"]);

        // Large
        this.$feedback.toggleClass("instruction-element-feedback--large", this.state["large"]);
        this.$overlay.toggleClass("instruction-element-feedback-overlay--visible", this.state["large"]);
        this.$footer.toggle(!this.state["large"]);

        // Title
        this.$title.text(this.state["title"])

        // ID
        this.$element.attr("data-id", this.state["id"])
    }

    openButtonHandler(component) {
        /**
         * This handler is called when the user clicks on the open button.
         * 
         * It toggles the visibility of the feedback.
         * 
         * @param {object} component: the component that triggered the event.
        */
        // We scroll to top, as in the 'large' view we could've scrolled down.
        component.$body.scrollTop(0);
        component.setState({"visible": !component.state.visible});
    }

    closeButtonHandler(component) {
        /** 
         * This handler is called when the user clicks on the close button.
         * 
         * It closes the feedback.
         * 
         * @param {object} component: the component that triggered the event.
        */
        console.log("InstructionElementFeedback.closeButtonHandler()", component, this);
        component.openButton.click();
        if (component.state["large"]) {
            component.setState({"large": false});
        }
    }

    readMoreHandler(component) {
        /**
         * This handler is called when the user clicks on the read more button.
         * 
         * It opens the feedback in a large view.
         * 
         * @param {object} component: the component that triggered the event.
         */
        component.setState({"large": true});
    }

    load() {
        /**
         * This function loads the feedback from the server.
         * 
         * It is called when the component is initialized.
         * 1. It sets the state to loading, to show the loading indicator.
         * 2. It makes an AJAX call to the server to get the feedback.
         * 3. It replaces the whole element html.
         * 4. It loads the elements, creates components, and bind events again.
         * 5. Status is set back to idle.
         */
        this.setState({"status": "loading"})
        // If instruction does not exist, it creates it. This is the case for new tasks.
        jQuery.ajax({
            url: `/instruction/${this.instructionElement.instruction.id}/element/${this.instructionElement.id}/feedback`,
            type: "GET",
            success: (data) => {
                console.log("InstructionElementFeedback.load(): success", data);
                this.$element.html(data);
                this.loadElements();
                this.createComponents();
                this.bindEvents();
                this.setState({"status": "idle"})
            },
            error: (data) => {
                console.log("InstructionElementRevisionComponent.load(): error", data);
            }
        });
    }

    update_text(text) {
        /**
         * This function updates the feedback text in the server.
         * 
         * It is called when the feedback finished streaming.
         * 
         * @param {string} text: the text to update.
         */
        let data = {
            "text": text,
            "csrfmiddlewaretoken": Cookies.get('csrftoken')
        }
        jQuery.ajax({
            url: `/instruction/${this.instructionElement.instruction.id}/element/${this.instructionElement.id}/feedback`,
            type: "POST",
            data: data,
            success: (data) => {
                console.log("InstructionElementFeedback.update_text(): success", data);
            },
            error: (data) => {
                console.log("InstructionElementRevisionComponent.update_text(): error", data);
            }
        });
    }

    call() {
        /**
         * This function begins the feedback streaming from the LLM answer.
         * 
         * It is called when the user looses focus on the text element.
         * It uses the LLM class to stream the answer from the server to a specific element.
         * Promise of LLM is resolved when the streaming is finished.
         */
        this.setState({"status": "loading"})
        let url = `/instruction/${this.instructionElement.instruction.id}/element/${this.instructionElement.id}/feedback_call`;
        let id = this.instructionElement.id
        this.instructionElement.instruction.save().then((data) => {
            this.llm.stream(url, `instruction-text-${id}`, `instruction-element-feedback-${id}__body__text`, null, this).then((data) => {
                this.update_text(data);
                this.setState({
                    "status": "idle"
                })
            });
        })
    }

}