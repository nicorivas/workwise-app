import {projectsView} from './projects.js';
import DropdownComponent from './dropdown.js';

export default class TasksView {
    
    constructor() {
        this.$element;
        this.$tasks;
        this.tasksDropdowns = [];
        this.project_id;
    }

    load(element) {
        console.log("TasksView.load");

        this.$element = jQuery(element);
        this.$tasks = this.$element.find(".project-task")
        this.project_id = this.$element.find(".project").first().data("id");
        this.init();
    }

    init() {
        console.log("TasksView.init");

        for (const $task of this.$tasks) {
            this.tasksDropdowns.push(new DropdownComponent(jQuery($task)));
        }
        this.bindEvents();
    }

    bindEvents() {
        console.log("TasksView.bindEvents");

        for (const dropdown of this.tasksDropdowns) {
            // On click of the delete button, remove the project from the list
            // We use lambda to keep the context of 'this'
            dropdown.$element.find("#dropdown-item-delete").click(() => {
                console.log("#dropdown-item-delete", dropdown.task_id);
                dropdown.$element.remove();
            });
        }
        
    }
}

let tasksView = new TasksView();
export { tasksView }