import AbstractComponent from '../abstractComponent.js';
import IconButtonComponent from '../iconButtonComponent/iconButton.js';

export default class FlowFormComponent extends AbstractComponent {

    constructor(element) {
        super(element);
        this.state;
        this.init();
    }

    init() {
        this.loadComponents();
    }

    loadComponents() {
        this.buttonExplorer = new IconButtonComponent("#sidebar__explorer")
        this.buttonProjects = new IconButtonComponent("#sidebar__projects")
        this.buttonActions = new IconButtonComponent("#sidebar__actions")
        this.buttons = {
            "explorer": this.buttonExplorer,
            "projects": this.buttonProjects,
            "actions": this.buttonActions
        }
        this.bindEvents();
    }

    bindEvents() {
        //this.bindEvent('click', this.nextStep, '.next-btn');
    }

    select(url) {
        // Iterate over buttons and set selected false
        for (let button in this.buttons) {
            this.buttons[button].setState({"selected": false});
        }
        this.buttons[url].setState({"selected": true});
    }

    render() {
    }

    destroy() {
        //
    }
}