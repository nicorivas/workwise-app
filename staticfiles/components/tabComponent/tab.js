import AbstractComponent from "../abstractComponent.js";

/**
 * Tabs component.
 * 
 * @extends AbstractComponent
 * @class
 */
export default class TabComponent extends AbstractComponent {

    /**
     * 
     * @param {string|jQuery} element 
     */
    constructor(element) {
        super(element);
        this.state = {
            "selected": false,
        };
        this.init();
    }

    /**
     * @override
     */
    init() {
        console.log("TabComponent:init()");
        this.bindEvents();
        this.setState(this.state);
    }

    /**
     * @override
     */
    bindEvents() {
        console.log("TabComponent:bindEvents()");
    }

    /**
     * @override
     */
    render() {
        this.$element.find(".tabs__tab__link").toggleClass("active", this.state.selected);
    }
    
}