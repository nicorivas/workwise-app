import AbstractComponent from '../abstractComponent.js';
import ButtonComponent from '../buttonComponent/button.js';
import TaskComponent from '../taskComponent/task.js';


/*
  Flow form consists of a Task Creation Form, and then the Task itself.
*/

export default class FlowFormComponent extends AbstractComponent {

    constructor(element, flow = null) {
        super(element);
        // Parent
        this.flow = flow;
        // Components
        this.task = null;
        // State
        this.state = {
            currentStep: 0,
            steps: jQuery(".step").map(function () { return `#${this.id}`; }).get(),
            currentInstruction: 0,
        };
    }

    init() {
        this.createComponents();
        this.bindEvents();
        this.render();
    }

    createComponents() {
        // Create task button, submission of first form
        this.createTaskButton = new ButtonComponent('#btn-create-task', true, false);
        
        // If we have a task, create component.
        if (jQuery("#task").length > 0 && jQuery("#task").data("id")) {
            this.loadTask(null);
        }

        // Step indicators, duplicate to the number of steps
        for (let i = 0; i < this.state.steps.length - 1; i++) {
            jQuery(".dots .dot:eq(0)").clone().appendTo(".dots");
        }
    }

    bindEvents() {
        this.createTaskButton.bindEvent('click', this.createTaskHandler, null, this);
    }

    render() {
        // Hide all steps
        jQuery(this.state.steps.join(', ')).hide();

        // Show the current step
        jQuery(this.state.steps[this.state.currentStep]).show();

        // Update step indicator
        jQuery('.step-indicator .dot').removeClass('active');
        jQuery(`.step-indicator .dot:eq(${this.state.currentStep})`).addClass('active');
    }

    destroy() {
        this.unbindEvent('click', '.next-btn');
    }

    // ------------------------------

    loadTask(html) {
        if (html != null) {
            jQuery("#task-container").html(html);
        }
        
        this.analyseButton = new ButtonComponent('.button.agent-call', true, false);
        this.analyseButton.bindEvent("click", this.nextStep, null, this);

        this.lastButton = new ButtonComponent('#btn-last', true, false);
        this.lastButton.bindEvent("click", this.nextStep, null, this);
        
        this.task = new TaskComponent(jQuery("#task"));
        this.task.openInstruction(0);
    }

    prevStep(component = null) {
        if (component == null) component = this;
        const prevStepIndex = component.state.currentStep - 1;
        if (prevStepIndex >= 0) {
            component.setState({ currentStep: prevStepIndex });
        }
    }

    nextStep(component = null) {
        if (component == null) component = this;
        const nextStepIndex = component.state.currentStep + 1;
        if (nextStepIndex < component.state.steps.length) {
            component.setState({ currentStep: nextStepIndex });
        }
    }

    prevInstruction(component = null) {
        if (component == null) component = this;
        const prevInstructionIndex = component.state.currentInstruction - 1;
        if (prevInstructionIndex >= 0) {
            component.setState({ currentInstruction: prevInstructionIndex });
        }
    }

    nextInstruction(component = null) {
        if (component == null) component = this;
        const nextInstructionIndex = component.state.currentInstruction + 1;
        if (nextInstructionIndex < component.instructions.length) {
            component.setState({ currentInstruction: nextInstructionIndex });
        }
    }

    createTaskHandler(view) {
        //view.createPitch(this);
        view.createTask(this);
    }

    createTask(button) {
        let dataForm = jQuery("#task-create").serializeArray();
        let dataFormJSON = {}
        jQuery.map(dataForm, function (n, i) {
            dataFormJSON[n['name']] = n['value'];
        });

        let data = [];
        data.push({ name: "csrfmiddlewaretoken", value: Cookies.get("csrftoken") });
        // User
        data.push({ name: "author_name", value: dataFormJSON["author_name"] });
        data.push({ name: "author_email", value: dataFormJSON["author_email"] });
        data.push({ name: "email", value: dataFormJSON["author_email"] });
        // Task
        data.push({ name: "project", value: this.flow.projectId });
        data.push({ name: "action", value: this.flow.actionId });

        jQuery.ajax({
            type: 'POST',
            url: "/flow/create_task/",
            data: data,
            success: (response) => {
                if (response.status == "error") {
                    for (let error in response.errors) {
                        let elementId = `#id_${error}`
                        let elementErrorId = `#id_${error}-error`
                        jQuery(elementId).addClass("is-invalid")
                        if ("This field is required." == response.errors[error]) {
                            jQuery(elementErrorId).find("p").text("Este campo no puede estar en blanco.");
                        } else if ("Enter a valid email address." == response.errors[error]) {
                            jQuery(elementErrorId).find("p").text("Por favor ingresa un correo válido.");
                        } else {
                            jQuery(elementErrorId).find("p").text(response.errors[error]);
                        }
                    }
                    button.setState({ "status": "idle" })
                } else {
                    this.loadTask(response);
                    this.nextStep();
                    button.setState({ "status": "idle" })
                    window.history.pushState("", "", `/flow/${this.flow.id}/task/${this.task.id}`);
                }
            },
            error: (xhr, status, error) => {
                // Handle AJAX errors
                for (let field in xhr.responseJSON) {
                    let elementId = `#id_${field}`
                    let elementErrorId = `#id_${field}-error`
                    jQuery(elementId).addClass("is-invalid")
                    if ("This field may not be blank." == xhr.responseJSON[field]) {
                        jQuery(elementErrorId).find("p").text("Este campo no puede estar en blanco.");
                    } else if ("Enter a valid email address." == xhr.responseJSON[field]) {
                        jQuery(elementErrorId).find("p").text("Por favor ingresa un correo válido.");
                    } else {
                        jQuery(elementErrorId).find("p").text(xhr.responseJSON[field]);
                    }
                    button.setState({ "status": "idle" })
                }
            }
        })
    }
}
