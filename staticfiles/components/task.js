import AbstractComponent from './abstractComponent.js';
import SelectorComponent from './selectorComponent/selector.js';
import DocumentComponent from './documentComponent/document.js';
import InstructionComponent from './instructionComponent/instruction.js';
import InstructionSidebarComponent from './instructionSidebarComponent/instructionSidebar.js';

export default class TaskView extends AbstractComponent {
    
    constructor($element) {
        super($element);
        // Elements
        this.$instructions;
        // Components
        this.instructionsComponents = [];
        this.instructionsSidebars = {};
        this.document;
        this.selector;
        // State
        this.state = {
            "id": null,
        }
        this.init();
    }

    init() {
        console.log("TaskView.init()");

        // Initialize sidebars
        this.instructionsSidebars["instructions"] = new InstructionSidebarComponent(jQuery("#task-instructions-wrapper"), this);
        this.instructionsSidebars["formats"] = new InstructionSidebarComponent(jQuery("#task-formats-wrapper"), this);

        // Initialize instructions
        this.$instructions = this.$element.find(".instruction");
        for (const $instruction of this.$instructions) {
            this.instructionsComponents.push(new InstructionComponent(jQuery($instruction), this));
        }

        // Initialize documents
        this.document = new DocumentComponent(".document", this);

        // Initialize selector of documents
        this.selector = new SelectorComponent("#selector-documents");
        this.selector.addFunction(this.selectorItemClick, [this.document]);

        // Set initial state of instructions
        this.collapseInstructions();
        this.instructionsSidebars["instructions"].selectStep(0);
        this.selectInstruction(0);
    }

    selectorItemClick(document, item) {
        console.log("TaskView.itemClicked()", document, item);
        let document_id = item.data("id")
        document.read(document_id);
    }

    hideInstructions() {
        for (const instruction of this.instructionsComponents) {
            instruction.hide();
        }
    }

    showInstructions(step=null) {
        for (const instruction of this.instructionsComponents) {
            if ((step != null && instruction.step == step) || step == null) {
                instruction.show();
            }
        }
    }

    collapseInstructions() {
        for (const instruction of this.instructionsComponents) {
            instruction.collapse();
        }
    }

    deselectInstructions() {
        for (const instruction of this.instructionsComponents) {
            instruction.deselect();
        }
    }

    openFormatsSidebar() {
        this.instructionsSidebars["formats"].open();
    }

    selectInstruction(index) {
        this.instructionsComponents[index].select();
    }

    selectFormatInstruction(instructionTypeName) {
        this.openFormatsSidebar();
        this.instructionsSidebars["formats"].selectInstructionByName(instructionTypeName);
    }
    
    deselectFormatInstruction(instructionTypeName) {
        for (let instruction of this.instructionsComponents) {
            console.log(instruction.instructionTypeName, instructionTypeName)
            if (instruction.instructionTypeName == instructionTypeName) {
                instruction.$element.removeClass("selected");
            }
        }
    }

    documentReady() {
        this.instructionsSidebars["instructions"].documentReady();
        this.instructionsSidebars["formats"].documentReady();
    }

    createDocument(name="New document", is_format=false, parent_document_id=null) {
        //path("create/", DocumentCreateView.as_view(), name="create")
        let url = "/document/create/";
        let taskId = this.$element.data("id");
        let dataPost = {
            "task_id": taskId,
            "name": name,
            "is_format": is_format,
            "parent_document_id": parent_document_id,
            "csrfmiddlewaretoken": Cookies.get('csrftoken')
        }
        return new Promise((resolve, reject) => { 
            jQuery.ajax({
                url: url,
                type: "POST",
                data: dataPost,
                success: (data) => {
                    console.log("TaskView.createDocument() success", data);
                    resolve(data);
                },
                error: function (xhr, errmsg, err) {
                    console.log(xhr.status + ": " + xhr.responseText);
                    reject(err);
                },
            })
        });
    }
}