import AbstractView from '../abstractView.js';
import TableComponent from '../../components/tableComponent/table.js';

export default class ActionsView extends AbstractView {
    
    constructor(element) {
        super(element)
        this.init();
    }

    init() {
        this.actionsTable = new TableComponent("#actions-table", "/actions/")
    }
    
    /**
     * @override
     */
    bindEvents() {
    }

    createAction(sourceView, event) {
        // Handle the creation of a new project.
        // Creates a task though a POST request to the server.
        // Then closes the modal.
        console.log("create project", this, sourceView, event);
        event.preventDefault();
        console.log("create project");

        let data = jQuery("#create-project-form").serializeArray();
        data.push({"name":"description", "value":"Sample"});
        console.log(data);
        jQuery.ajax({
            type: 'POST',
            url: "/api/project/",
            data: data,
            success: function (itemData) {
                jQuery("#create-project-modal").modal('hide');
                let item = sourceView.projectsList.newItem(itemData.name, itemData.id);
                sourceView.bindEvents();
                item.$element.click();
            },
            error: function (xhr, status, error) {
                // Handle AJAX errors
                console.log(xhr);
                console.log(status);
                console.log(error);
            }
        })
    }
}