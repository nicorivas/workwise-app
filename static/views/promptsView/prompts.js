import AbstractView from '../abstractView.js';
import PromptView from '../promptView/prompt.js';
import SelectorComponent from '../../components/selectorComponent/selector.js';
import ButtonComponent from '../../components/buttonComponent/button.js';

export default class PromptsView extends AbstractView {
    
    /**
     * @override
     */
    constructor(element, parentView=null) {
        super(element)
        this.parentView = parentView;
        this.init();
    }

    /**
     * @override
     */
    init() {
        this.createComponents();
        this.bindEvents();
    }

    createComponents() {
        /* */
        this.promptsSelector = new SelectorComponent("#selector-prompts");
        this.promptsSelector.addFunction(this.selectPrompt, [this]);

        this.createPromptButton = new ButtonComponent("#prompts__add-prompt");
        this.createPromptButton.bindEvent("click", this.createPrompt, null, this);
    }

    selectPrompt(view, $item) {
        console.log("selectPrompt", view, $item);
        view.fetch($item.data("id"));
    }

    createPrompt(view) {
        console.log("createPrompt", view, view.parentView.id);
        jQuery.ajax({
            type: 'POST',
            data: {
                "action": view.parentView.id,
                "csrfmiddlewaretoken": Cookies.get('csrftoken'),
            },
            url: '/prompt/create/',
            success: (html) => {
                view.$element.html(html);
            },
            error: (xhr, status, error) => {
                // Handle AJAX errors
                console.log(xhr);
                console.log(status);
                console.log(error);
            }
        })
    }
    
    /**
     * @override
     */
    bindEvents() {
        /* */
    }

    fetch(id) {
        /* Fetch data */
        console.log("PromptsView:fetch", id);
        jQuery.ajax({
            type: 'GET',
            url: `/prompt/${id}`,
            success: (html) => {
                console.log(html);
                this.$element.find("#prompt__wrapper").html(html);
                let promptView = new PromptView("#prompt", id, this);
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