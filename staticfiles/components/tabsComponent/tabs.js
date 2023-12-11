import AbstractComponent from "../abstractComponent.js";
import TabComponent from "../tabComponent/tab.js";

/**
 * Tabs component.
 * 
 * @extends AbstractComponent
 * @class
 */
export default class TabsComponent extends AbstractComponent {

    /**
     * 
     * @param {string|jQuery} element 
     */
    constructor(element, tabs=null) {
        super(element);
        this.tabs = []
        this.state = {
            "selected_tab": null,
            "tabs": tabs
        };
        this.init();
    }

    /**
     * @override
     */
    init() {
        console.log("TabsComponent init", this.tabs);
        this.createComponents();
    }

    createComponents() {
        /* Create components */
        for (let tab of jQuery(this.$element).find(".tabs__tab")) {
            let tabComponent = new TabComponent(jQuery(tab));
            this.tabs.push(tabComponent);
        }
        this.bindEvents();
    }

    /**
     * @override
     */
    bindEvents() {
        /* Handled by DataTables */
        for (let tab of this.tabs) {
            tab.bindEvent("click", this.selectTabHandler, null, this);
        }
    }



    fetch() {
        /* Fetch data */
    }

    selectTabHandler(component, event) {
        /* Select tab */
        console.log("selectTabHandler", component, event, this);
        for (let tab of component.tabs) {
            tab.setState({"selected": false});
        }
        this.setState({"selected": true});
    }

    /**
     * @override
     */
    render() {
        /* Render */
        for (let tab of this.tabs) {
            tab.setState({"selected": false});
            jQuery(tab).find(".tabs__tab__link").removeClass("active");
        }
        this.tabs[this.state.selected_tab].setState({"selected": true});
    }
    
}