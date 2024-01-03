import AbstractComponent from '../abstractComponent.js';
import IconButtonComponent from '../iconButtonComponent/iconButton.js';

/**
 * Represents a sidebar component for main page
 * @class
 * @extends AbstractComponent
 */
export default class SidebarComponent extends AbstractComponent {

    /**
     * Creates an instance of SidebarComponent.
     * @constructor
     * @param {HTMLElement} element - The HTML element that represents the sidebar component.
     */
    constructor(element) {
        super(element);
        this.state;
        this.init();
    }

    /**
     * Initializes the sidebar component by loading its components.
     */
    init() {
        this.loadComponents();
    }

    /**
     * Loads the buttons of the sidebar, as IconButtonComponents.
     */
    loadComponents() {
        //this.buttonExplorer = new IconButtonComponent("#sidebar__explorer")
        this.buttonProjects = new IconButtonComponent("#sidebar__projects")
        this.buttonActions = new IconButtonComponent("#sidebar__actions")
        this.buttonFlows = new IconButtonComponent("#sidebar__flow")
        this.buttons = {
            //"explorer": this.buttonExplorer,
            "projects": this.buttonProjects,
            "actions": this.buttonActions,
            "flow": this.buttonFlows,
        }
        this.bindEvents();
    }

    /**
     * Binds events to the sidebar component.
     */
    bindEvents() {
        //this.bindEvent('click', this.nextStep, '.next-btn');
    }

    /**
     * Selects a button in the sidebar based on the given URL.
     * @param {string} url - The URL of the button to be selected.
     */
    select(url) {
        // Iterate over buttons and set selected false
        for (let button in this.buttons) {
            this.buttons[button].setState({"selected": false});
        }
        this.buttons[url].setState({"selected": true});
    }

    /**
     * Renders the sidebar component.
     */
    render() {
    }

    /**
     * Destroys the sidebar component.
     */
    destroy() {
        //
    }
}