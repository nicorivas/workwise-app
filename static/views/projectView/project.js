import AbstractView from '../abstractView.js';
import TableComponent from '../../components/tableComponent/table.js';
import KebabComponent from '../../components/kebabComponent/kebab.js';
import IconButtonComponent from '../../components/iconButtonComponent/iconButton.js';
import ModalComponent from '../../components/modalComponent/modal.js';
import RadioButtonsComponent from '../../components/radioButtonsComponent/radioButtons.js';

export default class ProjectView extends AbstractView {
    
    constructor(element, view, id=null) {
        super(element);
        console.log("ProjectView.constructor()", this, element, view, id);
        this.parentView = view;
        this.projectsDropdown;
        this.contextTable;
        this.tasksTable;
        this.id = id;
        this.init();
    }

    init() {
        console.log("ProjectView.init()", this.parentView);
        if (this.id) this.load(this.id);
    }

    load(id) {
        this.setData({"id":id});
    }

    loadComponents() {
        this.projectsKebab = new KebabComponent("#project-kebab");
        this.projectsKebab.addItem("Delete");
        
        // Context table
        this.contextTable = new TableComponent("#project-context-table", "/context/")
        this.contextTableAddButton = new IconButtonComponent("#context__add-document");

        // Add document modal
        this.contextAddDocumentModal = new ModalComponent("#add-document-modal");
        this.contextAddDocumentModal.$element.find("#add-document-modal__form-create").hide();

        // Document sources
        this.contextAddDocumentModalTypes = new RadioButtonsComponent(".document-sources");
        this.contextAddDocumentModalTypes.addOption("document-type-blank", "Blank document");
        this.contextAddDocumentModalTypes.addOption("document-type-google-docs", "Google Docs");
        this.contextAddDocumentModalTypes.addOption("document-type-google-docs", "Word");
        this.contextAddDocumentModalTypes.addOption("document-type-google-docs", "Website");
        this.contextAddDocumentModalTypes.addOption("document-type-google-docs", "Email");
        this.contextAddDocumentModalTypes.addOption("document-type-google-docs", "Notion");

        // Tasks table
        this.tasksTable = new TableComponent("#project-tasks-table", "/task/")
        this.tasksTableAddButton = new IconButtonComponent("#project-tasks-table .table__header__actions .icon-button");

        // Add task modal
        this.tasksAddTaskModal = new ModalComponent("#create-task-modal");

        this.bindEvents();
    }

    bindEvents() {
        console.log("ProjectView.bindEvents");

        // Show Modals
        this.contextTableAddButton.addFunction(() => {this.contextAddDocumentModal.show()});
        this.tasksTableAddButton.addFunction(() => {this.tasksAddTaskModal.show()});

        // Create blank document
        this.contextAddDocumentModal.bindEvent("click", this.clickDocumentTypeHandler, "#document-type-blank .button", this);
        this.contextAddDocumentModal.bindEvent("click", this.addDocumentHandler, "#add-document-modal__footer__save-button", this);

        // Remove document
        for (const kebab of this.contextTable.kebabs) {
            kebab.bindEvent("click", this.removeDocument, "#remove", this);
            kebab.bindEvent("click", this.deleteDocument, "#delete", this);
        }

        // Remove task
        for (const kebab of this.tasksTable.kebabs) {
            kebab.bindEvent("click", this.deleteTask, "#remove", this);
            kebab.bindEvent("click", this.deleteTask, "#delete", this);
        }

        // Bind events to the kebab menu.
        this.projectsKebab.bindEvent("click", this.deleteProject, "#delete", this);
        
        // While title is being modified, also modify the element of the list.
        jQuery(".title-input").on("input", (event) => {
            let id = this.data.id;
            let val = jQuery(event.target).val();
            this.parentView.projectsList.renameItem(id, val);
            jQuery.ajax({
                url: `/api/project/${id}/`,
                method: "PATCH",
                data: {
                    "name": val,
                },
                success: (data) => {
                    //console.log("ListComponent.fetch() success", data);
                },
                error: (error) => {
                    //console.log("ListComponent.fetch() error", error);
                },
                complete: () => {
                    //
                }
            })
        });
    }

    clickDocumentTypeHandler(event) {
        console.log("ProjectView.clickDocumentTypeHandler", this, event);
        this.$element.find(".add-document-modal__form__create").hide();
        this.$element.find("#add-document-modal__form__create__blank-document").show();
    }

    addDocumentHandler(projectView, event) {
        let modalComponent = this;
        console.log("ProjectView.addDocumentHandler", this, projectView, event);
        let data = jQuery("#add-document-modal__form").serializeArray()
        data["csrfmiddlewaretoken"] = Cookies.get("csrftoken");
        jQuery.ajax({
            url: `/api/document/`,
            method: "POST",
            data: data,
            success: (data) => {
                console.log("Success document created", projectView.data.id);
                projectView.contextTable.fetch(projectView.data.id);
            },
            error: (error) => {
                //console.log("ListComponent.fetch() error", error);
            },
            complete: () => {
                jQuery("#project-indicator").hide();
                projectView.$element.show();
            }
        
        })
    }

    deleteProject(projectView, event) {
        console.log("ProjectView.deleteProject()", this, projectView, event);
        projectView.parentView.projectsList.removeItem(projectView.data.id);
        
        // Delete. TODO This should be an API call, not an AJAX request.
        jQuery.ajax({
            url: `/api/project/${projectView.data.id}/`,
            method: "DELETE",
            data: {
                "csrfmiddlewaretoken": Cookies.get("csrftoken"),
            },
            success: (data) => {
                //console.log("ListComponent.fetch() success", data);
            },
            error: (error) => {
                //console.log("ListComponent.fetch() error", error);
            },
            complete: () => {
                //
            }
        });
        
    }

    removeDocument(projectView, event) {
        console.log("ProjectView.removeDocument()", this, projectView, event);

        const id = this.$element.data("element-id");
        if (!id) {
            throw new Error("removeDocument(): id is undefined");
        }
        jQuery.ajax({
            url: `/api/document/${id}/`,
            method: "PATCH",
            data: {
                "project": null,
            },
            success: (data) => {
                projectView.contextTable.fetch(projectView.data.id);
            },
            error: (jqXhr, textStatus, errorThrown) => {
            },
            complete: () => {
            }
        
        })

    }

    deleteDocument(projectView, event) {
        console.log("ProjectView.deleteDocument()", this, projectView, event);
        const id = this.$element.data("element-id");
        if (!id) {
            throw new Error("deleteDocument(): id is undefined");
        }
        jQuery.ajax({
            url: `/api/document/${id}/`,
            method: "DELETE",
            success: (data) => {
                projectView.contextTable.fetch(projectView.data.id);
            },
            error: (jqXhr, textStatus, errorThrown) => {
                console.log(jqXhr, textStatus, errorThrown)
            },
            complete: () => {
                //
            }
        
        })
    }

    deleteTask(projectView, event) {
        // Delete a task
        // this: task.
        console.log("ProjectView.deleteTask()", this, projectView, event);
        const id = this.$element.data("element-id");
        if (!id) {
            throw new Error("deleteTask(): id is undefined");
        }
        // Delete row from table
        projectView.tasksTable.table.rows(`[data-id=${id}]`).remove().draw();
        // Delete row from DB
        axios.delete(`/api/task/${id}/`).catch((error) => {
            console.log(error);
            projectView.showError("Error deleting task");
        }).then((response) => {
            console.log(response);
        })
        /*
        jQuery.ajax({
            url: `/api/task/${id}/`,
            method: "DELETE",
            success: (data) => {
                //
            },
            error: (jqXhr, textStatus, errorThrown) => {
                console.log(jqXhr, textStatus, errorThrown)
            },
            complete: () => {
                //
            }
        
        })
        */
    }

    render() {
        console.log("ProjectView.render()", this.data);
        if (!this.data.id) {
            throw new Error("ProjectView.fetchProject(): id is undefined");
        }
        jQuery("#project-indicator").addClass("project-indicator--visible");
        this.$element.hide();
        jQuery.ajax({
            url: `/projects/${this.data.id}`,
            method: "GET",
            data: {"source":"menu"},
            success: (data) => {
                this.$element.html(data);
            },
            error: (error) => {
                /**/
            },
            complete: () => {
                jQuery("#project-indicator").removeClass("project-indicator--visible");
                this.$element.show();
                this.loadComponents();
            }
        });
    }
}