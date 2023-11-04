import {projectsView} from './projects.js';
import DropdownComponent from './dropdown.js';

export default class ContextView {
    
    constructor() {
        this.$element;
        this.$documents;
        this.documentsDropdowns = [];
        this.project_id;
    }

    load(element) {
        console.log("ContextView.load");

        this.$element = jQuery(element);
        this.$documents = this.$element.find(".project-document")
        this.project_id = this.$element.find(".project").first().data("id");
        this.init();
    }

    init() {
        console.log("ContextView.init");

        for (const $document of this.$documents) {
            this.documentsDropdowns.push(new DropdownComponent(jQuery($document)));
        }
        this.bindEvents();
    }

    bindEvents() {
        console.log("ContextView.bindEvents");

        for (const dropdown of this.documentsDropdowns) {
            // On click of the delete button, remove the project from the list
            // We use lambda to keep the context of 'this'
            dropdown.$element.find("#dropdown-item-delete").click(() => {
                dropdown.$element.remove();
            });
        }
        
    }
}

let contextView = new ContextView();
export { contextView }