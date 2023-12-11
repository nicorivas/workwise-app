import AbstractView from '../abstractView.js';
import FlowFormComponent from '../../components/flowFormComponent/flowForm.js';
import ButtonComponent from '../../components/buttonComponent/button.js';
import LLM from '../../js/llm.js';
/*
    Flow view, navigates through steps and collects components.
*/

export default class FlowView extends AbstractView {
    
    constructor(element, view, id=null) {
        super(element);
        this.id = this.$element.data("id");
        this.projectId = this.$element.data("project");
        this.actionId = this.$element.data("action");
        // Components
        this.flowForm;
        this.navPrevButton;
        this.navNextButton;
        this.init();
    }
    
    /**
     * @override
     */
    init() {
        this.loadComponents();
        this.setData(this.data);
    }

    /**
     * @override
     */
    loadComponents() {

        // Component that handles the flow form.
        this.flowForm = new FlowFormComponent('#flow-container', this);
        this.flowForm.init();

        if (jQuery("#btn-prev").length > 0) {
            this.navPrevButton = new ButtonComponent('#btn-prev', true, false);
            this.navNextButton = new ButtonComponent('#btn-next', true, false);
        }

        //this.navPrevInstructionButton = new ButtonComponent("#step__instruction__debug__prev", true, false);
        //this.navNextInstructionButton = new ButtonComponent("#step__instruction__debug__next", true, false);

        this.finishButton = new ButtonComponent('#btn-finish', true, false);

        this.bindEvents();
    }

    /**
     * @override
     */
    bindEvents() {

        // Navigating steps
        if (jQuery("#btn-prev").length > 0) {
            this.navPrevButton.bindEvent('click', this.flowForm.prevStep, null, this.flowForm);
            this.navNextButton.bindEvent('click', this.flowForm.nextStep, null, this.flowForm);
        }

        // Navigating instructions
        //this.navPrevInstructionButton.bindEvent('click', this.flowForm.prevInstruction, null, this.flowForm);
        //this.navNextInstructionButton.bindEvent('click', this.flowForm.nextInstruction, null, this.flowForm);

        this.finishButton.bindEvent("click", this.finishHandler, null, this);
    }
    
    /**
     * @override
     */
    render() {
        /**/
    }
    
    /*
        Returns user to the first flow page.
    */
    finishHandler(view) {
        // Send email by calling email endpoint
        let flow_id = view.id;
        let task_id = view.flowForm.task.id;
        jQuery.ajax({
            url: `/flow/${flow_id}/task/${task_id}/send_email/`,
            type: 'POST',
            data: {
                "csrfmiddlewaretoken": Cookies.get('csrftoken')
            },
            success: function(data) {
                console.log(data);
            },
            error: function(data) {
                console.log(data);
            }
        });
        //window.location.href = `/flow/${view.id}/`;
    }

}