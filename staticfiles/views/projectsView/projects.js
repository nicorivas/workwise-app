import AbstractView from '../abstractView.js';
import ProjectView from '../projectView/project.js';
import ListComponent from '../../components/listComponent/list.js';
import ModalComponent from '../../components/modalComponent/modal.js';

export default class ProjectsView extends AbstractView {
    
    constructor(element) {
        super(element)

        this.projectView; // Project view
        this.projectsList; // ListComponent of projects
        this.init();
    }

    init() {
        // Projects list component.
        this.projectsList = new ListComponent("#projects-list");

        // Modal to create new projects
        this.createProjectModal = new ModalComponent("#create-project-modal");
        this.createProjectModal.bindEvent("click", this.createProject, ".modal__action-button", this);

        // Bind events
        this.bindEvents();

        // Load project. If id was given then load it, else load the first of the list.
        let projectId;
        if (this.$element.data("project")) {
            projectId = this.$element.data("project");
        } else {
            projectId = this.projectsList.items[0].state["id"];
        }
        this.projectsList.clickItemById(projectId);
    }
    
    /**
     * @override
     */
    bindEvents() {
        // Bind events of list items clicked.
        for (const item of this.projectsList.items) {
            item.bindEvent("click", this.listItemClicked, null, this, true);
        }
    }

    listItemClicked(projectsView, fetch=false, event) {
        /*
        *   This function is called when a list item is clicked.
        *   Args:
        *       projectView: this.
        *       fetch: if true, fetch the project data.
        *       event: the event.
        */
        console.log("ProjectsView.listItemClicked()", this, projectsView, fetch, event);
        projectsView.projectsList.selectItem(this);
        if (fetch) {
            this.projectView = new ProjectView("#project", projectsView, this.state["id"]);
            history.pushState({ page: "project" }, "", `/projects/${this.state["id"]}`);
        }
    }

    createProject(sourceView, event) {
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