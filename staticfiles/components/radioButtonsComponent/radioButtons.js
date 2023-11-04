import AbstractComponent from "../abstractComponent.js";
import ButtonComponent from "../buttonComponent/button.js";

/**
 * Radio buttons component.
 * @class
 */
export default class RadioButtonsComponent extends AbstractComponent {

    /**
     * 
     * @param {string|jQuery} element 
     */
    constructor(element, async = true) {
        super(element);
        // Elements
        this.$buttonTemplate = this.$element.find(".radio-buttons__button--template");
        this.$buttons = this.$element.find(".button-container");
        this.buttons = [];
        this.init();
    }

    /**
     * @override
     */
    init() {
        console.log("RadioButtonsComponent.init()", this.$element);
        // Create button components
        this.$buttons.each((i, button) => {
            this.buttons.push(new ButtonComponent(jQuery(button), false));
        });
        this.bindEvents();
    }

    /**
     * @override
     */
    bindEvents() {
        console.log("RadioButtonsComponent.bindEvents()");
        for (const button of this.buttons) {
            this.bindEventButton(button);
        };
    }

    bindEventButton(button) {
        console.log("RadioButtonsComponent.bindEventButton()");
        button.bindEvent("click", this.buttonClick, null, this);
    }


    buttonClick(radioButtons, event) {
        console.log("RadioButtonsComponent.buttonClick()", this, radioButtons, event);
        // Deselect all buttons
        for (const button of radioButtons.buttons) {
            if (button !== this) button.setState({"selected": false});
        }
    }

    addOption(id, label) {
        console.log("RadioButtonsComponent.addOption()");
        
        // Create button element
        let $button = this.$buttonTemplate.clone().removeClass("radio-buttons__button--template").appendTo(this.$element);
        $button.find(".radio-buttons__button__input").attr("value", this.$buttons.length);
        let button_id = $button.find(".radio-buttons__button__input").attr("name")+"-"+this.$buttons.length
        $button.find(".radio-buttons__button__input").attr("id", button_id);
        $button.find(".radio-buttons__button__label").attr("for", button_id);
        this.$buttons = this.$element.find(".button-container");

        // Create button component
        let button = new ButtonComponent($button.find(".button-container"), false);
        this.bindEventButton(button);
        button.setId(id);
        button.setLabel(label);
        this.buttons.push(button);
    }

    /**
     * @override
     */
    render() {
        console.log("RadioButtonsComponent.render()");
    }
    
}