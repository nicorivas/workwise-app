import AbstractComponent from "../abstractComponent.js";
import IconButtonComponent from "../iconButtonComponent/iconButton.js";

export default class InstructionSidebarComponent extends AbstractComponent {
    
    constructor(element, task) {
        super(element)
        // Components
        this.buttons = []
        // Daddy
        this.task = task;
        // Define state
        this.state = {
            "open": false,
            "feedbackPossible": false,
        }
        this.load(element, task);
    }

    load(element, task) {
        this.init();
    }

    init() {
        // Icon buttons
        this.$element.find(".vertical-toolbar .icon-button").each((index, $button) => {
            let buttonComponent = new IconButtonComponent(jQuery($button))
            buttonComponent.$element.data(
                "step"
                ,buttonComponent.$element.closest(".instructions-sidebar-tools-button").data("step")
            );
            this.buttons.push(buttonComponent);

        })
        this.isOpen = false; // TODO Move this to state.

        // Initial state
        let feedbackPossible = false;
        if (this.task.document) {
            feedbackPossible = this.task.document.isReadyForFeedback();
        }
        this.setState({
            "feedbackPossible": feedbackPossible,
        })

        this.bindEvents();
    }

    bindEvents() {
        console.log("InstructionSidebarComponent.bindEvents()");
        for (let button of this.buttons) {
            button.bindEvent("click", this.buttonClicked, null, this);
        };
    }

    open($button=null) {
        // If the instruction is to open the sidebar, we need to click a button
        // so if no button is provided we just use the first one
        if (this.isOpen) return;
        if ($button == null) {
            $button = jQuery(this.buttons.first().$element)
        }
        this.buttonClicked($button)
    }

    buttonClicked(sidebar, event) {
        // 'this' is the button component
        console.log("InstructionSidebarComponent.buttonClicked()", this, sidebar, event);

        // If button is disabled, don't do anything.
        if (this.state["disabled"]) return;

        let step = this.$element.data("step");
        console.log(step);

        // Hide all instructions, show this step
        sidebar.task.hideInstructions();
        sidebar.task.showInstructions(step);
        
        console.log(this.state);
        if (this.state.selected) {
            sidebar.setState({"open":false})
            this.setState({"selected":false})
        } else {
            for (const key in sidebar.task.instructionsSidebars) {
                sidebar.task.instructionsSidebars[key].deselectButtons();
                sidebar.task.instructionsSidebars[key].setState({"open":false});
            }
            sidebar.setState({"open":true});
            this.setState({"selected":true});
            if (step != 2) {
                sidebar.task.document.closeFormat();
            }
        }
    }

    selectStep(step) {
        console.log("InstructionSidebarComponent.selectStep(step)", step);
        for (const button of this.buttons) {
            if (button.$element.data("step") == step) {
                console.log("FOUND");
                button.click(this);
                return;
            }
        }
        throw `InstructionSidebarComponent.selectStep(step): step ${step} not found.`;
    }

    deselectButtons() {
        for (const button of this.buttons) {
            button.setState({"selected":false});
        }
    }

    selectInstructionByName(instructionTypeName) {
        for (let instruction of this.task.instructionsComponents) {
            instruction.deselect();
            if (instruction.instructionTypeName == instructionTypeName) {
                instruction.select();
            }
        }
    }

    documentReady() {
        this.setState({"feedbackPossible": true})
    }

    render() {
        this.$element.toggleClass("collapsed", !this.state.open);
        for (const button of this.buttons) {
            if (button.$element.data("step") == 1 && !this.state.feedbackPossible) {
                button.setState({"disabled": true});
            } else {
                button.setState({"disabled": false});
            }
        }
    }
}