import AbstractView from '../abstractView.js';
import ButtonComponent from '../../components/buttonComponent/button.js';

export default class PromptView extends AbstractView {
    
    /**
     * @override
     */
    constructor(element, id=null, parentView=null) {
        super(element)
        this.id = id;
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
        this.saveButton = new ButtonComponent("#prompt-save-btn");
    }
    
    /**
     * @override
     */
    bindEvents() {
        /**/
        this.saveButton.bindEvent("click", this.saveHandler, null, this)
    }

    saveHandler(view) {
        console.log("PromptsView:saveHandler", view);
        jQuery.ajax({
            type: 'PATCH',
            url: `/api/prompt/${view.id}/`,
            contentType: 'application/json',
            data: JSON.stringify({
                "prompt": view.$element.find("#prompt-text").val()
            }),
            success: (response) => {
                console.log("success", response);
            },
            beforeSend: function(xhr) {
                // Include the CSRF token as a header
                xhr.setRequestHeader("X-CSRFToken", Cookies.get("csrftoken"));
            },
            error: (xhr, status, error) => {
                // Handle AJAX errors
                console.log(xhr);
                console.log(status);
                console.log(error);
            }
        })
    }

    fetch(url) {
        /* Fetch data */
    }

    createAction(view) {
    }
}