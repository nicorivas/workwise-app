import AbstractView from '../abstractView.js';
import PromptsView from '../promptsView/prompts.js';
import TabsComponent from '../../components/tabsComponent/tabs.js';

export default class ActionView extends AbstractView {
    
    constructor(element, id=null) {
        super(element)
        this.id = id;
        this.init();
    }

    init() {
        this.actionTabs = new TabsComponent("#action-tabs")
        this.bindEvents();
    }
    
    /**
     * @override
     */
    bindEvents() {
        /**/
        this.actionTabs.tabs[0].bindEvent("click", this.tabHandler, null, this)
    }

    tabHandler(view) {
        console.log("tabHandler", view);
        view.fetch(`/actions/${view.id}/prompts`)
    }

    fetch(url) {
        /* Fetch data */
        console.log("fetch", url);
        jQuery.ajax({
            type: 'GET',
            url: url,
            success: (html) => {
                this.$element.find("#action-main").html(html);
                let promptsView = new PromptsView("#prompts", this);
            },
            error: (xhr, status, error) => {
                // Handle AJAX errors
                console.log(xhr);
                console.log(status);
                console.log(error);
            }
        })
    }

    createAction(view) {
    }
}